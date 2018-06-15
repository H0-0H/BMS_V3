"""
创建时间 : 2018/03/31
版本号 : V2
文档名 : views.py
编辑人 : he_wm
作 用 : 后端逻辑处理
源存储位置 : D:\pycharm\python\BMS_V2\APP01\views.py
修改及增加功能记录 :
    修改时间 : 2018/04/02
    1、修复了登录界面，账号密码输入正确无法跳转到 book_dashboard 界面的问题（修改了返回指定界面的链接）
    修改时间 : 2018/04/03
    1、修改了各方法中对出版社、作者、图书，修改、删除 操作时获取id的方法（urls关键字传参方法）
    2、修改了各方法中redirect跳转页面的方法，使用页面别名进行url反向推导界面（界面起别名的方法）
    修改时间 : 2018/04/08
    1、为所有界面进入添加了cookie验证（函数名：check_login）
    修改时间 : 2018/04/08
    1、为所有界面进入由cookie验证改为session验证（函数名：check_login）
    添加时间 : 2018/04/08
    1、在横栏主菜单添加注销链接
    添加时间 : 2018/04/09
    1、启用主页注册按钮---->添加注册界面（ajax）
"""

from django.shortcuts import render, redirect, HttpResponse
from .models import Books, Press, Author, User
# 通过给url起别名进行反转映射需要导入的模块
from django.urls import reverse
from functools import wraps
# Create your views here.


# session 验证函数
def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        url = request.get_full_path()
        # login_user = request.COOKIES.get('login', None)
        # login_user = request.get_signed_cookie('sign_in', default=None, salt='SSS', max_age=100)
        # 获取session中的用户名与密码
        user = request.session.get('user')
        # 可以取多值实例
        # password = request.session.get('password')
        db_user = User.objects.get(username=user)
        # if request.session.get("user"):  # 登录成功
        if user == db_user.username:  # 登录成功
            # 被执行的函数
            return func(request, *args, **kwargs)
        # 如果不是登录用户就跳转到登录界面
        else:
            return redirect('/sign_in/?next={}'.format(url))
    return inner


# 登录界面
def sign_in(request):
    # 预设显示提示信息
    error_msg = ''
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 接收用户填写的用户名和密码
        _username = request.POST.get('user')
        _password = request.POST.get('password')
        # 判断数据库中是否含有此用户
        if User.objects.get(username=_username):
            # 由用户名获取此用户的所有数据
            obj_user = User.objects.get(username=_username)
            # 判断密码是否正确
            if obj_user.password == _password:
                # 获取动态的链接界面
                next_url = request.GET.get('next')
                # 返回动态界面
                # 解释 : 如果 next_url为空或者next_url不等于sign_in界面就走下一步
                if next_url and next_url != reverse('sign_in'):
                    # 返回cookie记录的界面
                    response = redirect(next_url)
                else:
                    # 返回固定界面
                    response = redirect(reverse('book_dashboard'))
                # red.set_cookie('login', '123')
                # 设置session验证
                request.session["user"] = _username
                request.session["password"] = _password
                return response
        else:
            error_msg = "登陆失败"
    return render(request, 'sign_in.html', {"error": error_msg})


# 注册界面
def register(request):
    if request.method == 'POST':
        _username = request.POST.get('input_username')
        _password = request.POST.get('input_password')
        user = User.objects.create(username=_username, password=_password)
        user.save()
        return redirect(reverse('sign_in'))
    return render(request, 'register.html')


# 检验用户名是否被占用分模块
def register_name_ajax(request):
        # 从请求中取到用户名
    _username = request.POST.get('username')
    # 去数据库中检查用户名是否被占用
    ret = User.objects.filter(username=_username)
    if ret:
        msg = '用户名已被占用'
    else:
        msg = '用户名未被占用'
    return HttpResponse(msg)


# 检验第一次与第二次输入密码是否一致
def register_password_ajax(request):
    password1 = request.POST.get('input_password1')
    password2 = request.POST.get('input_password2')
    if password1 == password2:
        msg = '密码一致'
    else:
        msg = '密码不一致'
    return HttpResponse(msg)


# 注销登录模块（清除session记录，跳转回登录界面）
def sing_out(request):
    # 把当前用户的session全部清理掉
    request.session.delete()
    return redirect(reverse('sign_in'))


# 前期测试界面1
@check_login
def cs(request):
    i1 = int(request.GET.get('i1', 0))
    i2 = int(request.GET.get('i2', 0))
    ret = i1+i2
    # 不需要回完整界面
    return HttpResponse(ret)


# 前期测试界面2(无cookie限制)
def cs2(request):
    i1 = int(request.GET.get('i1', 0))
    i2 = int(request.GET.get('i2', 0))
    ret = i1 + i2
    return render(request, 'cs.html', {'i1': i1, 'i2': i2, 'ret': ret})


# 图书控制界面
@check_login
def book_dashboard(request):
    # 获取整张图书表数据
    obj_books = Books.objects.all()
    # 返回给前端界面
    return render(request, 'book_dashboard.html', {"book_list": obj_books})


# 添加新图书
@check_login
def add_books(request):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _book_name = request.POST.get('book_name')  # 书名
        _book_aut = request.POST.getlist('book_aut')  # 作者
        _book_date = request.POST.get('book_date')  # 出版日期
        _book_press = request.POST.get('book_press')  # 出版社
        # 添加进数据库中
        book_obj = Books.objects.create(title=_book_name, date_pub=_book_date, the_press_id=_book_press)
        # 表关系为多对多的情况下添加数据方法
        book_obj.author_set.set(_book_aut)
        # 存储
        book_obj.save()
        # 获取book_dashboard界面别名
        url = reverse('book_dashboard')
        # 返回需要界面
        return redirect(url)
    # 获取所有作者信息
    obj_aut = Author.objects.all()
    # 获取所有出版社信息
    obj_press = Press.objects.all()
    # 将信息返回指定前端界面
    return render(request, 'add_books.html', {'aut_list': obj_aut, 'press_list': obj_press})


# 删除图书
@check_login
def del_books(request, did):
    # 获取前端点击删除按钮所在的行 数据的id
    # _del_book = request.GET.get('id')
    book_obj = Books.objects.get(id=did)
    # 删除此条数据
    book_obj.delete()
    # 通过路径别名，使django自动计算出路径（作用：再路径名称改变时，可以不用全盘修改路径）
    # url =
    # 返回指定前端界面
    return redirect(reverse('book_dashboard'))


# 编辑图书
@check_login
def edit_books(request, did):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _book_id = request.POST.get('book_id')  # 图书id
        _book_name = request.POST.get('book_name')  # 图书名称
        _book_aut = request.POST.getlist('book_aut')  # 图书作者
        _book_date = request.POST.get('book_date')  # 出版时间
        _book_press = request.POST.get('book_press')  # 出版社
        # 由图书id找到数据库中存储的数据行
        _obj_book = Books.objects.get(id=_book_id)
        # 修改数据
        _obj_book.title = _book_name
        _obj_book.date_pub = _book_date
        _obj_book.the_press_id = _book_press
        # 数据库存在多对多的外键时,修改数据信息使用此方法
        _obj_book.author_set.set(_book_aut)
        # 存储
        _obj_book.save()
        # url = reverse('book_dashboard')
        # 返回指定界面
        return redirect(reverse('book_dashboard'))
    # 获取所有作者信息
    obj_aut = Author.objects.all()
    # 获得所有出版社信息
    obj_press = Press.objects.all()
    # 获取数据库中的id为did的数据行
    obj_book = Books.objects.get(id=did)
    # 将数据返回指定界面
    return render(request, 'edit_books.html', {'book_list': obj_book, 'aut_list': obj_aut, 'press_list': obj_press})


# 出版社控制界面
@check_login
def press_dashboard(request):
    # 获取数据库中所有出版社信息
    obj_press = Press.objects.all()
    # 将数据返回指定界面
    return render(request, 'press_dashboard.html', {'press_list': obj_press})


# 添加新出版社
@check_login
def add_press(request):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _press_name = request.POST.get('press_name')  # 出版社名称
        _press_address = request.POST.get('press_address')  # 出版社地址
        # 在数据库Press表中添加此条数据
        obj_press = Press.objects.create(publisher=_press_name, address=_press_address)
        # 保存
        obj_press.save()
        # 获取/press_dashboard/页面的别名
        url = reverse('press_dashboard')
        # 返回给指定界面
        return redirect(url)
    # 显示指定界面
    return render(request, 'add_press.html')


# 删除出版社
@check_login
def del_press(request, did):
    # 获取前端点击删除按钮所在的行 数据的id
    # _del_press = request.GET.get(did)
    # 由获得的id在数据库中查找到所需的数据行
    obj_press = Press.objects.get(id=did)
    # 删除此条数据
    obj_press.delete()
    # 获取press_dashboard界面别名
    url = reverse('press_dashboard')
    # 返回指定前端界面
    return redirect(url)


# 编辑出版社
@check_login
def edit_press(request, did):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _press_id = request.POST.get('press_id')
        _press_publisher = request.POST.get('press_name')
        _press_address = request.POST.get('press_address')
        # 由出版社id找到数据库中存储的数据行
        _obj_press = Press.objects.get(id=_press_id)
        # 修改数据
        _obj_press.publisher = _press_publisher
        _obj_press.address = _press_address
        # 存储
        _obj_press.save()
        # 获取press_dashboard界面别名
        url = reverse('press_dashboard')
        # 返回指定界面
        return redirect(url)
    # 获取用户点击编辑按钮所在数据行的id
    # _edit_press = request.GET.get(did)
    # 获取id = _edit_press的所在行信息
    obj_press = Press.objects.get(id=did)
    # 将数据返回前端指定界面
    return render(request, 'edit_press.html', {'press_list': obj_press})


# 作者控制界面
@check_login
def author_dashboard(request):
    # 获取所有作者信息
    obj_aut = Author.objects.all()
    # 将数据返回前端指定界面
    return render(request, 'author_dashboard.html', {'author_list': obj_aut})


# 添加作者界面
@check_login
def add_author(request):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _author_name = request.POST.get('author_name')
        _author_date = request.POST.get('author_date')
        # 在数据库中添加此条数据
        obj_author = Author.objects.create(name=_author_name, birthday=_author_date)
        # 存储
        obj_author.save()
        # 获取author_dashboard界面别名
        url = reverse('author_dashboard')
        # 返回指定界面
        return redirect(url)
    # 单击添加按钮返回指定界面
    return render(request, 'add_author.html')


# 删除作者界面
@check_login
def del_author(request, did):
    # 获取前端点击删除按钮所在的行 数据的id
    # _del_author = request.GET.get(did)
    # 由获得的id在数据库中查找到所需的数据行
    obj_aut = Author.objects.get(id=did)
    # 删除此条数据
    obj_aut.delete()
    # 获取author_dashboard界面的别名
    url = reverse('author_dashboard')
    # 返回指定前端界面
    return redirect(url)


# 编辑作者界面
@check_login
def edit_author(request, did):
    # 如果请求是POST说明是前端界面向后端发送数据
    if request.method == 'POST':
        # 获取前端发送的所有数据
        _author_id = request.POST.get('author_id')
        _author_name = request.POST.get('author_name')
        _author_date = request.POST.get('author_date')
        # 由出版社id找到数据库中存储的数据行
        obj_author = Author.objects.get(id=_author_id)
        # 修改数据
        obj_author.name = _author_name
        obj_author.birthday = _author_date
        # 存储
        obj_author.save()
        # 获取author_dashboard界面的别名
        url = reverse('author_dashboard')
        # 返回指定界面
        return redirect(url)
    # 获取用户点击编辑按钮所在数据行的id
    # _edit_author = request.GET.get(did)
    # 获取id = _edit_author的所在行信息
    obj_aut = Author.objects.get(id=did)
    # 将数据返回指定界面
    return render(request, 'edit_author.html', {'author_list': obj_aut})
