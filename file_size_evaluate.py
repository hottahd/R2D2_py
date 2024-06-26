# -*- coding: utf-8 -*-
# run以下のディレクトリのサイズを計算し、filesize.txtに保存する

import R2D2
import os

# ../run/以下のディレクトリを自動で取得
base_path = '../run'
#directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
directories = sorted([d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])

results_file_path = '../run/filesize.txt'

# ディレクトリサイズの計算と結果の保存
for caseid in directories:
    print(caseid)
    dir_path = os.path.join(base_path, caseid)
    total_size, unit = R2D2.util.get_total_file_size(dir_path)
    R2D2.util.update_results_file(results_file_path, total_size, unit, caseid, dir_path)
