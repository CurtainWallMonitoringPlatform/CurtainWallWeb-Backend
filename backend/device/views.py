from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
import uuid
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from device.models import *
from argparse import _ActionsContainer
import io
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from device.models import *
from rest_framework import status

from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import IntegrityError

from datetime import datetime, timedelta
from django.utils import timezone
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import csv


# def index(request):
#     return HttpResponse("Hello, world. You're at the setting index.")


class DeviceAPI(GenericViewSet):
    #serializer_class = ImageSerializer  # 序列化器类，序列化和反序列化使用的规则
    serializer_class = ModelSerializer
    queryset = Deviceinfo.objects.all()  #从device模型中获取所有设备的数据


    # 获取设备
    @action(methods=['get'], detail=False)
    def get_all_device(self, request):
        devices = self.get_queryset()
        result = []
        try:
            for device in devices:
                device_data = {
                    "deviceName": device.devicename,
                    "deviceId": device.deviceid,
                    #"online": device.online_status,
                    "offset": device.offset,
                    "lowerOuliter": device.loweroutlier,
                    "higherOuliter": device.upperoutlier
                }
                result.append(device_data)

        except Exception as e:
            return Response({
                "code": 500,
                "msg": "获取设备信息失败",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response_data = {
            "code": 200,
            "msg": "获取成功",
            "data": {
                "devices": result
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    # 获取单个设备信息
    @action(methods=['get'], detail=False)
    def get_single_device(self, request,**kwargs):
        
        device_id = kwargs.get('deviceId')  #前端通过path传参
        print('deviceId:',device_id)
        #device_id = request.GET.get('deviceId')
        #devices = self.get_queryset()
        device = get_object_or_404(Deviceinfo,deviceid = device_id )
        # devices = devices.filter(deviceid=device_id)

        result = []
        try:
            device_data = {
                "deviceName": device.devicename,
                "deviceId": device.deviceid,
                "offset": device.offset,
                "lowerOuliter": device.loweroutlier,
                "higherOuliter": device.upperoutlier
            }
            result.append(device_data)

            response_data = {
                "code": 200,
                "msg": "获取成功",
                "data": {
                    "devices": result
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "code": 500,
                "msg": "获取设备信息失败",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 新增设备
    @action(methods=['post'], detail=False)
    def add_device(self, request):
        try:
            device_name = request.GET.get('deviceName')
            lower_ouliter = float(request.GET.get('lowerOuliter'))
            higher_ouliter = float(request.GET.get('higherOuliter'))
            offSet = float(request.GET.get('offset', '0'))
            device_Id = request.GET.get('deviceId')

            #检查ID是否已存在
            if Deviceinfo.objects.filter(deviceid=device_Id).exists():
                error_response = {
                    "code": 409,
                    "msg": "设备ID已存在"
                }
                return Response(error_response, status=status.HTTP_409_CONFLICT)


            device = Deviceinfo(
                deviceid =device_Id,
                devicename=device_name,
                offset=offSet,
                loweroutlier=lower_ouliter,
                upperoutlier=higher_ouliter
            )
            device.save()

            response = {
                "code": 200,
                "msg": "新建设备成功",
                "data": {
                    "deviceId": device.deviceid,
                    "deviceName": device.devicename,
                    "offset": device.offset,
                    "lowerOuliter": device.loweroutlier,
                    "higherOuliter": device.upperoutlier
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValueError:
            error_response = {
                "code": 400,
                "msg": "参数错误"
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_response = {
                "code": 500,
                "msg": "服务器错误"
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    # 删除设备
    @action(methods=['delete'],detail=False)
    def delete_device(self,request,**kwargs):
        device_id = kwargs.get('deviceId')  #前端通过path传参
        #device_id = request.GET.get('deviceId')
        device = get_object_or_404(Deviceinfo, deviceid = device_id)  
        #DRF提供的一个辅助函数，用于获取指定主键值的对象。
        #如果找不到指定主键的对象，将引发HTTP 404错误。
        device.delete()
        return Response({
            "code": 200,
            'message':'成功删除设备'
        },status=status.HTTP_200_OK)
    
    # 修改设备信息
    @action(methods=['put'],detail=False)
    def modify_device(self,request,**kwargs):
        print(request.data) 
        device_id = kwargs.get('deviceId')  #前端通过path传参
        #device_id = request.GET.get('deviceId')
        device = get_object_or_404(Deviceinfo, deviceid = device_id) 
        
        try:
            device_name = request.GET.get('deviceName')
            lower_ouliter = float(request.GET.get('lowerOuliter'))
            higher_ouliter = float(request.GET.get('higherOuliter'))
            offSet = float(request.GET.get('offset'))
            
            device.deviceid = device_id
            device.devicename = device_name
            device.offset = offSet
            device.loweroutlier = lower_ouliter
            device.upperoutlier = higher_ouliter

            device.save()

            response = {
                "code": 200,
                "msg": "设备信息修改成功",
                "data": {
                    "deviceId": device.deviceid,
                    "deviceName": device.devicename,
                    "offset": device.offset,
                    "lowerOuliter": device.loweroutlier,
                    "higherOuliter": device.upperoutlier
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValueError:
            error_response = {
                "code": 400,
                "msg": "参数错误"
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_response = {
                "code": 500,
                "msg": "服务器错误"
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
