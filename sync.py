import os
import shutil
import sys
import time

from lib.logger import Logger
from lib.source import list_dirs, del_root, parser_cmd

args = parser_cmd()
root_src_dir = args.src_path
root_dst_dir = args.dst_path
logger = Logger(args.log_path)
if not os.path.isdir(args.log_path):
    os.mkdir(args.log_path)
    logger.add_log(args.log_path, 1)
if not os.path.isdir(args.src_path):
    logger.add_log('The source is not exist', 3)
    sys.exit()
if not os.path.isdir(args.dst_path):
    os.mkdir(args.dst_path)
    logger.add_log(args.dst_path, 1)


while 1:
    time.sleep(args.time)
    src_arr, dst_arr, del_arr = [], [], []
    del_root(root_src_dir, list_dirs(root_src_dir, src_arr))
    del_root(root_dst_dir, list_dirs(root_dst_dir, dst_arr))
    if dst_arr:  # если клон не новый
        for path_src in src_arr:
            count = len(dst_arr)
            full_path_src = root_src_dir + path_src
            for path_dst in dst_arr:
                full_path_dst = root_dst_dir + path_dst
                # перебираем пути и, если совпало и это новый файл - перезаписываем, если это папка - пропускаем
                if path_src == path_dst:
                    if os.path.isfile(full_path_src):
                        if os.path.getmtime(full_path_src) > os.path.getmtime(full_path_dst):
                            shutil.copy2(full_path_src, root_dst_dir + os.path.split(path_dst)[0])
                            logger.add_log(full_path_dst, 2)
                else:
                    count -= 1
            if count == 0:  # если count=0  - новый путь. Создаем копию файла или папки
                if os.path.isfile(full_path_src):
                    shutil.copy2(full_path_src, root_dst_dir + os.path.split(path_src)[0])
                    logger.add_log(root_dst_dir + path_src, 1)
                else:
                    os.mkdir(root_dst_dir + path_src)
                    logger.add_log(root_dst_dir + path_src, 1)

        for path_dst in dst_arr:  # определяем массив с папками, которые надо удалить из источника
            flag = False
            for path_src in src_arr:
                if path_dst == path_src:
                    flag = True
            if not flag:
                del_arr.append(path_dst)

        for i in range(len(del_arr), 0, -1):  # удаляем из источника папки и файлы
            path = root_dst_dir + del_arr[i - 1]
            if os.path.isfile(path):
                os.remove(path)
                logger.add_log(path, 0)
            else:
                os.rmdir(path)
                logger.add_log(path, 0)

    else:  # если клон новый
        for path in src_arr:
            if os.path.isdir(root_src_dir + path):
                os.mkdir(root_dst_dir + path)
                logger.add_log(root_dst_dir + path, 1)
            else:
                shutil.copy2(root_src_dir + path, root_dst_dir + os.path.split(path)[0])
                logger.add_log(root_dst_dir + path, 1)
