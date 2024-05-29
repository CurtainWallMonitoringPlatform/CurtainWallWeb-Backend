from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from monitor.models import Historicaldata, Abnormaldata, Deviceinfo, Warning

# 获取历史数据
@require_GET
def get_historical_data(request):
    device_id = request.GET.get('deviceId')
    start_time = request.GET.get('startTime')
    end_time = request.GET.get('endTime')

    # 根据请求参数构建查询条件
    query_params = {}
    if device_id:
        query_params['deviceid'] = device_id
    if start_time:
        start_datetime = convert_timestamp_to_datetime(start_time)
        query_params['time__gte'] = start_datetime
    if end_time:
        end_datetime = convert_timestamp_to_datetime(end_time)
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

    # 根据请求参数构建查询条件
    query_params = {}
    if device_id:
        query_params['deviceid'] = device_id
    if start_time:
        start_datetime = convert_timestamp_to_datetime(start_time)
        query_params['recordtime__gte'] = start_datetime
    if end_time:
        end_datetime = convert_timestamp_to_datetime(end_time)
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


# 获取报警记录
@require_GET
def get_warning_page(request):
    try:
        # 先读取请求参数
        device_id = request.GET.get('deviceId')
        start_time = request.GET.get('startTime')
        end_time = request.GET.get('endTime')
        level = request.GET.get('level')
        page_no = int(request.GET.get('pageNo'))
        page_size = int(request.GET.get('pageSize'))

        # 按照push_time降序排列
        queryset = Warning.objects.all().order_by('-push_time')

        # 获取所有设备信息
        device_info = {}
        device_list = Deviceinfo.objects.all()
        # 将查询结果存储到字典中
        for row in device_list:
            id = row.deviceid
            device_info[id] = {
                'deviceName': row.devicename,
                'offset': row.offset,
                'lowerOutlier': row.loweroutlier,
                'upperOutlier': row.upperoutlier
            }

        if device_id:
            queryset = queryset.filter(deviceid=device_id)

        if start_time:
            start_datetime = convert_timestamp_to_datetime(start_time)
            queryset = queryset.filter(push_time__gte=start_datetime)

        if end_time:
            end_datetime = convert_timestamp_to_datetime(end_time)
            queryset = queryset.filter(push_time__lte=end_datetime)

        if level:
            queryset = queryset.filter(level=level)


        # 分页处理
        paginator = Paginator(queryset, page_size)
        page = paginator.page(page_no)

        if device_id:
            deviceName = device_info[device_id]['deviceName']
            offset = device_info[device_id]['offset']
            lowerOutlier = device_info[device_id]['lowerOutlier']
            upperOutlier = device_info[device_id]['upperOutlier']
            data = {
                'records': [
                    {
                        'recordId': w.id,
                        'pushTime': w.push_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'level': w.level,
                        'emails': w.emails,
                        'deviceId': w.deviceid,
                        'deviceName': deviceName,
                        'lowerOutlier': lowerOutlier,
                        'upperOutlier': upperOutlier,
                        'offset': offset
                    } for w in page
                ],
                'total': paginator.count, # 总记录数
                'pages': paginator.num_pages, # 总页数
                'currentNum': page.number # 当前页数
            }
        else:
            data = {
                'records': [
                    {
                        'recordId': w.id,
                        'pushTime': w.push_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'level': w.level,
                        'emails': w.emails,
                        'deviceId': w.deviceid,
                        'deviceName': device_info[w.deviceid]['deviceName'],
                        'lowerOutlier': device_info[w.deviceid]['lowerOutlier'],
                        'upperOutlier': device_info[w.deviceid]['upperOutlier'],
                        'offset': device_info[w.deviceid]['offset']
                    } for w in page
                ],
                'total': paginator.count,  # 总记录数
                'pages': paginator.num_pages,  # 总页数
                'currentNum': page.number  # 当前页数
            }

        return JsonResponse({
            'code': 200,
            'msg': "success",
            'data': data
        }, status=200)
    except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': "Error: " + str(e)
            }, status=500)

def convert_timestamp_to_datetime(timestamp):
    """
    Converts a timestamp (in milliseconds) to a Django-aware datetime object.
    """
    try:
        # 将时间戳(毫秒级别的timestamp) 转换为 datetime 对象
        datetime_obj = datetime.fromtimestamp(int(timestamp) / 1000)
        # 使用 timezone 模块来为 datetime 对象添加项目默认的时区信息
        datetime_obj = timezone.make_aware(datetime_obj)
        return datetime_obj
    except Exception as e:
        raise Exception(f"Error converting timestamp to datetime: {e}")