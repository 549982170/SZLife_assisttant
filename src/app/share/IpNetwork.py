# coding:utf-8
#!/user/bin/python
'''
Created on 2017年6月21日
@author: yizhiwu
判断网络的网段是否相同
'''

import struct
import socket

''''' 
 转换为子网地址,并检验和输出正确的子网地址 
 192.168.2.1 -> 192.168.2.1/255.255.255.255 
 192.168.2.1/24 -> 192.168.2.0/255.255.255.0 
 192.168.2.1/255.255.255.0 -> 192.168.2.0/255.255.255.0 
 '''


def format_subnet(subnet_input):
    # 如果输入的ip，将掩码加上后输出
    if subnet_input.find("/") == -1:
        return subnet_input + "/255.255.255.255"
    else:
        # 如果输入的是短掩码，则转换为长掩码
        subnet = subnet_input.split("/")
        if len(subnet[1]) < 3:
            mask_num = int(subnet[1])
            last_mask_num = mask_num % 8
            last_mask_str = ""
            for _ in range(last_mask_num):
                last_mask_str += "1"
            if len(last_mask_str) < 8:
                for _ in range(8 - len(last_mask_str)):
                    last_mask_str += "0"
            last_mask_str = str(int(last_mask_str, 2))
            if mask_num / 8 == 0:
                subnet = subnet[0] + "/" + last_mask_str + "0.0.0"
            elif mask_num / 8 == 1:
                subnet = subnet[0] + "/255." + last_mask_str + ".0.0"
            elif mask_num / 8 == 2:
                subnet = subnet[0] + "/255.255." + last_mask_str + ".0"
            elif mask_num / 8 == 3:
                subnet = subnet[0] + "/255.255.255." + last_mask_str
            elif mask_num / 8 == 4:
                subnet = subnet[0] + "/255.255.255.255"
            subnet_input = subnet
            # 计算出正确的子网地址并输出
        subnet_array = subnet_input.split("/")
        subnet_true = socket.inet_ntoa(struct.pack("!I", struct.unpack("!I", socket.inet_aton(subnet_array[0]))[0] & struct.unpack("!I", socket.inet_aton(subnet_array[1]))[0])) + "/" + subnet_array[1]
        return subnet_true


def ip_in_subnet(ip, subnet):
    """判断ip是否属于某个网段"""
    subnet = format_subnet(str(subnet))
    subnet_array = subnet.split("/")
    ip = format_subnet(ip + "/" + subnet_array[1])
    return ip == subnet

if __name__ == "__main__":
    print (ip_in_subnet("192.168.2.252", "192.168.0.0/255.255.0.0"))
    print (ip_in_subnet("192.168.2.252", "192.168.3.0/255.255.255.0"))
    print (ip_in_subnet("192.168.2.252", "192.168.2.0/23"))
    print (ip_in_subnet("192.168.2.252", "192.168.2.0/29"))
    print (ip_in_subnet("192.168.2.2", "192.168.2.2"))
    print (ip_in_subnet("192.168.2.2", "192.168.2.3"))
