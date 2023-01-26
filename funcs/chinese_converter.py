
import os
import re

## chinese converter (traditional to simplified)
from opencc import OpenCC
import jieba
import jieba.analyse


def convert_wiki_cn(dir, out_dir):
    cc = OpenCC('t2s')
    # get folder list:
    folder_list = os.listdir(dir)
    if '.DS_Store' in folder_list:
        folder_list.remove('.DS_Store')
    for i in folder_list:
        # i = 'AA'
        path = os.path.join(dir, i)
        out_path = os.path.join(out_dir, i)
        os.mkdir(out_path)
        os.chdir(out_path)
        file_list = os.listdir(path)
        if '.DS_Store' in file_list:
            file_list.remove('.DS_Store')
        for file_name in file_list:
            file = os.path.join(path, file_name)
            with open(file, 'r') as f1, open(file_name, 'w') as f2:
                for lines in f1:
                    f2.write(cc.convert(lines))

def cleantext(text):
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, ' ', text)
    text = re.sub(r"[-()\"#/@;:<>{}=~|.?,]", "", text)
    text = re.sub("([^\u4e00-\u9fa5])", " ", text)
    return text

def seperate_sentence(in_dir, out_dir):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    # get folder list:
    folder_list = os.listdir(in_dir)
    if '.DS_Store' in folder_list:
        folder_list.remove('.DS_Store')
    for i in folder_list:
        # i = 'AA'
        path = os.path.join(in_dir, i)
        out_path = os.path.join(out_dir, i)
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        os.chdir(out_path)
        file_list = os.listdir(path)
        if '.DS_Store' in file_list:
            file_list.remove('.DS_Store')
        for file_name in file_list:
            file = os.path.join(path, file_name)
            with open(file, 'r', encoding='utf-8') as f1, open(file_name, 'w', encoding='utf-8') as f2:
                for line in f1:
                    text = cleantext(line)
                    seg_list = jieba.cut(text)
                    f2.write(' '.join(seg_list) + '\n')

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for root, dirs, files in os.walk(self.dirname):
            for filename in files:
                file_path = root + '/' + filename
                if '.DS_Store' in file_path:
                    pass
                else:
                    for line in open(file_path):
                        sline = line.strip()
                        if sline == "":
                            continue
                        sentence = sline.split()
                        yield sentence