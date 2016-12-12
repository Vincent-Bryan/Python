---
title:  微博爬虫
grammar_cjkRuby: true
---

### 功能
> 给定用户id，获取其微博的文字内容、图片链接并将其保存

### 环境
* pyhton2.7
* 依赖库：urllib2, BeautifulSoup, requests, lxml
### 使用（Chrome）
* 修改代码中的70行的文字内容保存路径和77行图片链接路径
* 打开新浪微博的移动端登录：http://m.weibo.cn/
* 按==F12==打开开发者工具
* 点开==network==，将==Preserve log==选上
* 输入账号密码，登录微博
* 在==network==中，找到==m.weibo.com==->==Headers==->==Request Headers==->==Cookie==，将其复制到代码的==paste your Cookie here==
![enter description here][1]
 
* 点击所要爬取的用户头像，复制其地址栏的id，如：http://m.weibo.cn/u/12345678, 则其id为12345678
* 运行爬虫，按其提示输入id
* 等待爬取结果


  [1]: ./images/cookie.png "cookie.png"