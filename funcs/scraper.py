import numpy as np
import pandas as pd

## libs for scraping and storing data
import requests
import csv
from bs4 import BeautifulSoup

## cookie need to be updated manually because of the new login requirement of Douban
cookie = 'push_doumail_num=0; push_noty_num=0; _vwo_uuid_v2=DAAEF2DB6070490F44837287B7D3D797C|75b8cb11e0d9a6bbf28b5ee9b67a20a8; __utma=30149280.526420392.1673120562.1673120562.1673480474.2; __utmb=30149280.29.10.1673480474; __utmc=30149280; __utmv=30149280.2597; __utmz=30149280.1673120562.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.488996994.1673480474.1673480474.1673480474.1; __utmb=223695111.0.10.1673480474; __utmc=223695111; __utmz=223695111.1673480474.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=3941380d5373def8.1673480474.1.1673481310.1673480474.; _pk_ses.100001.4cf6=*; __utmt=1; __utmt_douban=1; frodotk_db="be0943d1a2339aaa3a1bcb74e69acffe"; ap_v=0,6.0; ck=7eSj; dbcl2="25977271:W1EkFloTu78"; ll="108258"; bid=rX6WylNFHYI'
file_path = 'comment_data.csv'

class CollectComments:
    def __init__(self, cookie, file_path):
        self.url = 'https://movie.douban.com/subject/34444648/comments?start={}&limit=20&status=P&sort=new_score'
        self.url_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
                           'Cookie': cookie}
        self.file_path = file_path
        
    def get_url_list(self, N=29):
        url_list = []
        for i in range(N):
            url_list.append(self.url.format(i * 20))
        return url_list
    
    def get_comment(self, url):
        ## need to have a way of checking response.
        resp = requests.get(url=url, headers=self.url_header)
        soup = BeautifulSoup(resp.text, 'lxml')
        node = soup.select('.comment-item')
        content = []
        for i in node: 
            name = i.a.get('title')
            star = i.select_one('.comment-info').select('span')[1].get('class')[0][-2]
            time = i.select_one('.comment-time').get('title')
            comment = i.select_one('.short').text
            votes = i.select_one('.votes').text
            content.append([name, star, time, votes, comment])
        return content
    
    def write_content_to_csv(self, content, file_path):
        with open(file_path, 'a+', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerows(content)
    
    def run(self):
        url_list = self.get_url_list()
        csv_header = ['name', 'star', 'time', 'votes', 'comment']
        f = open(self.file_path, 'w')
        w = csv.writer(f)
        w.writerow(csv_header)
        f.close()
        
        for url in url_list:
            content = self.get_comment(url)
            self.write_content_to_csv(content, self.file_path)
        
        print('done')
        
