#!/usr/bin/python
# -*- coding: UTF-8 

from OneNetApi import *


if __name__ == '__main__':
    test = OneNetApi("Your Api Key")

    # 添加数据
    device_id = *******
    #无名参数要放在keyword前面
    #res1 = test.datapoint_add(device_id, 'temperature', 70)
    #print res1.content
    #res2 = test.datapoint_multi_add(device_id, 'temperature', 66, 'humidity', 70)
    #print res2.content

    # 获取数据
    # stream_id使用list
    datastream_ids = ['temperature', 'humidity']
    #print type(datastream_ids)
    start_time = "2016-07-30 00:00:01"
    end_time = "2016-07-31 23:59:59"
    limit = 100
    res3 = test.datapoint_multi_get(device_id = device_id, start_time = start_time, end_time = end_time, limit = limit, datastream_ids = datastream_ids)
    print res3.content

