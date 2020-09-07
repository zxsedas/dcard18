import requests
import json
from bs4 import BeautifulSoup
import os

class dcard_sex():
    
    def __init__(self,number,articles):
        self.url = 'https://www.dcard.tw/service/api/v2/forums/sex/posts?popular=true&limit='
        self.room = 'https://www.dcard.tw/f/sex/p/'
        self.count = 0
        self.before = ''
        self.number = number
        self.articles = articles

    def scrape(self):
        srcs = list()
        datas = list()
        i = 1
        url = self.url + str(self.articles)
        print(url)
        for i in range(self.number):
            response = requests.get(url)
            jcs = json.loads(response.text)
            

            for jc in jcs:
                if jc["gender"] == "F":
                    #print(jc["title"],jc["id"]) 
                    datas.append((jc["title"].replace("#",""),str(jc["id"]),))
                    
            self.before = '&before=' + str(jc["id"])
            url =  self.url + str(self.articles) + self.before

        
        for data in datas:
            room = requests.get(self.room + data[1])
            soup = BeautifulSoup(room.text,"lxml")
            imgs = soup.find_all("img",{"class":"sc-1iqzwcj-0 frUOHl"})
            if imgs:
                for img in imgs:
                    
                    srcs.append(img["src"])            
        return srcs
    
    def img_save(self,srcs):
        if not os.path.exists('imgslib'):
            os.mkdir('imgslib')

        for src in srcs:
            self.count += 1
            img_b = requests.get(src).content
            with open(f'imgslib/{self.count}.png','wb') as fout:
                fout.write(img_b)
        

            
        
b = dcard_sex(2,100)
import time
t = time.time()
result = b.scrape()
b.img_save(result)

print(time.time()-t)