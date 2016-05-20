#coding:utf8
import utils
import traceback
import generate_feature1

try:

    generate_feature1.generate_train(data_path='test', position_name=u'招聘主管(有猎头经验优先)')

except:
    traceback.print_exc()
