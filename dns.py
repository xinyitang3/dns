#!/usr/bin/env python3
"""
用法：
  python dns.py <域名>          # 查询域名的全部 A 记录（Cloudflare DoH JSON）
  python dns.py <IP地址>        # IP 反查域名（site.ip138.com）
  python dns.py targets.txt     # 批量查询
"""
import sys
import os

# 解决 dns.py 自身名与包冲突
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR in sys.path:
    sys.path.remove(SCRIPT_DIR)
if '' in sys.path:
    sys.path.remove('')

import re
import requests
import ipaddress
import json

CF_DNS_URL = "https://cloudflare-dns.com/dns-query"


def query_a_record(domain):
    """通过 Cloudflare DoH JSON 接口获取域名的全部 A 记录 IP"""
    try:
        resp = requests.get(
            CF_DNS_URL,
            params={"name": domain, "type": "A"},
            headers={"Accept": "application/dns-json"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("Status") != 0:
            return []
        answers = data.get("Answer", [])
        # 收集所有 type 1 (A) 的 IP
        ips = [ans["data"] for ans in answers if ans.get("type") == 1]
        return sorted(set(ips))
    except Exception:
        return []


def reverse_ip_lookup(ip):
    """通过 site.ip138.com 获取 IP 上绑定的域名列表"""
    try:
        url = f"https://site.ip138.com/{ip}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return []
        html = resp.text
        # 提取 <ul id="list"> 中的内容
        list_match = re.search(r'<ul[^>]*id="list"[^>]*>(.*?)</ul>', html, re.DOTALL)
        if not list_match:
            return []
        list_html = list_match.group(1)
        domains = re.findall(r'<a[^>]*>([^<]+)</a>', list_html)
        return [d.strip() for d in domains if d.strip()]
    except Exception:
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

    if os.path.isfile(target):
        with open(target, 'r', encoding='utf-8') as f:
            items = [line.strip() for line in f if line.strip()]
        for i, item in enumerate(items):
            results = process_target(item)
            print(f"[{item}]")
            print('\n'.join(results) if results else "(无结果)")
            if i != len(items) - 1:
                print()
    else:
        results = process_target(target)
        print('\n'.join(results) if results else "(无结果)")