

#### 介绍
用户管理系统--B站武沛齐
Python+Django+MySQL

引用： https://gitee.com/cwk985/sms-b

#### 使用说明
1. 首先有python3环境（项目是3.10的环境）
2. 进入该项目目录，安装项目依赖包：`pip install -r requirements.txt`
3. mysql数据库，数据库名为:"`db-users`",然后去djangoProject01/settings.py文件中，找到DATABASES配置项，配置一下你的数据库名和密码（数据库密码默认为root）
4. 进入该项目目录，生成数据库迁移文件命令：1.`python manage.py makemigrations` 2.`python manage.py migrate`
5. 进入该项目目录，运行项目命令：`python manage.py runserver`
6.  **注意** ：如有疑问或需要具体教程私信up


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


