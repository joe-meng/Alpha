# -- coding: utf-8 --
import os
import sys

new_path_list = os.path.abspath(__file__).split(os.sep)
while True:
    if new_path_list[-1] == 'src':
        break
    else:
        new_path_list = new_path_list[:-1]


new_lib_path = os.sep.join(new_path_list+['workers', 'calculation'])
sys.path.append(new_lib_path)
sys.path.append(os.sep.join(new_path_list))