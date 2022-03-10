import pandas as pd
import datetime
import numpy as np

# # only read the columns and rows that we are interested
# cols = ["SEASON", "NAME", "ISO_TIME", "LAT", "LON", "WMO_WIND", "USA_WIND", "TOKYO_WIND", "CMA_WIND", "NEWDELHI_WIND",
#         "REUNION_WIND", "BOM_WIND", "WELLINGTON_WIND"]
# dateparse = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if (x != " ") else x
# raw_df_chunk = pd.read_csv("last3years_all.csv", usecols=cols,  parse_dates=['ISO_TIME'], chunksize=1000,
#                            date_parser=dateparse, dtype='unicode', skiprows=[1])
# df = pd.concat([chunk[pd.to_datetime(chunk["ISO_TIME"], "%Y-%m-%d") >
#                       datetime.datetime(2021, 1, 1, 0, 0, 0, 0)] for chunk in raw_df_chunk])
#
# # populate the missing values from other xx_wind column to wmo_wind column
# # df.loc[df["WMO_WIND"] == " ", ["WMO_WIND"]] = df[df["WMO_WIND"] == " "]["USA_WIND"]
#
# # We can find out that USA_WIND has the most complete values in the for the wind speed
# df = df.drop(columns=["WMO_WIND", "TOKYO_WIND", "CMA_WIND", "NEWDELHI_WIND", "REUNION_WIND", "BOM_WIND",
#                       "WELLINGTON_WIND"])
#
# # assign missing values
# df["USA_WIND"] = df["USA_WIND"].replace(" ", np.nan)
# df["USA_WIND"] = pd.to_numeric(df["USA_WIND"])
# df.loc[df["USA_WIND"].isna(), ["USA_WIND"]] = 5 if min(df["USA_WIND"]) - 5 < 0 else min(df["USA_WIND"]) - 5
# print(min(df["USA_WIND"]))


def clean_and_transform_data(fp, start_date, cols, date_col, chunk_size=1000):
    dateparse = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if (x != " ") else x
    raw_df_chunk = pd.read_csv(fp, usecols=cols, parse_dates=[date_col], chunksize=chunk_size,
                               date_parser=dateparse, dtype='unicode', skiprows=[1])
    df = pd.concat([chunk[pd.to_datetime(chunk[date_col], "%Y-%m-%d") > start_date] for chunk in raw_df_chunk])
    df["USA_WIND"] = df["USA_WIND"].replace(" ", np.nan)
    df["USA_WIND"] = pd.to_numeric(df["USA_WIND"])
    df.loc[df["USA_WIND"].isna(), ["USA_WIND"]] = 5 if min(df["USA_WIND"]) - 5 < 0 else min(df["USA_WIND"]) - 5
    df["USA_WIND"] = df["USA_WIND"].apply(lambda x: knots_to_km_h(x))
    return df


def add_comment(df, target_name, comments):
    df["COMMENT"] = np.nan
    for idx, name in enumerate(target_name):
        df.loc[df["NAME"] == name, "COMMENT"] = comments[idx]
    return df


def knots_to_km_h(knots):
    km_h = knots * 1.852
    return km_h


if __name__ == '__main__':
    df = clean_and_transform_data("last3years_all.csv", datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
                                  ["SEASON", "NAME", "ISO_TIME", "LAT", "LON", "USA_WIND"], "ISO_TIME")

    df.to_csv("ready_data.csv", index=False)
