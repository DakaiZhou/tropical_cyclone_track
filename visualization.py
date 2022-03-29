import pandas as pd
import plotly.graph_objects as go
import logging
import os


def tracking_data_overview(df):
    """
    Give the all cyclone traces and visualize them
    :param df: pandas dataframe
    :return:
    """
    # column SEASON is year. One year can be expanded to the first several days of the next year
    season_lst = df.SEASON.unique()
    fig = go.Figure(go.Scattermapbox(
        mode="markers+lines",
        lon=[],
        lat=[],
        marker={'size': 3}))
    for year in season_lst:
        # only one season data per loop
        sub_df = df.loc[df["SEASON"] == year, :]
        number_lst = sub_df.NUMBER.unique()
        for number in number_lst:
            # the full trace for one cyclone in one year
            trace = sub_df.loc[df["NUMBER"] == number, :]
            lon = trace.LON.tolist()
            lat = trace.LAT.tolist()
            fig.add_trace(go.Scattermapbox(
                mode="markers+lines",
                lon=lon,
                lat=lat,
                name=trace["NAME"].unique()[0],
                marker={'size': 3}))

    fig.update_layout(
        width=1025,
        height=950,
        showlegend=False,
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 0},
            'zoom': 1},
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ]
    )
    fig.show()
    fig.write_image("overview.png")


def tracking_data_single(df, min_color, max_color, date):
    """
    Given trace segments data and visualize them
    :param df: pandas dataframe, trace segment
    :param min_color: min value of the whole dataset, which serves as the min value of the color scale
    :param max_color: max value of the whole dataset, which serves as the max value of the color scale
    :param date: the current timestamps
    :return:
    """
    check_lst = df["ISO_TIME"] == date
    # determine the marker size of current location and the previous locations in the plot
    size_lst = [15 if check else 5 for idx, check in check_lst.items()]
    text_lst = [df.NAME[idx] if check else "" for idx, check in check_lst.items()]
    # determine the colors of the current location and the previous locations in the plot
    color_lst = df.USA_WIND.tolist()
    # visualize all trace segment at once
    fig = go.Figure(go.Scattermapbox(
        # mode "markers+text" raise a bug in scattermapbox, so here we are not going to show name and wind speed around
        # the marker. You can use other maps to achieve this.
        mode="markers",
        lon=df.LON.tolist(),
        lat=df.LAT.tolist(),
        text=text_lst,
        marker={'size': size_lst,
                "showscale": True,
                "color": color_lst,
                "colorscale": [[0, "yellow"], [1, "red"]],
                "cmin": min_color,
                "cmax": max_color,
                "allowoverlap": True,
                "colorbar": {"title": "km/h"}}))

    fig.update_layout(
        width=1125,
        height=950,
        showlegend=False,
        margin={'l': 0, 't': 30, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 7},
            'zoom': 1},
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ],
        title_text="2021 Global Tropical Cyclones Track - {}".format(date),
        title_x=0.5
    )
    if not os.path.exists("img"):
        os.mkdir("img")
    fig.write_image("img/{}.png".format(date))
    logging.basicConfig(level=logging.INFO)
    logging.info("Image {}.png created.".format(date))


def tracking_data_timestamp(df):
    """
    To generate image for each timestamps
    :param df: full data
    :return:
    """

    # all timestamps
    date_lst = df.sort_values(by=["ISO_TIME"]).ISO_TIME.unique()
    max_wind = max(df.USA_WIND)
    min_wind = min(df.USA_WIND)
    # split the data
    for date in date_lst:
        current_val = df.loc[df["ISO_TIME"] == date, :]
        current_name = current_val.NAME
        current_number = current_val.NUMBER
        current_season = current_val.SEASON

        # trace segments for current timestamps, it only contain ongoing cyclones
        sub_df = df.loc[(df["ISO_TIME"] <= date) & (df["NAME"].isin(current_name)) &
                        (df["NUMBER"].isin(current_number)) & (df["SEASON"].isin(current_season)), :]
        tracking_data_single(sub_df, min_wind, max_wind, date)

