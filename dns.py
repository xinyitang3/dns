#!/usr/bin/env python3
"""
用法：
  python dns.py <域名>          # 单次查询
  python dns.py <IP地址>        # 单次查询
  python dns.py targets.txt               # 批量查询（文件每行一个目标）
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR in sys.path:
    sys.path.remove(SCRIPT_DIR)

import dns.resolver
import requests
import ipaddress

RESOLVER = dns.resolver.Resolver()
RESOLVER.nameservers = ['1.0.0.1', '8.8.4.4']
RESOLVER.timeout = 5
RESOLVER.lifetime = 10

def query_a_record(domain):
    try:
        answers = RESOLVER.resolve(domain, 'A')
        return [str(rdata) for rdata in answers]
    except Exception:
        return []

def reverse_ip_lookup(ip):
    try:
        api_url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200 and "error" not in resp.text.lower():
            return [line.strip() for line in resp.text.splitlines() if line.strip()]
    except Exception:
        pass
    return []

def process_target(target):
    try:
        ipaddress.ip_address(target)
        return reverse_ip_lookup(target)
    except ValueError:
        return query_a_record(target)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python dns.py <目标/文件>")
        sys.exit(1)

    target = sys.argv[1]

    # 批量模式
    if os.path.isfile(target):
        with open(target, 'r', encoding='utf-8') as f:
            items = [line.strip() for line in f if line.strip()]
        for i, item in enumerate(items):
            results = process_target(item)
            # 输出目标标识
            print(f"[{item}]")
            if results:
                print('\n'.join(results))
            else:
                print("(无结果)")
            # 每个目标之间空一行，最后一个不空
            if i != len(items) - 1:
                print()
    else:
        # 单次模式（保持原样）
        results = process_target(target)
        if results:
            print('\n'.join(results))