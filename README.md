
## 环境
Python 3.10.0

## 目录说明
1. mysite: 主项目
2. tma: tma 程序
3. apis: 接口项目，为Dapp前端提供数据接口
3. apis: job项目，定时任务

## dev

1. 配置python环境
```
python3.10 -m venv tutorial-env
source tutorial-env/bin/activate

sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysqlclient

pip install --upgrade mysqlclient


```
2. 安装django和依赖包
```
python -m pip install -r requirements.txt
```

3. 初始化数据库和管理员数据

```
source .env
python3 manage.py migrate
python3 manage.py createsuperuser
```

4. 为用户设置一个初始token用于首次登录
```
python3 manage.py addstatictoken [用户名]
```

5. 启动
```
python manage.py runserver
```

6. 访问管理后台，添加客户和客户的节点: http://127.0.0.1:8000/admin
7. 访问客户端，通过客户收益地址查询节点信息: http://127.0.0.1:8000/validators

8. 后期修改model后,在venv环境执行
```
python manage.py makemigrations
python manage.py migrate
```
## test
```shell
# 整体测试
python manage.py test
# 测试validators项目
python manage.py test supermap
# 测试scheduler项目测试中的ValidatorUtilTests
python manage.py test scheduler.tests.ValidateUtilTests
```


## production

1. 安装python3和pip

```
sudo apt install python3.9
sudo apt install python3-pip
sudo apt install python3.8-venv

source venv/bin/activite
python -m pip install uwsgi
sudo apt-get install libmysqlclient-dev
```

2. 安装依赖包
```
python -m pip install -r requirements.txt
```

3.修改配置文件settings.py
```
# 指定可访问的域名或者*表示所有域名
ALLOWED_HOSTS = ['*']

# 修改数据库配置

# 修改STATIC_ROOT，用于生成静态文件
```
生成静态文件，将nginx静态路由指向此路径
```
python manage.py collectstatic
```


4. 初始化数据库和管理员数据

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

5. 安装uwsgi
```
python3 -m pip install uwsgi==2.0.18
```
6. 配置uwsgi，保存为uwsgi.ini
```
[uwsgi]
# 虚拟主机模式
vhost = false
# ip端口
socket = 0.0.0.0:8997
# 是否主服务器
master = true
# 是否多线程
enable-threads = true
# 工作进程数
workers = 5
# wsgi文件的位置
wsgi-file = /var/www/backend-python/mysite/wsgi.py
# 项目的根目录
chdir = /var/www/backend-python

# 设置 pid 记录文件
pidfile = /var/run/uwsgi.pid
# 后台运行uwsgi, 如果想实时查看日志内容，可以使用 tail -f uwsgi.log
daemonize = /var/www/a/logs/uwsgi.log
```

## 配置说明

- notice_email_set: 邮件通知名单，类型为数组，例如: ["admin@tma.io"]


## 日志使用规范，列举了所有可选类型和多种内容拼接方式
```python
import logging
logger = logging.getLogger(__name__)

logger.info ('这是信息日志')
logger.warning('这是%s日志', '警告')
logger.error('这是%s日志', '错误')
logger.debug('这是{}日志'.format('调试'))
logger.critical('这是严重错误日志')
```

## FAQ

- 如何设置断点调试
```py
import pdb
# pdb.set_trace() 设置断点
# p i 打印变量i
# n 执行一行
# s 进入方法
# r 跳出方法
# c 执行
```

- simpleui安装失败
```
# 降级 setuptools（推荐使用这个版本）
pip install 'setuptools==65.5.1' --force-reinstall
# 再次安装 simpleui
pip install 'django-simpleui==2025.1.13'
```