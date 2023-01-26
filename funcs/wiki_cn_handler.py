import os

def file_path_name_generator(dir):
    for root, dirs, files in os.walk(dir):
        for file_name in files:
            file_path = root + '/' + file_name
            if '.DS_Store' in file_path:
                pass
            else:
                yield file_path, file_name