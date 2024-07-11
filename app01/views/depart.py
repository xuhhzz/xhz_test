# File: depart.py
from urllib.parse import urlparse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import DepartModelForm
from django.contrib.sessions.models import Session

def get_user_level(request):
    try:
        session_id = request.session.session_key
        session = get_object_or_404(Session, session_key=session_id)
        user_id = session.get_decoded().get('info')['id']
        user = get_object_or_404(models.Admin, pk=user_id)
        return user.level
    except Session.DoesNotExist:
        return None  # Handle session not found gracefully

def check_admin_permission(view_func):
    def wrapper(request, *args, **kwargs):
        if get_user_level(request) != 1:
            messages.error(request, '非管理员，权限不足')
            return redirect('/depart/list/')
        return view_func(request, *args, **kwargs)
    return wrapper


from django.shortcuts import render, redirect
from urllib.parse import urlparse


def clean_url(request):
    # 获取当前请求的完整URL
    full_url = request.get_full_path()

    # 解析URL
    parsed_url = urlparse(full_url)

    # 获取路径部分，不包括查询字符串
    path = parsed_url.path
    print(path)
    # 如果路径已经是不带查询字符串的形式，直接返回
    if not parsed_url.query:
        return path

    # 否则，重定向到不带查询字符串的URL
    return redirect(path)


def depart_list(request):
    """部门列表"""
    # 调用 clean_url 函数处理重定向到不带查询字符串的URL

    # 进行部门列表的其他逻辑
    title = request.GET.get("title", '')
    hd_name = request.GET.get("hd_name", '')
    date_dict = {}
    if title:
        date_dict["title__contains"] = title
    if hd_name:
        date_dict['hd_name__contains'] = hd_name

    queryset = models.Department.objects.filter(**date_dict).order_by("-created")

    page_object = Pagination(request, queryset)

    # 渲染页面时使用处理后的不带查询字符串的 URL
    return render(request, 'depart_list.html',
                  {"queryset": page_object.page_queryset, "page_string": page_object.html()})
@check_admin_permission
def depart_add(request):
    """添加部门"""
    title = '添加数据'
    if request.method == 'GET':
        form = DepartModelForm()
        return render(request, 'change.html', {"form": form, 'title': title})

    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.error(request, '新增成功')
        return redirect('/depart/list/')

    return render(request, 'change.html', {"form": form, 'title': title})

@check_admin_permission
def depart_delete(request, nid):
    """删除部门"""
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')

@check_admin_permission
def depart_edit(request, nid):
    """修改部门"""
    title = '修改部门'
    row_object = get_object_or_404(models.Department, id=nid)

    if request.method == 'GET':
        form = DepartModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, 'title': title})

    form = DepartModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/depart/list/')

    return render(request, 'change.html', {"form": form, 'title': title})