#-*-coding:utf8-*-
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')
if(len(sys.argv)>=2):
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"请输入user_id: "))
    #user_id = 2080779295

cookie = {"Cookie": "# paste your Cookie here"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

html = requests.get(url, cookies = cookie).content
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = "" 
urllist_set = set()
word_count = 1
image_count = 1

print u'爬虫准备就绪...'

#爬取的页数, 把这段注释掉可以爬取所有页数
if pageNum > 1 :
    pageNum = 1
  
for page in range(1,pageNum+1):

  #获取lxml页面
  url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
  lxml = requests.get(url, cookies = cookie).content

  #文字爬取
  print u'开始爬取文字内容'
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count>=4:
      text = "%d :"%(word_count-3) +text+"\n"
    else :
      text = text+"\n"
    print text
    result = result + text
    word_count += 1

  #图片爬取，使用BeautifulSoup，具体用法可参考其文档
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  print u'开始爬取图片链接'
  for imgurl in urllist:
    #把图片的链接添加至urllist_set
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    print imgurl
    image_count +=1

#保存文字内容
fo = open("/home/vincent/git/Python/weibo/crawler/text%s"%user_id, "wb")
fo.write(result)
word_path=os.getcwd()+'/%d'%user_id
print u'文字微博爬取完毕'

#保存图片链接
link = ""
fo2 = open("/home/vincent/git/Python/weibo/crawler/img%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
  link = link + eachlink +"\n"
fo2.write(link)
print u'图片链接爬取完毕'


#下载图片
if not urllist_set:
  print u'该页面中不存在图片'
else:
  #下载图片,保存在当前目录的文件夹下
  image_path=os.getcwd()+'/weibo_image'
  if os.path.exists(image_path) is False:
    os.mkdir(image_path)
  x=1
  for imgurl in urllist_set:
    temp= image_path + '/%s.jpg' % x
    print u'正在下载第%s张图片' % x
    try:
      urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
    except:
      print u"该图片下载失败:%s"%imgurl
    x+=1

print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)
