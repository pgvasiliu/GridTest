"""
花式网格策略 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx719

1、批量读取文件名，并按照币种对文件名进行分组
2、按照币种去读取文件，合成币种信息（这样做的好处是占用的内存小）
"""
from multiprocessing import cpu_count, Pool
from program.Function import *


def read_candle_data(file_path):
    """
    读取币种的K线数据
    :param file_path:
    :return:
    """
    print(file_path)
    # 获取币种的名字
    symbol = os.path.basename(file_path).replace('_1m.csv', '')
    # 读取数据
    df = pd.read_csv(file_path, encoding='gbk', skiprows=1, parse_dates=['candle_begin_time'])
    df['symbol'] = symbol

    # 删除不必要的数据，省的文件太大
    # df.drop(columns=['volume', 'quote_volume', 'trade_num', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume'],
    #     inplace=True)
    return df


if __name__ == '__main__':
    # 获取所有1分钟K线数据的文件路径
    file_path_list = get_code_list_in_one_dir(candle_raw_path, end_with='1m.csv')
    # file_path_list = file_path_list[:10]
    print(file_path_list)

    # 将K线的文件路径转为DataFrame
    file_path_df = pd.DataFrame(file_path_list)
    file_path_df['symbol'] = file_path_df[0].apply(lambda x: os.path.basename(x).replace('_1m.csv', ''))

    # 批量读取K线数据
    # start_time = datetime.datetime.now()
    # 并行或串行读取数据
    multiply_process = False
    # 挨个币种读取数据，这样做的好处是可以避免内存不足。
    group = file_path_df.groupby('symbol')
    for coin, data in group:
        print('\n', coin)
        coin_fr_path = candle_fd_path + coin.replace('-', '') + '.csv'
        if not os.path.exists(coin_fr_path):
            print(coin, ':不存在资金费率数据')
            continue

        # 币种路径合集
        coin_path_list = data[0].to_list()
        if multiply_process:
            # 开始并行
            with Pool(max(cpu_count() - 2, 1)) as pool:
                df_list = pool.map(read_candle_data, sorted(coin_path_list))
        else:
            df_list = []
            for fp in coin_path_list:
                data = read_candle_data(fp)
                df_list.append(data)
        # 合并数据
        coin_data = pd.concat(df_list, ignore_index=True)
        # 数据整理
        coin_data.sort_values('candle_begin_time', inplace=True)
        coin_data.reset_index(inplace=True, drop=True)
        # 读取资金费率数据
        fr_data = pd.read_csv(coin_fr_path, encoding='gbk', skiprows=1, parse_dates=['time'])
        coin_data = pd.merge(left=coin_data, right=fr_data[['time', 'fundingRate']], left_on=['candle_begin_time'],
                             right_on=['time'], how='left')
        del coin_data['time']
        # 保存数据
        coin_data.to_pickle(candle_path + '%s.pkl' % coin)