import argparse
import os


def list_dirs(root_dir, arr):
    for name in os.listdir(root_dir):
        dir_name = os.path.join(root_dir, name)
        arr.append(dir_name)
        if os.path.isdir(dir_name):
            list_dirs(dir_name, arr)
    return arr


def del_root(root_dir, arr):
    for i in range(0, len(arr)):
        arr[i] = arr[i][len(root_dir):]
    return arr


def parser_cmd():
    parser = argparse.ArgumentParser(description='Synchronisation of directories and files')
    parser.add_argument('src_path', type=str, help='Sourse DIR for synchronisation')
    parser.add_argument('dst_path', type=str, help='Destination DIR for synchronisation')
    parser.add_argument('log_path', type=str, help='Destination DIR for synchronisation')
    parser.add_argument('time', type=int, help='Time in sec for synchronisation')
    arg = parser.parse_args()
    return arg
