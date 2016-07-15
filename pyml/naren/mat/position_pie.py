#coding:utf8

import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('qt4agg')
import pdb
zh_font = matplotlib.font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', size=14)

#调节图形大小，宽，高
plt.figure(figsize=(12,12))
#定义饼状图的标签，标签是列表
labels = [u'销售',u'java ',u'测试', u'产品', u'前端', u'猎头', u'andriod', u'市场', u'运营', u'设计', u'PHP', u'项目', u'文案', u'python', u'财务', u'其他']
#每个标签占多大，会自动去算百分比
sizes = [76, 38, 32, 31, 20, 20, 19, 16, 16, 16, 12, 12, 8, 7, 7, 132]
# colors = ['red','yellowgreen','lightskyblue']
#将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
# explode = (0,0,0)

patches,l_text,p_text = plt.pie(sizes,labels=labels,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                startangle = 90,pctdistance = 0.6)
# pdb.set_trace()
# for font in patches[1]:
#     font.set_fontproperties(matplotlib.font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', sizes=14))


#labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
#autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
#shadow，饼是否有阴影
#startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
#pctdistance，百分比的text离圆心的距离
#patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

#改变文本的大小
#方法是把每一个text遍历。调用set_size方法设置它的属性
for t in l_text:
    t.set_size=(30)
    t.set_fontproperties(matplotlib.font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc'))
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
# plt.ylabel(fontproperties=zh_font)
# plt.legend(prop=zh_font)
# plt.xlabel(fontproperties=zh_font)
plt.show()
