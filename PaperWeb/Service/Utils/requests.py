import requests

"""
IP池:多个IP取爬取B站
避免因同一个IP多次请求B站而被B站封杀
"""
def get_http_session(pool_connections=2, pool_maxsize=10, max_retries=3):       # http连接池
    session = requests.session()
    adapter = requests.adapter.HTTPAdapter(pool_connections=pool_connections,       # 适配器
                                           pool_maxsize=pool_maxsize,
                                           max_retries=max_retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session