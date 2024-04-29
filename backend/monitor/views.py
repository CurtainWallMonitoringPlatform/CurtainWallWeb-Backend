from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from monitor.models import Historicaldata, Abnormaldata, Deviceinfo

# 获取历史数据
@require_GET
def get_historical_data(request):
    device_id = request.GET.get('deviceId')
    start_time = request.GET.get('startTime')
    end_time = request.GET.get('endTime')

    # 将时间戳(毫秒级别的timestamp) 转换为 datetime 对象
    start_datetime = datetime.fromtimestamp(int(start_time) / 1000)
    end_datetime = datetime.fromtimestamp(int(end_time) / 1000)
    # 使用 timezone 模块来为 datetime 对象添加项目默认的时区信息
    start_datetime = timezone.make_aware(start_datetime)
    end_datetime = timezone.make_aware(end_datetime)

    # 根据请求参数构建查询条件
    query_params = {}
    if device_id:
        query_params['deviceid'] = device_id
    if start_time:
        query_params['time__gte'] = start_datetime
    if end_time:
        query_params['time__lte'] = end_datetime

    try:
        # 查询历史数据
        historical_data = Historicaldata.objects.filter(**query_params)
        # 构建返回数据
        data = {
            "xData": [entry.xdata for entry in historical_data],
            "yData": [entry.ydata for entry in historical_data],
            "zData": [entry.zdata for entry in historical_data],
            "time": [entry.time.strftime("%Y-%m-%d %H:%M:%S") for entry in historical_data],
            "deviceInfo": {}
        }
        # 如果指定了设备编号，则查询设备信息
        if device_id:
            device_info = Deviceinfo.objects.get(deviceid=device_id)
            data["deviceInfo"] = {
                "deviceId": device_info.deviceid,
                "deviceName": device_info.devicename
            }

        response = {
            "code": 200,
            "msg": "success",
            "data": data
        }
        return JsonResponse(response, status=200)

    except Deviceinfo.DoesNotExist:
        error_response = {
            "code": -1,
            "msg": "Device not found",
            "data": {}
        }
        return JsonResponse(error_response, status=404)
    except Exception as e:
        error_response = {
            "code": -1,
            "msg": str(e),
            "data": {}
        }
        return JsonResponse(error_response, status=500)


# 获取异常数据
@require_GET
def get_abnormal_data(request):
    device_id = request.GET.get('deviceId')
    start_time = request.GET.get('startTime')
    end_time = request.GET.get('endTime')

    # 将时间戳(毫秒级别的timestamp) 转换为 datetime 对象
    start_datetime = datetime.fromtimestamp(int(start_time) / 1000)
    end_datetime = datetime.fromtimestamp(int(end_time) / 1000)
    # 使用 timezone 模块来为 datetime 对象添加项目默认的时区信息
    start_datetime = timezone.make_aware(start_datetime)
    end_datetime = timezone.make_aware(end_datetime)

    # 根据请求参数构建查询条件
    query_params = {}
    if device_id:
        query_params['deviceid'] = device_id
    if start_time:
        query_params['recordtime__gte'] = start_datetime
    if end_time:
        query_params['recordtime__lte'] = end_datetime

    try:
        # 查询历史数据
        abnormal_data = Abnormaldata.objects.filter(**query_params)
        # 构建返回数据
        x_data = []
        y_data = []
        z_data = []
        x_time = []
        y_time = []
        z_time = []
        for entry in abnormal_data:
            if entry.direction == 'X':
                x_data.append(entry.data)
                x_time.append(entry.recordtime.strftime("%Y-%m-%d %H:%M:%S"))
            elif entry.direction == 'Y':
                y_data.append(entry.data)
                y_time.append(entry.recordtime.strftime("%Y-%m-%d %H:%M:%S"))
            elif entry.direction == 'Z':
                z_data.append(entry.data)
                z_time.append(entry.recordtime.strftime("%Y-%m-%d %H:%M:%S"))
        # 构建返回数据结构
        data = {
            "xData": x_data,
            "yData": y_data,
            "zData": z_data,
            "xTime": x_time,
            "yTime": y_time,
            "zTime": z_time,
            "deviceInfo": {}
        }
        # 如果指定了设备编号，则查询设备信息
        if device_id:
            device_info = Deviceinfo.objects.get(deviceid=device_id)
            data["deviceInfo"] = {
                "deviceId": device_info.deviceid,
                "deviceName": device_info.devicename,
                "lowerOutlier": device_info.loweroutlier,
                "upperOutlier": device_info.upperoutlier
            }

        response = {
            "code": 200,
            "msg": "success",
            "data": data
        }
        return JsonResponse(response, status=200)

    except Deviceinfo.DoesNotExist:
        error_response = {
            "code": -1,
            "msg": "Device not found",
            "data": {}
        }
        return JsonResponse(error_response, status=404)
    except Exception as e:
        error_response = {
            "code": -1,
            "msg": str(e),
            "data": {}
        }
        return JsonResponse(error_response, status=500)
