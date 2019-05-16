from shutil import rmtree
from os import path, makedirs


def make_dir_nx(p: str):
    folder = path.exists(p)
    if not folder:
        makedirs(p)


def rm_dir_f(path: str):
    rmtree(path)


def print_step(info: str):
    print(f'........{info}........')


def add_number_file_name(path: str, i: int = 1) -> str:
    paths = path.split('.')
    name_int = int(paths[0]) + i
    return str(name_int) + '.' + paths[1]
