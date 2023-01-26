import numpy as np
import pandas as pd

## libs for initial analysis
import matplotlib.pyplot as plt
import jieba
import jieba.analyse
from wordcloud import WordCloud
from collections import Counter

def pie_chart(df):
    score = dict(df['star'].value_counts(dropna=False))
    count = len(df)
    
    ## percentage of each category
    size = {} 
    explode = {}  
    
    ## calculate percentages
    for i in range(1, 6):  
        size[str(i)] = score[str(i)] * 100 / count
        explode[str(i)] = score[str(i)] / count / 10
    
    ## setup for pie chart
    label = '1分', '2分', '3分', '4分', '5分'
    color = 'blue', 'orange', 'yellow', 'green', 'red' 
    pie = plt.pie(size.values(), colors=color, explode=explode.values(), labels=label, shadow=True, autopct='%1.1f%%')
    for font in pie[1]:
        font.set_size(8)
    for digit in pie[2]:
        digit.set_size(8)
    plt.axis('equal')  
    plt.title(u'各个评分占比', fontsize=12)  
    plt.legend(loc=0, bbox_to_anchor=(0.82, 1))  
    ## setup legend font
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=6)
    plt.savefig("score.png")
    plt.show()
    
def word_frequency_counter(df, stopword):
    commentstr = '' 
    c = Counter()  
    index = 0
    for i in df['comment']:
        seg_list = jieba.cut(i,cut_all=False )
        index += 1
        for x in seg_list:
            if len(x)>1 and x != '\r\n':
                try:
                    c[x] += 1
                except:
                    continue
        commentstr += i
    
    ## screen out stop words and word_frequency<5
    for (k, v) in c.most_common():  
        if v < 5 or k in stopword:
            c.pop(k)
            continue
    return c

def counter_to_lists(map, N):
    ## get the word_list and corresponding frequency list
    x = []
    y = []
    for (k, v) in map.most_common(N):
        x.append(k)
        y.append(v)
    return x, y

def histo(map):
    x, y = counter_to_lists(map, 15)
    width = .6
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(figsize=(8,6))
    plt.bar(x, y, width, color='blue', label='热门词频统计', alpha=.8)
    
    plt.xlabel('高频词')
    plt.ylabel('次数')
    plt.savefig('histo.png')
    plt.show()
    
def word_cloud(map):
    FONT_PATH = "STHeiti Medium.ttc"
    x, y = counter_to_lists(map, 300)
    ci = x[:150]
    ci = ' '.join(ci)
    wc = WordCloud(background_color="white",
                   width=1500, height=1200,
                   # min_font_size=40,
                   # mask=backgroud_Image,
                   font_path=FONT_PATH,
                   max_font_size=150,  # 设置字体最大值
                   random_state=50,  # 设置有多少种随机生成状态，即有多少种配色方案
                   )
    my_wordcloud = wc.generate(ci)
    plt.imshow(my_wordcloud)
    plt.axis('off')
    my_wordcloud.to_file('wordcloud.jpg')