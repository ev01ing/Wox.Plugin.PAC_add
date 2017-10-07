# 说明


#### 关于shadowsocks的pac

我用的是这个版本![shadowsocks](https://github.com/shadowsocks/shadowsocks-windows)，pac有两个文件，一个是pac.txt，还有一个是user-rule.txt。可能你的没有第二个，但是可以自定义出来。如果你要添加一个网站让其走代理，该pac.txt太麻烦，而且这个文件有些复杂。所以就有了user-rule.txt，直接往里面写网址就行了。

这个插件本来准备在这个基础上写一个插件出来，但是更改了user-rule.txt之后需要重启shadowsocks才能生效。此插件没有完成也是卡在了这里，关闭后开启的时候wox卡死，python的非阻塞api完全失效。但是奇怪的是，我刚开始写这个功能的时候是已经成功了的，故把这个代码版本放在一个分支里，有需要的可以下载来试试可以运行不

#### 使用

正式使用前请配置你的ss的名字和放置目录
```
pac set name yourssname
pac set directory yourssdirectory
```

添加网址到user-rule.txt中
```
pac google.com
```
可以输入一个复杂的网址，但是默认加入其最次的域名，比如```https://map.google.com/some```会加入```map.google.com```到user-rule.txt文件中

删除某个
```
pac delete
```
找到对应的域名，回车即可删掉。因为重启导致wox崩溃的问题没有解决，所以暂不支持匹配。


#### 依赖

本程序使用了python的os, traceback, subprocess及ConfigParser包，请满足需求再使用