import pandas as pd
import datetime
import numpy as np


def clean_and_transform_data(fp, start_date, end_date, cols, date_col, chunk_size=1000):
    """
    Clean and transform the data to ready status
    :param fp: path of the CSV file
    :param start_date: the start date of the period
    :param end_date: the end date of the period
    :param cols: the needed columns
    :param date_col: the timestamps column
    :param chunk_size: chunk size
    :return: ready dataframe
    """
    dateparse = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if (x != " ") else x
    raw_df_chunk = pd.read_csv(fp, usecols=cols, parse_dates=[date_col], chunksize=chunk_size,
                               date_parser=dateparse, dtype='unicode', skiprows=[1])
    df = pd.concat([chunk[(pd.to_datetime(chunk[date_col], "%Y-%m-%d") > start_date) & (pd.to_datetime(chunk[date_col], "%Y-%m-%d") < end_date)] for chunk in raw_df_chunk])
    df["USA_WIND"] = df["USA_WIND"].replace(" ", np.nan)
    df["USA_WIND"] = pd.to_numeric(df["USA_WIND"])
    df.loc[df["USA_WIND"].isna(), ["USA_WIND"]] = 5 if min(df["USA_WIND"]) - 5 < 0 else min(df["USA_WIND"]) - 5
    df["USA_WIND"] = df["USA_WIND"].apply(lambda x: knots_to_km_h(x))
    return df


def add_comment(df, target_name, comments):
    """
    A function you use to add additional information to certain cyclones
    :param df: pandas dataframe
    :param target_name: list of cyclone names
    :param comments: lis of comments, order align to the names in the target_name
    :return: dataframe with extra column COMMENT
    """
    df["COMMENT"] = np.nan
    for idx, name in enumerate(target_name):
        df.loc[df["NAME"] == name, "COMMENT"] = comments[idx]
    return df


def knots_to_km_h(knots):
    km_h = knots * 1.852
    return km_h

