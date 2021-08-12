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
        "https://raw.githubusercontent.com/hectorflores329/heroku/main"
    )
    mapaJson = f"{url}/Lim_comunas.json"

    input_dict = json.loads(requests.get(mapaJson).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['COMUNA'] == str(cut)]

    salida = {'type:':'FeatureCollection','features':output_dict}

    html="""

        <style>
            *{
                font-family: Arial, Helvetica, sans-serif;
                font-size: 13px;
            }
            
            li{
                list-style:none;
                margin-left: -40px;
            }

            .contenedor{
                width: 100%;
            }

            .col1{
                background-color: #1381c0;
                padding: 5px;
                color: #FFF;
                text-align: right;
                margin-bottom: 5px;
                max-width: 100%;
            }

            .col2{
                background-color: #f632a3;
                padding: 5px;
                color: #FFF;
                text-align: right;
                max-width: 100%;
            }
        </style>

        <h3><b>DATOS CENSO</b></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["REGION"][indx]) + """</li>
                <li><b>PROVINCIA:</b> """ + str(df["PROVINCIA"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["COMUNA"][indx]) + """</li>
                <li><b>HOMBRES:</b> """ + str(df["TOTAL_HOMB"].sum()) + """</li>
                <li><b>MUJERES:</b> """ + str(df["TOTAL_MUJE"].sum()) + """</li>
                <li><b>TOTAL PERSONAS:</b> """ + str(df["TOTAL_PERS"].sum()) + """</li>
                <li><b>TOTAL VIVIENDAS:</b> """ + str(df["TOTAL_VIVI"].sum()) + """</li>
            </ul>
        </div>

        <div class="contenedor"> 
            <div class="col1">
                <h3>Columna 1</h3>
            </div> 
            <div class="col2">
                <h3>Columna 2</h3>
            </div> 
        </div>
    """

    if (cut == 13101):
        ubicacion = [-33.4537511827, -70.6569543965]
    else:
        ubicacion = [df["lat_comuna"][indx], df["lon_comuna"][indx]]

    iframe = folium.IFrame(html=html, width=250, height=185)
    _popup = folium.Popup(iframe, max_width=2650)

    m = folium.Map(
        location=ubicacion,
        zoom_start=11,
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
