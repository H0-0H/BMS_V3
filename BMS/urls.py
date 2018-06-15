"""BMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
Personal addition(个人添加)
    修改记录 :
        1、201804/03 : 为所有url添加别名，并使用分组命名方法命名链接
        2、
"""
from django.conf.urls import url
from django.contrib import admin
from APP01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 登录模块
    url(r'^sign_in/', views.sign_in, name='sign_in'),

    # 注销模块
    url(r'^sing_out/', views.sing_out, name='sign_out'),

    # 注册模块
    url(r'^register_name_ajax/', views.register_name_ajax, name='register_name_ajax'),  # ajax检验用户名是否被占用分模块
    # ajax检验第一次与第二次输入的密码是否一致
    url(r'^register_password_ajax/', views.register_password_ajax, name='register_password_ajax'),
    url(r'^register/', views.register, name='register'),  # 注册主体模块


    # 预留登录测试链接界面
    url(r'^cs/', views.cs, name='cs'),
    # url(r'^cs2/', views.cs2, name='cs2'),

    # 图书管理模块
    url(r'^book_dashboard/', views.book_dashboard, name='book_dashboard'),  # 图书管理模块
    url(r'^add_books/', views.add_books, name='add_books'),  # 添加图书模块
    url(r'^del_books/(?P<did>[\d]+)', views.del_books, name='del_books'),  # 删除图书模块
    url(r'^edit_books/(?P<did>[\d]+)', views.edit_books, name='edit_books'),   # 修改图书模块

    # 出版社管理模块
    url(r'^press_dashboard/', views.press_dashboard, name='press_dashboard'),  # 出版社管理模块
    url(r'^add_press/', views.add_press, name='add_press'),  # 添加出版社模块
    url(r'^del_press/(?P<did>[\d]+)', views.del_press, name='del_press'),  # 删除出版社模块
    url(r'^edit_press/(?P<did>[\d]+)', views.edit_press, name='edit_press'),  # 修改出版社模块

    # 作者管理模块
    url(r'^author_dashboard', views.author_dashboard, name='author_dashboard'),  # 作者管理模块
    url(r'^add_author', views.add_author, name='add_author'),  # 添加作者模块
    url(r'^del_author/(?P<did>[\d]+)', views.del_author, name='del_author'),  # 删除作者模块
    url(r'^edit_author/(?P<did>[\d]+)', views.edit_author, name='edit_author'),  # 修改作者模块

    # 默认界面
    url(r'', views.sign_in, name='sign_in'),
]
