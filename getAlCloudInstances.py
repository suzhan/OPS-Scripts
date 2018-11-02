# -*- coding: utf8 -*-
#  使用阿里云API读取线上主机信息
#

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
import json

# 创建AcsClient实例
client = AcsClient(
   "<your-access-key-id>", 
   "<your-access-key-secret>",
   "<your-region-id>"
)

# 创建request，并设置参数
request = DescribeInstancesRequest.DescribeInstancesRequest()
# 发起API请求并显示返回值
response = client.do_action_with_exception(request)
# print(response)
# json 格式化
jsonData = json.loads(response, encoding='utf-8')


print('总页数:', jsonData['TotalCount'])
pagesize = 10  # 分页数

request.set_PageSize(pagesize)    # 每页记录, 最大100
pagenum = jsonData['TotalCount'] // pagesize   # 总页数除分页取整数


for i in range(pagenum):
    print('页码:', i+1)
    request.set_PageNumber(i+1)    # 第几页
    response = client.do_action_with_exception(request)
    jsonData = json.loads(response, encoding='utf-8')

    instances = dict()

    for item in jsonData['Instances']['Instance']:

        instance = dict()
        disk = dict()

        # 取回挂载的硬盘信息
        requestDisk = DescribeDisksRequest.DescribeDisksRequest()
        requestDisk.set_InstanceId(item['InstanceId'])   # 关联相关InstanceId
        responseDisk = client.do_action_with_exception(requestDisk)
        jsonDataDisk = json.loads(responseDisk, encoding='utf-8')

        for j in range(jsonDataDisk['TotalCount']):
            disk[jsonDataDisk['Disks']['Disk'][j]['Device']] = jsonDataDisk['Disks']['Disk'][j]['Size']

        # 写入字典
        instance['InstanceId'] = item['InstanceId']
        instance['HostName'] = item['HostName']
        instance['IpAddress'] = item['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
        instance['OSName'] = item['OSName']
        instance['Cpu'] = item['Cpu']
        instance['Memory'] = item['Memory']
        instance['Status'] = item['Status']
        instance['Disks'] = disk

        instances[instance['IpAddress']] = instance  # 组合成大数据

        print(instance)

    print(instances)