"""
花式网格船队 第1期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx719
"""
from program.Function import *


def df_2_md(data, drop_index=False):
    header = '| |'
    split_line = '|----|'
    if drop_index:
        header = '|'
        split_line = '|'
    for c in data.columns:
        header += ('%s|' % c)
        split_line += '----|'
    rows = []
    for i in data.index:
        line = '|%s|' % i
        if drop_index:
            line = '|'
        for c in data.columns:
            line += '%s|' % data.at[i, c]
        rows.append(line)
    text = header + '\n'
    text += split_line + '\n'
    for r in rows:
        text += r + '\n'
    return text


factor_str_info = factor_info_to_str(factors)
evaluate_df = pd.read_csv(root_path + '/data/回测结果/回测指标_%s.csv' % factor_str_info, encoding='gbk')
evaluate_df.rename(columns={'Unnamed: 0': '回测', '0': '指标'}, inplace=True)

equity_df = pd.read_csv(root_path + '/data/回测结果/回测评价_%s.csv' % factor_str_info, encoding='gbk')
equity_df = equity_df[['candle_begin_time', 'symbol', '当周期涨跌幅']]

pro_max = equity_df.sort_values('当周期涨跌幅', ascending=False).head(5)
pro_min = equity_df.sort_values('当周期涨跌幅', ascending=True).head(5)

pro_max['当周期涨跌幅'] = pro_max['当周期涨跌幅'].apply(lambda x: str(round(100 * x, 2)) + '%')
pro_min['当周期涨跌幅'] = pro_min['当周期涨跌幅'].apply(lambda x: str(round(100 * x, 2)) + '%')

tx_evaluate = df_2_md(evaluate_df, drop_index=True)
tx_evaluate = tx_evaluate.replace(':00:00', '点')

tx_pro_max = df_2_md(pro_max, drop_index=True)
tx_pro_min = df_2_md(pro_min, drop_index=True)

with open(root_path + '/program/发帖脚本/样本模板.txt', 'r', encoding='utf8') as file:
    bbs_post = file.read()
    bbs_post = bbs_post % (tx_evaluate, tx_pro_max, tx_pro_min)
    print(bbs_post)
