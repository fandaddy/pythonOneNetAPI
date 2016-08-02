#!usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import time
from urllib import urlencode

#class DataPoint:
#    def __init__(self):
#        self.streamID = ''  #数据流名称
#        self.value = 0      #数据流的值
#        self.time = 0       #数据流的时间

#API调用基本地址
base_url = "http://api.heclouds.com"

class OneNetApi():

    def __init__(self, key = None):
        self.__apikey = key
        self.__baseurl = base_url
        self.header = {'api-key': self.__apikey}

    def paddingUrl(self, url):
        return base_url + url

    # 设备相关API
    def device_add(self):
        print "先空着"

    def device_del():
        print "先空着"

    # 数据流相关API
    def set_devid(self, device_id):
        self.__device_id = device_id

    #def datastream(self):
        #api = "/devices/{device_id}/datapoints?type=3".format(device_id = self.__device_id)
    
    def _call(self, url, method, jdata = None, params = None):
        url = self.paddingUrl(url)
        s = requests.session()
        if method == 'POST':
            if jdata != None:
                res = s.post(url, data = jdata, headers = self.header)
            else:
                res = s.post(url, headers = self.header)

        if method == 'GET':
            res = s.get(url, headers = self.header, params = params)
        return res

    # 数据点操作
    # 增加数据点
    def datapoint_add(self, device_id = None, datastream_id = None, datas = None):
        if(datas == None):
            return 1
        if(device_id == None or datastream_id == None):
            return 0
        api = "/devices/{device_id}/datapoints?type=3".format(device_id = device_id)
        #values = {"datastreams":[{"id":datastream_id, "datapoints":[{"values":datas}]}]}
        values = {datastream_id:datas}
        jdata = json.dumps(values)
        #print jdata
        r = self._call(api, 'POST', jdata)
        return r

    # 多个数据点一次添加
    def datapoint_multi_add(self, device_id = None, *datas):
        if(datas == None):
            return 1
        if(device_id == None):
            return 0
        api = "/devices/{device_id}/datapoints?type=3".format(device_id = device_id)
        values = {}
        i = 1
        s_id = ''
        for data in datas:
            if i % 2 == 1:
                s_id = data
            else:
                values[s_id] = data
            i = i + 1
        jdata = json.dumps(values)
        r = self._call(api, 'POST', jdata)
        return r

    # 获取单个数据点
    def datapoint_get(self, device_id = None, datastream_id = None, start_time = None, end_time = None, limit = None, cursor = None):
        if device_id == None or datastream_id == None:
            return 0

        return self.datapoint_multi_get(device_id, start_time, end_time, limit, cursor, datastream_id)

    # 获取多个数据点
    def datapoint_multi_get(self, device_id = None, start_time = None, end_time = None, limit = None, cursor = None, datastream_ids = None):
        params = {}
        if device_id == None:
            return -1
        if datastream_ids != None:
            if type(datastream_ids) == list:
                datastream_ids = ",".join(datastream_ids)
                #print 'join!',datastream_ids
            params['datastream_id'] = datastream_ids;

        if start_time != None:
            start_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
            params['start'] = start_time
        if end_time != None:
            end_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            params['end'] = end_time
        if limit != None:
            params['limit'] = limit
        if cursor != None:
            params['cursor'] = cursor

        #params_enco = urlencode(params)
        #print params
        api = "/devices/{device_id}/datapoints?".format(device_id = device_id);
        return self._call(api, "GET", params = params)


