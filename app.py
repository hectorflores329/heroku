from flask import Flask
import folium
import folium.plugins as plugins
import numpy as np
import pandas as pd
import requests
import geopandas
import branca
import json
import requests
from datetime import datetime, timedelta
from folium.plugins import FloatImage
from folium.plugins import Draw
from folium.plugins import MiniMap
from folium.features import GeoJsonPopup, GeoJsonTooltip

app = Flask(__name__)

@app.route('/')
def mapa():

    url = (
        "https://raw.githubusercontent.com/hectorflores329/herokugee/main"
    )
    antarctic_ice_edge = f"{url}/_ICVU_2019.json"
    antarctic_ice_shelf_topo = f"{url}/_ICVU_2019_topo.json"


    m = folium.Map(
        location=[-59.1759, -11.6016],
        tiles="cartodbpositron",
        zoom_start=2,
    )

    folium.GeoJson(antarctic_ice_edge, name="geojson").add_to(m)

    folium.TopoJson(
        json.loads(requests.get(antarctic_ice_shelf_topo).text),
        "objects.ICVU_2019",
        name="topojson",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
