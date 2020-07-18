https_proxy = []                              # 'https://ip:port'
http_proxy = []                               # 'http://ip:port'


proxy_list = []

if len(http_proxy) != 0:
    for i in range(len(http_proxy)):
        proxy_list.append({"http": http_proxy[i]})
else:
    None

if len(https_proxy) != 0:
    for i in range(len(https_proxy)):
        proxy_list.append({"https": https_proxy[i]})
else:
    proxy_list = None