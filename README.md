# DNS 查询工具

一个简单的 Python 命令行工具，支持 DNS A 记录查询和 IP 反向域名查询（通过第三方 API），自动识别输入类型，支持批量处理。

## 特性

- 🎯 自动识别：输入域名则查询 A 记录（IPv4），输入 IP 则反查关联域名。
- 📁 批量处理：将目标写入文本文件（每行一个），一键批量查询。
- 🌐 自定义 DNS：使用 Cloudflare (`1.0.0.1`) 和 Google (`8.8.4.4`) 的公共 DNS，避免本地超时。
- 📡 IP 反查：基于 [HackerTarget](https://hackertarget.com/) 免费 API，获取同一 IP 上绑定的域名。
- 📦 无额外格式：单次查询直接输出结果（每行一个），批量查询带目标标记和分隔。

## 安装依赖

```bash
pip install dnspython requests
```

## 用法

### 单次查询

```bash
# 查询域名的 A 记录
python dns.py <域名>

# 查询 IP 上关联的域名
python dns.py <IP地址>
```

输出示例（域名查询）：
```
<返回的IP地址1>
<返回的IP地址2>
```

输出示例（IP 反查）：
```
<关联域名1>
<关联域名2>
<关联域名3>
...
```

### 批量查询

将目标（域名或 IP，每行一个）放入文件，例如 `targets.txt`：

```
<目标1>
<目标2>
<目标3>
```

运行：

```bash
python dns.py targets.txt
```

输出示例：
```
[<目标1>]
<结果1>
<结果2>
...

[<目标2>]
<结果3>
<结果4>
...

[<目标3>]
(无结果)
```

> 批量模式每个目标前会显示 `[目标名]`，无结果时显示 `(无结果)`，目标之间用空行分隔。

## 依赖

- Python 3.6+
- [dnspython](https://pypi.org/project/dnspython/)：DNS 解析
- [requests](https://pypi.org/project/requests/)：HTTP 请求（用于 IP 反查 API）

## 注意事项

- IP 反查使用免费的 [HackerTarget Reverse IP Lookup API](https://api.hackertarget.com/reverseiplookup/)，有每日查询次数限制（约 20-50 次），大量查询请合理控制频率。
- 部分 IP（尤其是 CDN 节点或动态 IP）可能查不到关联域名，属于正常现象。
- 脚本默认使用公共 DNS `1.0.0.1` 和 `8.8.4.4`，可在代码中修改 `RESOLVER.nameservers` 换成其他 DNS。
