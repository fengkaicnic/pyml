def snapshot(self, context, instance, image_href):
    """Create snapshot from a running VM instance.
    This command only works with qemu 1.1+
    """
    try:
        virt_dom = self._lookup_by_name(instance['name'])
    except exception.InstanceNotFound:
        raise exception.InstanceNotRunning()

    instance_disk = None
    if self._is_run_onebs(instance):
        instance_disk = os.path.join(FLAGS.ebs_instances_path, instance['name'], 'disk')
    else:
        instance_disk = os.path.join(FLAGS.instances_path, instance['name'], 'disk')

    back_image_id = None
    if os.path.exists(instance_disk):
        back_image_id = libvirt_utils.get_disk_backing_file(instance_disk)
    else:
        msg = (_("Failed snapshot %s, missing disk."%instance['name']))
        LOG.error(msg)
        raise Exception(msg)

    image_service = glance.get_default_image_service()
    try:
        base = image_service.show(context, back_image_id)
    except exception.ImageNotFound:
        msg = (_("Failed snapshot %s, cann't find base image information."%instance['name']))
        LOG.error(msg)
        raise Exception(msg)

    snapshot = image_service.show(context, image_href)
    metadata = {'is_public': False,
                'status': 'active',
                'name': snapshot['name'],
                'properties': {
                               'kernel_id': instance['kernel_id'],
                               'image_location': 'snapshot',
                               'image_state': 'available',
                               'owner_id': instance['project_id'],
                               'ramdisk_id': instance['ramdisk_id'],
                               }
                }
    if 'architecture' in base.get('properties', {}):
        arch = base['properties']['architecture']
        metadata['properties']['architecture'] = arch

    if 'os_version' in base.get('properties', {}):
        os_version = base['properties']['os_version']
        metadata['properties']['os_version'] = os_version

    # Find the disk
    xml_desc = virt_dom.XMLDesc(0)
    domain = etree.fromstring(xml_desc)
    source = domain.find('devices/disk/source')
    disk_path = source.get('file')
    image_format = self.get_disk_format(disk_path)
    metadata['disk_format'] = image_format
    metadata['container_format'] = base.get('container_format', 'bare')

    #out snapshot temp file       
    snapshot_directory = FLAGS.libvirt_snapshots_directory
    utils.ensure_tree(snapshot_directory)
    snapshot_name = uuid.uuid4().hex

    with utils.tempdir(dir=snapshot_directory) as tmpdir:
        # check if registyr_snapshot_only to the image service
        storage_path = ''
        if FLAGS.registry_snapshot_only:
            storage_path = os.path.join(FLAGS.ebs_images_path, snapshot_name)
            metadata['properties']['storage_locate'] = storage_path

        # Upload that image to the image service
        with self.file_open(out_path) as image_file:
            image_service.update(context,
                                 image_href,
                                 metadata,
                                 image_file)

        if FLAGS.registry_snapshot_only:
            cmd = ('mv', out_path, storage_path)
            self.execute(*cmd, run_as_root=True)


