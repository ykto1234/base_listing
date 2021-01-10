import configparser
import pandas as pd

def read_config(section):
    # coding: utf-8
    # --------------------------------------------------
    # iniファイルの読み込み
    # --------------------------------------------------
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')

    return config_ini[section]

def read_item_list(file_path, sheet_name, header_idx, cols):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_idx, usecols=cols)
    # データフレームから空白の値を含む行を削除する
    #df_formatted = df.dropna(how='all', axis=0)
    # 商品名と商品価格がNaNの行は削除する
    df_formatted = df.dropna(subset=['商品名','商品価格'])
    df_ret = df_formatted.fillna('')
    return df_ret


