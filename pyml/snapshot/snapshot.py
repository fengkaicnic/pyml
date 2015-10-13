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
        cmd = ('chmod', 'a+rwx', tmpdir)
        self.execute(*cmd, run_as_root=True)

        out_path = os.path.join(tmpdir, snapshot_name)
        (state, _max_mem, _mem, _cpus, _t) = virt_dom.info()
        state = LIBVIRT_POWER_STATE[state]

        #using copy command
        if state==power_state.SHUTDOWN:
            cmd = ('cp', '-f', disk_path, out_path)
            self.execute(*cmd, run_as_root=True)
        else:
            # create qcow2 image base on same backing_file with instance system disk
            # qemu-img create -f qcow2 -o  backing_file=/.../base.img  /.../system_disk.img        
            backing_file = self.get_disk_backing_file(disk_path)
            if not os.path.exists(backing_file):
                msg = "Failed create snapshot for %s, base image not exists"%instance['name']
                LOG.error(_(msg))
                raise Exception(msg)

            cmd = ('qemu-img', 'create', '-f', 'qcow2', '-o', 'backing_file=%s'%(backing_file), out_path)
            self.execute(*cmd, run_as_root=True)

            cmd = ('chmod', 'a+rw', out_path)
            self.execute(*cmd, run_as_root=True)

            #chck if have block-jobs on instance for drive-virtio-disk0
            cmd = ('virsh', 'qemu-monitor-command', '--hmp', instance['name'], 'info block-jobs')
            result = self.execute(*cmd, run_as_root=True)

            if 'No active jobs' not in result[0]:
                msg = "Have a snapshot job executing, will be canceled."
                LOG.warn(_(msg))
                cmd = ('virsh', 'qemu-monitor-command --hmp %s block_job_cancel drive-virtio-disk0'%(instance['name']))
                result = self.execute(*cmd, run_as_root=True)

            #execute drive_mirror
            cmd = ('virsh', 'qemu-monitor-command --hmp %s drive_mirror -n drive-virtio-disk0 %s'%(instance['name'], out_path))
            self.execute(*cmd, run_as_root=True)

            #check drive_mirror state, waiting for drive_mirror finished 
            cmd = ('virsh', 'qemu-monitor-command --hmp %s info block-jobs'%(instance['name']))
            result = self.execute(*cmd, run_as_root=True)
            if 'Type mirror' not in result[0]:
                msg = 'Failed create snapshot, with command %s, result %s'%(cmd,result)
                LOG.error(_(msg))
                raise Exception(msg)

            if 'Type mirror' not in result[0]:
                msg = 'Failed get snapshot progress information, failed execute pre snapshot command ?'
                LOG.error(_(msg))
                raise Exception(msg)
            else:
                result = result[0].split(' ')
                snap_size = result[5]
                base_size = result[7]
                while snap_size!=base_size:
                    time.sleep(2)
                    result = self.execute(*cmd, run_as_root=True)
                    result = result[0].split(' ')
                    snap_size = result[5]
                    base_size = result[7]

            #end drive_mirror job
            cmd = ('virsh', 'qemu-monitor-command --hmp %s block_job_cancel drive-virtio-disk0'%(instance['name']))
            self.execute(*cmd, run_as_root=True)
        # check if registyr_snapshot_only to the image service
        storage_path = ''
        if FLAGS.registry_snapshot_only:
            storage_path = os.path.join(FLAGS.ebs_images_path, snapshot_name)
            metadata['properties']['storage_locate'] = storage_path

        if FLAGS.qemu_version_snapshot:
            qemu_kvm_version = utils.get_qemu_kvm_version()
            qemu_kvm_bool = utils.compare_qemu_version(qemu_kvm_version, FLAGS.qemu_kvm_version_update_xml)
            if qemu_kvm_bool >= 0:
                cmdq1 = ('mv', out_path, out_path+'bk')
                self.execute(*cmdq1, run_as_root=True)
                cmdq2 = ('qemu-img', 'convert', '-f', 'qcow2', '-O', 'qcow2', '-o', 'compat=0.10', out_path+'bk', out_path)
                self.execute(*cmdq2, run_as_root=True)
                cmdq3 = ('rm', '-f', out_path+'bk')
                self.execute(*cmdq3, run_as_root=True)

        # Upload that image to the image service
        with self.file_open(out_path) as image_file:
            image_service.update(context,
                                 image_href,
                                 metadata,
                                 image_file)

        if FLAGS.registry_snapshot_only:
            cmd = ('mv', out_path, storage_path)
            self.execute(*cmd, run_as_root=True)


