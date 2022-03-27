import pandas as pd
import plotly.graph_objects as go
import logging
import os


def tracking_data_overview(df):
    season_lst = df.SEASON.unique()
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        lon=[],
        lat=[],
        marker={'size': 3}))
    for year in season_lst:
        sub_df = df.loc[df["SEASON"] == year, :]
        name_lst = sub_df.NAME.unique()
        for name in name_lst:
            tracking_data = sub_df.loc[df["NAME"] == name, :].sort_values(by=["ISO_TIME"])
            lon = tracking_data.LON.tolist()
            lat = tracking_data.LAT.tolist()
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lon=lon,
                lat=lat,
                name=name,
                marker={'size': 3}))

    fig.update_layout(
        width=1025,
        height=950,
        showlegend=False,
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 0, 'lat': 0},
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
    check_lst = df["ISO_TIME"] == date
    opacity_lst = [1 if check else 0.2 for idx, check in check_lst.items()]
    color_lst = [df["USA_WIND"][idx] if check else "chartreuse" for idx, check in check_lst.items()]
    size_lst = [15 if check else 10 for idx, check in check_lst.items()]
    text_lst = [df.NAME[idx] if check else "" for idx, check in check_lst.items()]
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
                "opacity": opacity_lst,
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
    date_lst = df.sort_values(by=["ISO_TIME"]).ISO_TIME.unique()
    max_wind = max(df.USA_WIND)
    min_wind = min(df.USA_WIND)
    for date in date_lst:
        current_val = df.loc[df["ISO_TIME"] == date, :]
        name_lst = current_val.NAME
        number_lst = current_val.NUMBER
        sub_df = df.loc[(df["ISO_TIME"] <= date) & (df["NAME"].isin(name_lst)) & (df["NUMBER"].isin(number_lst)), :]
        tracking_data_single(sub_df, min_wind, max_wind, date)


if __name__ == '__main__':
    df = pd.read_csv("ready_data.csv")
    tracking_data_timestamp(df)

