#coding:utf8
import utils
import traceback
import generate_feature1

try:

    generate_feature1.generate_train(data_path='test', typen=u'Java')

except:
    traceback.print_exc()
