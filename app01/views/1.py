from django.shortcuts import render, redirect, get_object_or_404
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def admin_list(request):
    """管理员列表"""
    search_data = request.GET.get('q', '')
    queryset = models.Admin.objects.filter(username__contains=search_data) if search_data else models.Admin.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """添加管理员"""
    title = '新建管理员'
    if request.method == 'POST':
        form = AdminModelForm(request.POST)
        if form.is_valid():
            if models.Admin.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', '用户已存在')
            else:
                form.save()
                return redirect('/admin/list/')
    else:
        form = AdminModelForm()

    return render(request, 'change.html', {'form': form, 'title': title})


def get_user_level(request):
    session_id = request.session.session_key
    session = get_object_or_404(Session, session_key=session_id)
    user_id = session.get_decoded().get('info')['id']
    user = get_object_or_404(models.Admin, pk=user_id)
    return user.level


def admin_edit(request, nid):
    """编辑管理员"""
    row_object = get_object_or_404(models.Admin, id=nid)

    if get_user_level(request) != 1:
        messages.error(request, '非管理员，权限不足')
        return redirect('/admin/list/')

    title = '编辑管理员'
    if request.method == 'POST':
        form = AdminEditModelForm(request.POST, instance=row_object)
        if form.is_valid():
            if models.Admin.objects.filter(username=form.cleaned_data['username']).exclude(id=nid).exists():
                form.add_error('username', '用户已存在')
            else:
                form.save()
                return redirect('/admin/list/')
    else:
        form = AdminEditModelForm(instance=row_object)

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """删除管理员"""
    if get_user_level(request) != 1:
        messages.error(request, '非管理员，权限不足')
        return redirect('/admin/list/')

    row_object = get_object_or_404(models.Admin, id=nid)
    row_object.delete()
    return redirect('/admin/list/')