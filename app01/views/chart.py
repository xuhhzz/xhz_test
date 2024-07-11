# 开发时间 2022/11/1 9:52
# 当前文件: chart.py

from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """数据统计页面"""
    return render(request, "chart_list.html")


def chart_bar(request):
    """ 构造柱状图的数据"""
    # 数据可以去数据库中获取
    legend = ["萧炎", "美杜莎"]

    series_list = [
        {
            "name": '萧炎',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 100]
        },
        {
            "name": '美杜莎',
            "type": 'bar',
            "data": [30, 40, 66, 20, 20, 100]
        }
    ]

    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据"""

    db_data_list = [
        {"value": 2048, "name": 'IT部门'},
        {"value": 1735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ["河北", "上海"]

    series_list = [
        {
            "name": '河北',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 100]
        },
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [30, 40, 66, 20, 20, 100]
        }
    ]

    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)


def chart_highcharts(request):
    """ highcharts实例"""
    return render(request, "highcharts.html")
