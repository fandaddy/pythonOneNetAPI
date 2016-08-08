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
    
    def _call(self, url, method, jdata = None, params = None):
        url = self.paddingUrl(url)
        #print url
        s = requests.session()
        if method == 'POST':
            if jdata != None:
                res = s.post(url, headers = self.header, data = jdata)
            else:
                res = s.post(url, headers = self.header)
        if method == 'GET':
            res = s.get(url, headers = self.header, params = params)
        if method == 'PUT':
            res = s.put(url, headers = self.header, data = jdata)
        if method == 'DELETE':
            res = s.delete(url, headers = self.header)

        return res

    
    ##### 设备相关操作 #######
    # 新增设备
    def device_add(self, title = None, desc = None, tags = None, location = None, private = 'true', protocol = 'HTTP'):
        values = {}
        if title == None:
            return 0
        else:
            values['title'] = title
        if desc == None:
            values['desc'] = 'no description'
        else:
            values['desc'] = desc
        if tags != None:
            values['tags'] = tags
        if location != None:
            values['location'] = location
        values['private'] = private
        values['protocol'] = protocol
        jdata = json.dumps(values)
        api = "/devices"
        return self._call(api, 'POST', jdata)
    
    #更新设备信息
    def device_update(self, device_id = None, title = None, desc = None, private = 'true', tags = None, location = None):
        values = {}
        if device_id == None:
            return 0
        api = "/devices/{device_id}".format(device_id = device_id)
        if title != None:
            values['title'] = title
        if desc != None:
            values['desc'] = desc
        if private != None:
            values['private'] = private
        if tags != None:
            values['tags'] = tags
        if location != None:
            values['location'] = location
        jdata = json.dumps(values)
        return self._call(api, 'PUT', jdata) 
    
    # 查找单个设备信息
    def device_info(self, device_id = None):
        if device_id == None:
            return 0
        api = "/devices/{device_id}".format(device_id = device_id)
        return self._call(api, 'GET')

    # 删除单个设备
    def device_del(self, device_id = None):
        if device_id == None:
            return 0
        api = "/devices/{device_id}".format(device_id = device_id)
        return self._call(api, 'DELETE')

    ######### 数据流操作 ###############
    # 数据流新增
    def datastream_add(self, device_id = None, datastream_id = None):
        if device_id == None or datastream_id == None:
            return 0
        api = "/devices/{device_id}/datastreams".format(device_id = device_id)
        values = {}
        values['id'] = datastream_id
        jdata = json.dumps(values)
        #print jdata
        return self._call(api, 'POST', jdata)

    def datastream_update(self, device_id = None, datastream_id = None, datastream = None):
        if device_id == None or datastream_id == None or datastream == None:
            return 0
        api = "/devices/{device_id}/datastreams/".format(device_id = device_id)
        api = api + datastream_id
        jdata = json.dumps(datastream)
        return self._call(api, 'PUT', jdata = jdata)

    def datastream_del(self, device_id = None, datastream_id = None):
        if device_id == None or datastream_id == None:
            return 0
        api = "/devices/{device_id}/datastreams/".format(device_id = device_id) + datastream_id
        return self._call(api, 'DELETE')

    ############## 数据点操作 #################
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
            return 0
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

    ########### 触发器操作 #############
    # 触发器添加
    def trigger_add(self, trigger = None):
        if trigger == None:
            return 0
        api = "/triggers"
        jdata = json.dumps(trigger)
        # print jdata
        return self._call(api, 'POST', jdata = jdata)

    # 触发器更新
    def trigger_update(self, trigger_id = None, trigger = None):
        if trigger_id == None or trigger == None:
            return 0
        api = "/triggers/{trigger_id}".format(trigger_id = trigger_id)
        jdata = json.dumps(trigger)
        return self._call(api, 'PUT', jdata = jdata)

    # 触发器删除
    def trigger_del(self, trigger_id = None):
        if trigger_id == None:
            return 0
        api = "/triggers/{trigger_id}".format(trigger_id = trigger_id)
        return self._call(api, 'DELETE')

    # 触发器查看
    def trigger_list(self, page = None, per_page = None, title = None):
        if title == None:
            return 0
        api = "/triggers"
        params = {}
        params['title'] = title
        if page != None:
            params['page'] = page
        if per_page != None:
            params['per_page'] = per_page
        return self._call(api, "GET", params = params)


    ############ API权限 ###############
    def api_add(self, dev_id = None, title = None):
        if dev_id == None or title == None:
            return 0
        values = {}
        values = {"title":title, "permissions":[{"resources":[{"dev_id":dev_id}]}]}
        jdata = json.dumps(values)
        #print jdata
        api = "/keys"
        return self._call(api, "POST", jdata = jdata)

