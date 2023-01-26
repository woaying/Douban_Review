import numpy as np
import pandas as pd

## libs for scraping and storing data
import requests
import csv
from bs4 import BeautifulSoup

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
        
