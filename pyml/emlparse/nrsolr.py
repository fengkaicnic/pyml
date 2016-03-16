#coding:utf8
import sys
from naren_solr import sales_solr

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    arg_map = {'name': '钰诚'}
    page_index = 0
    countofpage = 1
    solr_ip_port = '121.41.27.143:11082'
    num, lst = sales_solr.sales_search(arg_map, page_index, countofpage, solr_ip_port)

    print num
    print lst