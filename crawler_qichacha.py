import urllib.request
import urllib.parse
from io import BytesIO
import gzip
from bs4 import BeautifulSoup
import time
import urllib
import json

class crawler_qichacha(object):
    def __init__(self):
        self.items = []
        self.url = 'https://www.qichacha.com/search?key=%E6%BF%80%E5%85%89%E8%B7%9F%E8%B8%AA#p:'
        self.headers = {
            'Host': 'www.qichacha.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.qichacha.com/search?key=%E6%BF%80%E5%85%89%E8%B7%9F%E8%B8%AA',
            'Cookie': 'zg_did=%7B%22did%22%3A%20%2216dcf5b36849-0acc1f866a0e9c8-14377840-100200-16dcf5b36877f%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201574253594295%2C%22updated%22%3A%201574255416742%2C%22info%22%3A%201574226976627%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%22012047e52037bfd103590415c80398e8%22%7D; UM_distinctid=16dcf5b97129-0de9b2548694b1-14377840-100200-16dcf5b97132c; CNZZDATA1254842228=368439251-1571137487-https%253A%252F%252Fwww.baidu.com%252F%7C1574252367; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1574226978,1574245244; _uab_collina=157114198527205044688737; QCCSESSID=r8bmkbqp7ju3dpitkqlm81shg2; acw_tc=7a0e2b1915742269772534926e95a3d3833e1a95f6ff1766dfd587a985; hasShow=1; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1574255416',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        }

    def parse_content(self,content):
        soup = BeautifulSoup(content,'lxml')
        for href in soup.find_all('a' , class_="ma_h1"):
            url_now ='https://www.qichacha.com' + href['href']
            request1 = urllib.request.Request(url = url_now, headers = self.headers)
            buff1 = BytesIO(urllib.request.urlopen(request1).read())
            f = gzip.GzipFile(fileobj=buff1)
            res1 = f.read().decode('utf-8')
            self.parse_content1(res1)

    def parse_content1(self, content):
        soup = BeautifulSoup(content, 'lxml')
        company = soup.select('h1')[0].text
        scope = soup.find_all(attrs={'colspan': '3'})[1].text.strip()
        print(company)
        print(scope)
        item = {
            "公司名称":company,
            "经营范围":scope,
        }
        self.items.append(item)
        time.sleep(4)

    def run(self):
        for i in range(1,6):
            url = self.url + str(i) + '&'
            request = urllib.request.Request(url = url,headers= self.headers)
            response = urllib.request.urlopen(request)
            htmlPage = response.read()
            buff = BytesIO(htmlPage)
            f = gzip.GzipFile(fileobj=buff)
            res = f.read().decode('utf-8')
            self.parse_content(res)
        print(self.items)
        string = json.dumps(self.items, ensure_ascii = False)
        with open ('企查查.txt' , 'w',encoding = 'utf8') as fp:
            fp.write(string)

def main():
    crawler = crawler_qichacha()
    crawler.run()

if __name__ == '__main__':
    main()
