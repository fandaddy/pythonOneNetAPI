#!/usr/bin/python
# -*- coding: UTF-8 

from OneNetApi import *


if __name__ == '__main__':
    test = OneNetApi("Ur api key")

    # 添加设备
    #title = "test11"
    #desc = "testing"
    #tags = ["test1", "test2"]
    #private = "false"
    #res1 = test.device_add(title = title, desc = desc, tags = tags, private = private)
    #print res1.content

    # 更新设备
    #device_id = *******
    #title = "test_abs"
    #private = 'true'
    #res2 = test.device_update(device_id = device_id, title = title, private = private)
    #print res2.content

    # 查询设备
    #device_id = *******
    #res3 = test.device_info(device_id = device_id)
    #print res3.content

    # 删除设备
    device_id = *******
    res4 = test.device_del(device_id = device_id)
    print res4.content

    # 添加数据
    #device_id = *******
    #无名参数要放在keyword前面
    #res1 = test.datapoint_add(device_id, 'temperature', 70)
    #print res1.content
    #res2 = test.datapoint_multi_add(device_id, 'temperature', 66, 'humidity', 70)
    #print res2.content

    # 获取数据
    # stream_id使用list
    #datastream_ids = ['temperature', 'humidity']
    #print type(datastream_ids)
    #start_time = "2016-07-30 00:00:01"
    #end_time = "2016-07-31 23:59:59"
    #limit = 100
    #res3 = test.datapoint_multi_get(device_id = device_id, start_time = start_time, end_time = end_time, limit = limit, datastream_ids = datastream_ids)
    #print res3.content

