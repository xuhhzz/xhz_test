# 开发时间 2022/10/20 8:44
# 当前文件: task.py
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app01 import models
from django import forms
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            'detail': forms.TextInput
        }


def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),       # 生成页码
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_add(request):
    print(request.POST)

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

