#!/usr/bin/env python3
import os
from datetime import date
from pathlib import Path

import pandas as pd
import sys


def load(path: Path, d: date, sex: str) -> pd.DataFrame:
    print(f"Loading input file {path}")
    df = pd.read_excel(
        path,
        header=2
    )

    # rename the columns to NUTS? code
    column_mapping = {}
    for col in df.columns:
        parts = col.split('\n')
        nuts, name = parts[0], ' '.join(parts[1:])
        column_mapping[col] = nuts
    df = df.rename(column_mapping, axis='columns').rename({'Věk': 'age'}, axis='columns')
    # drop columns with missing values (rows bellow header)
    df = df.dropna()

    # drop the first row with total sum
    df = df.iloc[1:]
    # drop the last row with average
    df = df.drop(df[df.age.str.contains('Average')].index)

    # add extra columns to make it clear what type of data is there
    df['sex'] = sex
    df['date'] = d.isoformat()

    # set index
    df = df.set_index(['date', 'sex', 'age'])

    # and convert values to int
    df = df.astype({
        k: int
        for k in column_mapping.values() if k in df.columns
    })

    print(f"File: {path}; Date: {d}; Sex: {sex}")
    print(df.head())
    print(df.tail())

    return df


def save(path_prefix: Path, input_df: pd.DataFrame) -> None:
    path_table = str(path_prefix) + '_table.csv'
    print(f"Saving as table into {path_table}")
    input_df.to_csv(path_table)

    data = []
    i = 0
    for col_name in input_df.columns:
        for index, value in input_df[col_name].items():
            data.append(index + (col_name, value))

    index_columns = ['date', 'sex', 'age', 'NUTS']
    tuples = pd.DataFrame(data=data, columns=index_columns + ['population']).set_index(index_columns)
    path_tuples = str(path_prefix) + '_tuples.csv'
    print(f"Saving as tuples into {path_tuples}")
    tuples.to_csv(path_tuples)


DIR_ACT = Path(__file__).parent.absolute()
DIR_ORIGINAL = DIR_ACT / 'original'
DIR_CONVERTED = DIR_ACT / 'converted'

if __name__ == '__main__':
    # convert 2019

    dir_original_2019 = DIR_ORIGINAL / '2019'
    dir_converted_2019 = DIR_CONVERTED / '2019'
    dir_converted_2019.mkdir(parents=True, exist_ok=True)

    # 2019-01-01
    df_2019_01_01_B = load(dir_original_2019 / '1300642001.xlsx', date(2019, 1, 1), 'B')
    save(dir_converted_2019 / '1300642001', df_2019_01_01_B)

    df_2019_01_01_M = load(dir_original_2019 / '1300642002.xlsx', date(2019, 1, 1), 'M')
    save(dir_converted_2019 / '1300642002', df_2019_01_01_M)

    df_2019_01_01_F = load(dir_original_2019 / '1300642003.xlsx', date(2019, 1, 1), 'F')
    save(dir_converted_2019 / '1300642003', df_2019_01_01_F)

    df_2019_01_01 = pd.concat([df_2019_01_01_B, df_2019_01_01_M, df_2019_01_01_F])
    save(dir_converted_2019 / '2019_01_01', df_2019_01_01)

    del df_2019_01_01_B
    del df_2019_01_01_M
    del df_2019_01_01_F
    del df_2019_01_01

    # 2019-07-01
    df_2019_07_01_B = load(dir_original_2019 / '1300642004.xlsx', date(2019, 7, 1), 'B')
    save(dir_converted_2019 / '1300642004', df_2019_07_01_B)

    df_2019_07_01_M = load(dir_original_2019 / '1300642005.xlsx', date(2019, 7, 1), 'M')
    save(dir_converted_2019 / '1300642005', df_2019_07_01_M)

    df_2019_07_01_F = load(dir_original_2019 / '1300642006.xlsx', date(2019, 7, 1), 'F')
    save(dir_converted_2019 / '1300642006', df_2019_07_01_F)

    df_2019_07_01 = pd.concat([df_2019_07_01_B, df_2019_07_01_M, df_2019_07_01_F])
    save(dir_converted_2019 / '2019_07_01', df_2019_07_01)

    del df_2019_07_01_B
    del df_2019_07_01_M
    del df_2019_07_01_F
    del df_2019_07_01

    # 2019-12-31
    df_2019_12_31_B = load(dir_original_2019 / '1300642007.xlsx', date(2019, 12, 31), 'B')
    save(dir_converted_2019 / '1300642007', df_2019_12_31_B)

    df_2019_12_31_M = load(dir_original_2019 / '1300642008.xlsx', date(2019, 12, 31), 'M')
    save(dir_converted_2019 / '1300642008', df_2019_12_31_M)

    df_2019_12_31_F = load(dir_original_2019 / '1300642009.xlsx', date(2019, 12, 31), 'F')
    save(dir_converted_2019 / '1300642009', df_2019_12_31_F)

    df_2019_12_31 = pd.concat([df_2019_12_31_B, df_2019_12_31_M, df_2019_12_31_F])
    save(dir_converted_2019 / '2019_12_31', df_2019_12_31)

    del df_2019_12_31_B
    del df_2019_12_31_M
    del df_2019_12_31_F
    del df_2019_12_31
