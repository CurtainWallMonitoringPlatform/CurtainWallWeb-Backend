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
|backend		    项目根目录
├── backend			项目名称
│   ├── __init__.py	inti文件，标识当前所在的项目目录是一个 Python 包
│   ├── settings.py	项目配置文件
│   ├── urls.py		url路径文件
│   └── wsgi.py		WSGI服务器程序的入口文件
|
├── device
|
├── monitor
│   ├── __init__.py					
│   ├── admin.py	
│   ├── apps.py	
│   ├── models.py					
│   ├── test.py		
│   ├── urls.py		路由配置文件，按顺序查找找到第一个匹配的URL，然后执行对应的view函数
│   └── views.py	用来写接口的逻辑代码，封装成函数，函数名就是接口名称
|
|
├── setting
|
└── manage.py		命令行工具文件


```

