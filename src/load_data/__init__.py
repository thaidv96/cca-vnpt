import pandas as pd
import glob
from ..utils import clean_column_name
from tqdm import tqdm
import numpy as np

tqdm.pandas('my_bar!')


def load_historical_dataset(data_fn_pattern, sep='\t'):
    fns = glob.glob(data_fn_pattern)
    dfs = []
    for fn in fns:
        df = pd.read_csv(fn, sep=sep)
        df['period'] = fn.split("_")[-1].split(".")[0]
        dfs.append(df)
    df = pd.concat(dfs)
    df = clean_column_name(df)
    df.period = pd.to_datetime(df.period, format = '%Y%m')
    df.goi_su_dung = df.goi_su_dung.astype(str).replace('0',np.nan)
    df.ngay_kh = pd.to_datetime(df.ngay_kh)
    df = df[df.period >= df.ngay_kh]
    return df

    
def load_dky_goi(fn):
    df = pd.read_csv(fn, encoding='unicode_escape')
    df = clean_column_name(df)
    df.giao_dich = df.giao_dich.map({"Ðãng k?":"Đăng ký","Gia h?n":"Gia hạn"})
    df.ngay = pd.to_datetime(df.ngay, format="%Y%m%d")
    df['period'] = df.ngay - pd.to_timedelta(df.ngay.dt.day - 1, unit='d')
    df = df.groupby(["so_tb",'period']).agg({"goi":list})
    df.columns =['goi_dky']
    df.reset_index(inplace=True)
    return df

def load_mota_goi(fn):
    df = pd.read_excel("../Dataset/Mo_ta_goi.xlsx")
    df = clean_column_name(df)
    return df

def load_dataset(historical_fn_pattern, dky_goi_fn):
    historical_df = load_historical_dataset(historical_fn_pattern)
    dky_df = load_dky_goi(dky_goi_fn)
    df = pd.merge(historical_df, dky_df, on = ['so_tb','period'], how='left')
    df.goi_dky.loc[df.goi_dky.isnull()] = df.goi_dky.loc[df.goi_dky.isnull()].apply(lambda x: [])
    df.progress_apply(lambda row: row.goi_dky.append(row.goi_su_dung) if type(row.goi_su_dung) == str and row.goi_su_dung not in row.goi_dky else None, axis=1)
    return df