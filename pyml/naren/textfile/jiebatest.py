#coding:utf8
import jieba
import sys
reload(sys)
import os
sys.setdefaultencoding('utf8')

jieba.load_userdict('dict.txt')

txt = 'asp.netPC端网页制作前端开发objective-c岗位职责:1、参与公司移动终端的开发设计；2、负责产品 iPhone/iPad App 的设计、开发与维护工作，为用户呈现最好的界面交互体验；2、优化客户端模块结构及流程逻辑，产品适配和升级。任职要求：1、2年以上iOS开发经验，具有较强的学习领悟能力和上进心；2 、精通 Objective-C 语言；扎实的iOS应用软件开发基础；3、精通数据结构和算法者优先；4、具有独立研发能力和解决问题能力；以及良好的产品意识和沟通协作能力；5、热衷于软件开发，擅长逻辑思维。  '

seglst = jieba.cut(txt, cut_all=False)

print '//'.join(seglst)