from flask import Flask
import folium
import folium.plugins as plugins
from flask import request
import numpy as np
import pandas as pd
import requests
import json
import requests

app = Flask(__name__)

@app.route('/')
def mapa():

    try:
        cut = request.args.get("cut")
        cut = int(cut)
    except:
        cut = 13101

    datos = "https://raw.githubusercontent.com/hectorflores329/heroku/main/Base_ZonaLoc_Censo.csv"
    df = pd.read_csv(datos)

    df = df[df["CUT"] == cut]
    indx = df.index[0]

    url = (
        "http://ide.dataintelligence-group.com/mapasdi"
    )
    mapaJson = f"{url}/Base_ZonaLoc_Censo.json"

    input_dict = json.loads(requests.get(mapaJson).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['CUT'] == cut]

    salida = {'type:':'FeatureCollection','features':output_dict}

    html="""

        <style>
            *{
                font-family: Arial, Tahoma;
                font-size: 13px;
            }
            
            li{
                list-style:none;
                margin-left: -40px;
            }

        </style>

        <h3>Datos e información</h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["REGION"][indx]) + """</li>
                <li><b>PROVINCIA:</b> """ + str(df["PROVINCIA"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["COMUNA"][indx]) + """</li>
                <li><b>HOMBRES, 2017 - 2018:</b> """ + str(df["TOTAL_HOMB"][indx]) + """</li>
                <li><b>MUJERES, 2017 - 2018:</b> """ + str(df["TOTAL_MUJE"][indx]) + """</li>
                <li><b>TOTAL PERSONAS, 2017 - 2018:</b> """ + str(df["TOTAL_PERS"][indx]) + """</li>
            </ul>
        </div>
    """

    iframe = folium.IFrame(html=html, width=250, height=210)
    _popup = folium.Popup(iframe, max_width=2650)

    m = folium.Map(
        location=[-33.411165140009885, -70.66420044462977],
        zoom_start=13,
    )

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Geojson S.1p"
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
