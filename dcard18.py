import requests
from bs4 import BeautifulSoup
import json

class dcard_sex():
    """
    data['title']#各篇文章標題
    data['id']#id編號
    data['gender']#性別
    """
    def __init__(self,count,number):
        self.url="https://www.dcard.tw/service/api/v2/forums/sex/posts?popular=true&limit="
        self.count=count
        self.number=number
        self.j=0
        self.i=0
        self.times=-1
    def titles_article_img(self):
        data=requests.get(self.url+str(self.number))
        data_json=json.loads(data.text)
        while self.count>0:
            for data in data_json:
                if self.i>1:
                    url_article="https://www.dcard.tw/f/sex/p/"+str(data['id'])
                    print(data['title'],data['id'],data["gender"],url_article,"  ",self.times)
                    if data['gender'] == "F":
                        self.crawl_img(url_article)
                self.times+=1
                self.i+=1
            url_article="https://www.dcard.tw/service/api/v2/forums/sex/posts?popular=true&limit="+str(self.number)+"&before="+str(data['id'])
            data=requests.get(url_article)
            data_json=json.loads(data.text)
            self.count-=1

    def crawl_img(self,url_article):
        sex_content=requests.get(url_article)
        soup1=BeautifulSoup(sex_content.text,"html.parser")
        imgs=soup1.select("article div img")
        #print(imgs)
        for img in imgs:
            #print(img["src"],self.j)
            pic=requests.get(img["src"])
            sex_img=pic.content
            pic_out=open("imglib/{}.png".format(self.j),"wb")
            pic_out.write(sex_img)
            self.j+=1
            pic_out.close()


tom=dcard_sex(3,5)
tom.titles_article_img()


            


    