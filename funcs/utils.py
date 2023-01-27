import re
import os

def cleantext(text):
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, ' ', text)
    text = re.sub(r"[-()\"#/@;:<>{}=~|.?,]", "", text)
    text = re.sub("([^\u4e00-\u9fa5])", " ", text)
    return text

def file_path_name_generator(dir):
    for root, dirs, files in os.walk(dir):
        for file_name in files:
            file_path = root + '/' + file_name
            no_root_path = root.replace(dir, '')
            if '.DS_Store' in file_path:
                pass
            else:
                yield file_path, root, no_root_path, file_name