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
            'Cookie': '自己的Cookie',
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
