from flask import Flask
import folium
import folium.plugins as plugins
from flask import request
import numpy as np
import requests
import json
import requests

app = Flask(__name__)

@app.route('/')
def mapa():

    try:
        id = request.args.get("id")
        id = int(id)
    except:
        id = 13101

    url = (
        "https://raw.githubusercontent.com/hectorflores329/heroku/main"
    )
    mapaJson = f"{url}/Base_ZonaLoc_Censo.json"

    input_dict = json.loads(requests.get(mapaJson).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['CUT'] == id]

    salida = {'type:':'FeatureCollection','features':output_dict}

    m = folium.Map(
        location=[-33.411165140009885, -70.66420044462977],
        zoom_start=8,
    )

    folium.GeoJson(json.dumps(salida), 
                    name="Geojson S.1p"
                    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
