from django.db import models

# Create your models here.


# 书表
class Books(models.Model):
    # 书表id
    id = models.AutoField(primary_key=True)
    # 书名
    title = models.CharField(max_length=32)
    # 出版日期
    date_pub = models.DateField()
    # 书与出版社的关系
    the_press = models.ForeignKey('Press')


# 出版社表
class Press(models.Model):
    # 出版社id
    id = models.AutoField(primary_key=True)
    # 出版商
    publisher = models.CharField(max_length=32)
    # 出版商地址
    address = models.CharField(max_length=50)


# 作者表
class Author(models.Model):
    # 出版社id
    id = models.AutoField(primary_key=True)
    # 作者名
    name = models.CharField(max_length=20)
    # 作者生日
    birthday = models.DateField()
    # 出版过的书
    books_es = models.ManyToManyField(to='Books')


# 登录人员信息表
class User(models.Model):
    # 用户id
    id = models.AutoField(primary_key=True)
    # 用户账号名
    username = models.CharField(max_length=12)
    # 用户登录密码
    password = models.CharField(max_length=24)


# 解释：
    # 出版社与书为：一对多关系，
    # 作者与书为多对多关系。

