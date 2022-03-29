from data_transform import clean_and_transform_data
from visualization import tracking_data_timestamp, tracking_data_overview
from image2video import image2video
import datetime
import pandas as pd
import cv2


if __name__ == '__main__':
    df = clean_and_transform_data("last3years_all.csv", datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
                                      datetime.datetime(2022, 1, 1, 0, 0, 0, 0),
                                      ["SEASON", "NUMBER", "NAME", "ISO_TIME", "LAT", "LON", "USA_WIND"], "ISO_TIME")

    df.to_csv("ready_data.csv", index=False)

    df = pd.read_csv("ready_data.csv")

    tracking_data_overview(df)
    tracking_data_timestamp(df)

    image2video('img', 'video.avi')

    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # image2video('img', 'video.mp4', fourcc=fourcc)