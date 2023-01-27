import os

from funcs.utils import cleantext, file_path_name_generator
from opencc import OpenCC
import jieba
import jieba.analyse

def convert_wiki_cn(dir, out_dir):
    cc = OpenCC('t2s')
    # get folder list:
    for file_path, root, no_root_path, file_name in file_path_name_generator(dir):
        out_root = out_dir + no_root_path + '/'
        out_path = out_root + file_name
        if not os.path.isdir(out_root):
            os.makedirs(out_root)
        with open(file_path, 'r') as f1, open(out_path, 'w') as f2:
            for lines in f1:
                f2.write(cc.convert(lines))
    return


def seperate_sentence(in_dir, out_dir):
    for file_path, root, no_root_path, file_name in file_path_name_generator(in_dir):
        out_root = out_dir + no_root_path + '/'
        out_path = out_root + file_name
        if not os.path.isdir(out_root):
            os.makedirs(out_root)
        with open(file_path, 'r', encoding='utf-8') as f1, open(out_path, 'w', encoding='utf-8') as f2:
            for line in f1:
                text = cleantext(line)
                seg_list = jieba.cut(text)
                f2.write(' '.join(seg_list) + '\n')
    return

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for file_path, root, no_root_path, file_name in file_path_name_generator(self.dirname):
            for line in open(file_path):
                sline = line.strip()
                if sline == "":
                    continue
                sentence = sline.split()
                yield sentence