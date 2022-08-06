"""
花式网格船队 第1期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx719
"""
import os
import pandas as pd

csv_path = 'D:/Data/Coin/swap_candle_1m/'  # 读取CSV文件的路径
pkl_path = 'D:/Data/Coin/swap_candle_1m_pkl/'  # 保存PKL文件的路径，要用pkl文件还要修改config里面的candle_path

file_list = os.listdir(csv_path)
file_list = [f for f in file_list if '.csv' in f]

for file in file_list:
    print(file)
    df = pd.read_csv(csv_path + file, encoding='gbk', parse_dates=['candle_begin_time'], skiprows=1)
    df.to_pickle(pkl_path + file.replace('csv', 'pkl'))
