#!/usr/bin/env python
#_*_ coding: UTF8 _*_
from __future__ import print_function
import argparse
import json
from collections import defaultdict
from contextlib import contextmanager
import pymysql


def to_json(in_dict):
    return json.dumps(in_dict, sort_keys=True, indent=2)


@contextmanager
def get_conn(**kwargs):
    conn = pymysql.connect(**kwargs)
    try:
        yield conn
    finally:
        conn.close()


def parse_args():
    parser = argparse.ArgumentParser(description='OpenStack Inventory Module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='List active servers')
    group.add_argument('--host', help='List details about the specific host')

    return parser.parse_args()


def list_all_hosts(conn):
    hosts = defaultdict(list)

    with conn as cur:
        cur.execute('select name,private_ip,os,lab from server_device')
        rows = cur.fetchall()
        for row in rows:
            name, private_ip, os, lab = row
            hosts[lab].append(private_ip)

    return hosts


def get_host_detail(conn, private_ip):
    details = {}
    with conn as cur:
        cur.execute("select name,private_ip,os,lab from server_device where private_ip='{0}'".format(private_ip))
        rows = cur.fetchall()
        if rows:
            name, private_ip, os, lab = rows[0]
            details.update(HostName=name, HostOS=os, HostRole=lab)
    return details


def main():
    parser = parse_args()
    with get_conn(host='192.168.0.104', user='wt', passwd='123456', db='opencmdb') as conn:
        if parser.list:
            hosts = list_all_hosts(conn)
            print(to_json(hosts))
        else:
            details = get_host_detail(conn, parser.host)
            print(to_json(details))


if __name__ == '__main__':
    main()
