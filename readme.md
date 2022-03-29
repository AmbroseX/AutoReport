# 南七技校自动健康打卡报备脚本

![School](https://img.shields.io/badge/School-URC-blue.svg)
![Language](https://img.shields.io/badge/language-Python3-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/RongkangXiong/AutoReport)
![GitHub forks](https://img.shields.io/github/forks/RongkangXiong/AutoReport)


## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**



## 使用方法
### 运行环境

- 直接安装依赖

```python
pip install -r requirements.txt
```

- python
- 安装包

```python
pip install requests
pip install argparse
pip install ast
pip install datetime
pip install pytz
pip install bs4
pip install re
pip install getpass
```

可以更改`autoreport.py`中的

```python
    everyhours = 5 # hours 每多少小时进行打卡
    waittime = 10 # seconds 等待多长时间
```
调整每多长时间打一次卡,输出参数每多久更新一次

### Windows

- 输入用户名密码运行

CMD切换到当前目录下,运行

```cmd
python autoreport.py
```

然后输入用户名密码即可

如果想桌面生成图标运行,双击`runit.vbs`,就会在桌面生成运行图标,下次双击即可运行

![图标](./img/health.ico)

- 带参数运行

```cmd
python autoreport.py --username [SA...] --password [密码]
```

### Linux

cd切换到当前代码目录下,运行
```shell
python autoreport.py
```
然后输入用户名密码即可

- 带参数运行

```shell
python autoreport.py --username [SA...] --password [密码]
```

## 无需输入账号密码

请使用 `NopasswdAutoreport.py`,修改里面的用户名和密码,可以加入每日计划中,定时打卡


## data.json 数据获取方法

[登陆打卡地址](https://weixine.ustc.edu.cn/2020/home)

使用 F12 开发者工具抓包之后得到数据，按照 json 格式写入 data.json 中

- 登录进入 [登陆打卡地址](https://weixine.ustc.edu.cn/2020/home)，打开开发者工具（Chrome 可以使用 F12 快捷键），选中 Network 窗口：

- 点击确认上报，点击抓到的 daliy_report 请求，在 Payload 下面找到 Form Data 这就是每次上报提交的信息参数
![](https://cdn.jsdelivr.net/gh/RongkangXiong/pic-bed/blog/img/20220326175051.png)


