import requests
from bs4 import BeautifulSoup
import json
import os
import time
from concurrent import futures
import sys
"""
dcard_sex(爬取次數,爬取文章篇數)
titles_article_img()#爬取圖片方法
#執行範例 python ./dcard18.py 10
"""
class dcard_sex():
    """
    data['title']#各篇文章標題
    data['id']#id編號
    data['gender']#性別
    """
    def __init__(self,count, limit_number):
        self.url = "https://www.dcard.tw/service/api/v2/forums/sex/posts?popular=true&limit="
        self.count = count
        self.limit_number = limit_number
        self.j = 0
        self.i = 0
        self.times = -1
    def titles_article_img(self):
        data = requests.get(self.url + str(self.limit_number))
        data_json_content = json.loads(data.text)

        while self.count > 0:
            for data in data_json_content:
                if self.i > 1:
                    article_id_url = "https://www.dcard.tw/f/sex/p/"+str(data['id'])
                    print(data['title'],data['id'],data["gender"],article_id_url,"  ", self.times)

                    if data['gender'] == "F":#F=Female
                        self.crawl_img(article_id_url)
                self.times+=1
                self.i+=1
            
            url_article_before = self.url + str(self.limit_number) + "&before=" + str(data['id'])
            article_content_before = requests.get(url_article_before).text
            data_json_content = json.loads(article_content_before)

            self.count-=1

    def crawl_img(self,url_article):
        sex_content = requests.get(url_article)
        sex_soup = BeautifulSoup(sex_content.text, "html.parser")
        imgs = sex_soup.select("article div img")      

        if os.path.exists('imglib'):  
            for img in imgs:
                #print(img["src"],self.j)
                pic=requests.get(img["src"])
                sex_img = pic.content
                with open("imglib/{}.png".format(self.j), "wb") as pic:
                    pic.write(sex_img)
                    self.j += 1
                    pic.close()
        else:
            print("建立imglib資料夾\n")
            os.mkdir('imglib')


def use_process(obj,workers):
    t1 = time.time()
    with futures.ProcessPoolExecutor(workers) as pex:
        pex.map(obj.titles_article_img())
    t2 = time.time()
    print(f"Using {workers} workers 耗時{t2 - t1} seconds")

if __name__ == '__main__':
    tom=dcard_sex(1,10)
    worker = int(sys.argv[1])
    use_process(tom,worker)





            


    