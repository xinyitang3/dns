# DNS 查询工具

一个简单的 Python 命令行工具，支持 DNS A 记录查询和 IP 反向域名查询，自动识别输入类型，支持批量处理。

## 特性

- 🎯 自动识别：输入域名则查询其全部 **A 记录（IPv4）**，输入 IP 则反查同 IP 关联的域名。
- 📁 批量处理：将域名或 IP 写入文本文件（每行一个），一键批量查询，输出带标记和分隔。
- ☁️ Cloudflare DoH：通过 [Cloudflare DNS-over-HTTPS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/) 公共接口查询，无需本地 DNS 解析器，避免缓存和截断，确保获取完整 A 记录。
- 🧩 网页抓取反查：IP 反查基于 [site.ip138.com](https://site.ip138.com/) 公开页面，提取历史上绑定的域名。
- 📦 简洁输出：单次查询每行一个结果，批量查询带 `[目标]` 标记，无结果显示 `(无结果)`。

## 安装依赖

```bash
pip install requests
```

> 需要 Python 3.6+，`ipaddress` 和 `re` 均为内置模块，无需额外安装。

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
<返回的IP地址>
```

输出示例（IP 反查）：

```
<关联域名1>
<关联域名2>
<关联域名3>
...
```

### 批量查询

创建一个文本文件，例如 `targets.txt`，每行一个 **域名** 或 **IP 地址**：

```
<域名>
<IP地址>
<另一个域名或IP>
```

运行：

```bash
python dns.py targets.txt
```

输出示例：

```
[<域名>]
<返回的IP地址>

[<IP地址>]
<关联域名1>
<关联域名2>
...

[<另一个域名或IP>]
(无结果)
```

> 批量模式下，每个域名或 IP 前会显示 `[名称]`，无结果时显示 `(无结果)`，各条目之间用空行分隔。

## 工作原理

- **域名 → A 记录**：向 `https://cloudflare-dns.com/dns-query` 发送 DoH JSON 查询（类型 `A`），从响应中提取所有 `Answer` 中 `type=1` 的 IP 地址，去重后排序输出。
- **IP → 域名列表**：访问 `https://site.ip138.com/<IP>/`，用正则表达式提取页面中 `<ul id="list">` 内的 `<a>` 标签文本，得到同 IP 历史绑定的域名。

## 注意事项

- IP 反查结果为 `site.ip138.com` 的记录，可能包含已过期或不再解析的域名，仅供参考。
- 若目标网站修改页面结构，反查功能可能失效，届时需要调整正则表达式。
- Cloudflare DoH 为免费公共服务，一般无速率限制，但大量查询请保持合理间隔。
- 脚本开头已处理文件名 `dns.py` 与 `dns` 模块的导入冲突，可放心使用该文件名。

## 依赖

- Python 3.6+
- [requests](https://pypi.org/project/requests/)
