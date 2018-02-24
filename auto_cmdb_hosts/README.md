# 简介
hosts.py 基于Python2.7开发，主要用来动态生成Ansible Intentory 列表。

> 主要功能有：
> * 通过--list 参数，将CMDB采集到的主机信息，动态生成Ansible Inventory 列表
> * 通过--host 参数，查看CMDB采集的主机信息

# 环境依赖
* Python2.7
* Ansible
* PyMysql

# 使用方法
* chmod +x hosts.py
* ansible webserver -i hosts.py -m shell -a 'uptime'
