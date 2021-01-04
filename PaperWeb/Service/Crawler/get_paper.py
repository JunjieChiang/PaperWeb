import requests
from bs4 import BeautifulSoup
import traceback
import csv

# from PaperWeb.Service.Utils.requests import get_http_session

"""
IP池:多个IP取爬取B站
避免因同一个IP多次请求B站而被B站封杀
"""
def get_http_session(pool_connections=5, pool_maxsize=10, max_retries=10):       # http连接池
    requests.packages.urllib3.disable_warnings()
    session = requests.session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,       # 适配器
                                           pool_maxsize=pool_maxsize,
                                           max_retries=max_retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def gen_papers(skip):
    try:
        url = f"https://arxiv.org/list/cs/pastweek?skip={skip}&show=100"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        # ip代理(国外网站爬取速度较慢因此需要进行代理ip)
        """
        proxies = {
 
        }
        """

        r = get_http_session().get(url, headers=headers)
        if r.status_code != 200:
            return False, "请求网页失败!"
        else:
            soup = BeautifulSoup(r.text, "lxml")        # 解析速度快

        all_dt = soup.find_all("dt")    # 论文url
        all_dd = soup.find_all("dd")    # 论文标题与作者

        for dt, dd in zip(all_dt, all_dd):              # 找出url, title, author
            url = dt.find(class_="list-identifier").find("a").get("href")
            root_url = "https://arxiv.org"
            whole_url = root_url + url

            title = dd.find(class_="list-title mathjax").contents       # 返回的是一个list
            if len(title) >= 3:
                title = title[2]
            else:
                title = dd.find(class_="list-title mathjax").text       # 返回的是一个str

            authors = dd.find(class_="list-authors").text
            authors = authors.split(":")[1].replace("\n", "")

            yield title, whole_url, authors

    except Exception as e:
        print(e)        # 打印报错
        traceback.print_exc()


def main():
    resl = []
    for i in range(0, 1453, 100):
        for title, whole_url, authors in gen_papers(i):
            resl.append([title, whole_url, authors])
            print(title, "done!")

        with open("paper.csv", "w", encoding="utf-8", newline="") as f:             # nerline防止csv文件出现空行
            cw = csv.writer(f)      # 打开文件
            for i in resl:
                # 写一行
                cw.writerow(i)


if __name__ == "__main__":
    main()
