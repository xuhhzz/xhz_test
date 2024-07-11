# 开发时间 2022/9/13 19:31
# 文件: account.py
"""
管理员 登录 注册 视图
"""
import os
import sys

# 获取当前脚本文件的目录路径
current_dir = os.path.dirname(os.path.realpath(__file__))

# 获取当前目录的祖父目录的路径
grandparent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

# 将祖父目录添加到系统路径中，以便Python解释器可以搜索到其中的模块
sys.path.append(grandparent_dir)


from django.shortcuts import render, redirect, HttpResponse
from app01.utils.form import LoginForm, AdminModelForm
from app01 import models
from app01.utils.my_code import check_code
from io import BytesIO


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code') # 用于获取表单中名为 'code' 的字段的值，并将其从表单数据中移除
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象 / None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}

        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成图片验证码"""

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便后续获取验证码再进行校验）
    request.session['image_code'] = code_string

    # 给session设置60s超时
    request.session.set_expiry(60)

    # 把图片写入到内存中
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


def register(request):
    """注册（添加管理员）"""

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'register.html', {'form': form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})

