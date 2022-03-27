
## 使用方法
### 运行环境

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

CMD切换到当前目录下,运行

```cmd
python autoreport.py
```

然后输入用户名密码即可

如果想桌面生成图标运行,双击`runit.vbs`,就会在桌面生成运行图标,下次双击即可运行

![图标](./img/health.ico)


### Linux

cd切换到当前代码目录下,运行
```shell
python autoreport.py
```
然后输入用户名密码即可






## data.json 数据获取方法

[登陆打卡地址](https://weixine.ustc.edu.cn/2020/home)

使用 F12 开发者工具抓包之后得到数据，按照 json 格式写入 data.json 中

- 登录进入 [登陆打卡地址](https://weixine.ustc.edu.cn/2020/home)，打开开发者工具（Chrome 可以使用 F12 快捷键），选中 Network 窗口：

- 点击确认上报，点击抓到的 daliy_report 请求，在 Payload 下面找到 Form Data 这就是每次上报提交的信息参数
![](https://cdn.jsdelivr.net/gh/RongkangXiong/pic-bed/blog/img/20220326175051.png)

将找到的 Data 除 _token （每次都会改变，所以不需要复制，脚本中会每次获取新的 token 并添加到要提交的数据中）外都复制下来，存放在 data.json 中，并参考示例文件转换为对应的格式


