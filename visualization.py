import pandas as pd
import plotly.graph_objects as go


def tracking_data_overview(df):
    season_lst = df.SEASON.unique()
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        lon=[],
        lat=[],
        marker={'size': 5}))
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
                marker={'size': 5}))

    fig.update_layout(
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


if __name__ == '__main__':
    df = pd.read_csv("ready_data.csv")
    tracking_data_overview(df)

