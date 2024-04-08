# 玻璃幕墙振动数据可视化监管平台后端


## 🛠环境配置

使用vscode开发平台，安装Python和Django相应的插件，创建Python虚拟环境，安装Django。

```
pip install django
```

Django版本为3.2，

运行如下命令行出现欢迎界面即配置成功

```
python manage.py runserver
```



## 项目目录说明

```
|CurtainWallWeb-Backend			    项目根目录
├── backend				            项目名称
│   ├── __init__.py					inti文件，标识当前所在的项目目录是一个 Python 包
│   ├── settings.py					项目配置文件
│   ├── urls.py						url路径文件
│   └── wsgi.py						WSGI服务器程序的入口文件
|
├── device
├── monitor
├── setting
└── manage.py						命令行工具文件


```

