from flask import Flask
import folium
import folium.plugins as plugins
import numpy as np
import requests
import json
import requests

app = Flask(__name__)

@app.route('/')
def mapa():

    url = (
        "https://raw.githubusercontent.com/hectorflores329/heroku/main"
    )
    mapaJson = f"{url}/Base_ZonaLoc_Censo_MapShaper_15p.json"


    m = folium.Map(
        location=[-33.411165140009885, -70.66420044462977],
        tiles="openstreetmap",
        zoom_start=8,
    )

    folium.GeoJson(mapaJson, name="Geojson S.15p").add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
