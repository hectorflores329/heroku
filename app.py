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

    datos = "https://raw.githubusercontent.com/hectorflores329/heroku/main/comunas.csv"
    df = pd.read_csv(datos)

    vivi = df["TOTAL_VIVI"].sum()

    df = df[df["CUT"] == cut]
    indx = df.index[0]

    url = (
        "https://raw.githubusercontent.com/hectorflores329/heroku/main"
    )
    mapaJson = f"{url}/Lim_comunas.json"

    input_dict = json.loads(requests.get(mapaJson).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['COMUNA'] == str(cut)]

    salida = {'type:':'FeatureCollection','features':output_dict}

    hombre = round((df["TOTAL_HOMB"][indx] * 100) / df["TOTAL_PERS"][indx], 1)
    mujer = round((df["TOTAL_MUJE"][indx] * 100) / df["TOTAL_PERS"][indx], 1)
    vivienda = round((df["TOTAL_VIVI"][indx] * 100) / vivi, 1)

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
                font-size: 11px;
                padding: 4px;
                box-sizing: border-box;
                color: #FFF;
                text-align: right;
                margin-bottom: 5px;
                max-width: """ + str(hombre) +"""%;
            }

            .col2{
                background-color: #f632a3;
                font-size: 11px;
                padding: 4px;
                box-sizing: border-box;
                color: #FFF;
                text-align: right;
                margin-bottom: 5px;
                max-width: """ + str(mujer) +"""%;
            }

            .col3{
                background-color: #fba02d;
                font-size: 11px;
                padding: 4px;
                box-sizing: border-box;
                color: #3D3D3D;
                text-align: right;
                max-width: """ + str(vivienda) +"""%;
            }

            .background{
                background-color: #d2d2d2;
            }

        </style>

        <h3><b>DATOS CENSO</b></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["REGION"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["COMUNA"][indx]) + """</li>
                <li><b>HOMBRES:</b> """ + str('{:,}'.format(df["TOTAL_HOMB"][indx]).replace(',','.')) + """</li>
                <li><b>MUJERES:</b> """ + str('{:,}'.format(df["TOTAL_MUJE"][indx]).replace(',','.')) + """</li>
                <li><b>TOTAL PERSONAS:</b> """ + str('{:,}'.format(df["TOTAL_PERS"][indx]).replace(',','.')) + """</li>
                <li><b>TOTAL VIVIENDAS:</b> """ + str('{:,}'.format(df["TOTAL_VIVI"][indx]).replace(',','.')) + """</li>
            </ul>
        </div>

        <div class="contenedor"> 
            <div class="background">
                <div class="col1">
                    <h3>Hombres: """ + str(hombre) + """%</h3>
                </div>
            </div>
            <div class="background">
                <div class="col2">
                    <h3>Mujeres: """ + str(mujer) + """%</h3>
                </div> 
            </div>
            <div class="background">
                <div class="col3">
                    <h3>Vivienda: """ + str(vivienda) + """%</h3>
                </div> 
            </div>
        </div>

    """

    if (cut == 13101):
        ubicacion = [-33.4537511827, -70.6569543965]
    else:
        ubicacion = [df["lat_comuna"][indx], df["lon_comuna"][indx]]

    iframe = folium.IFrame(html=html, width=250, height=365)
    _popup = folium.Popup(iframe, max_width=2650)

    m = folium.Map(
        location=ubicacion,
        zoom_start=11,
    )

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Censo"
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

# SEGUNDO MAPA

@app.route('/mapa2')
def mapa2():

    try:
        region = request.args.get("region")
        region = int(region)
    except:
        region = 13

    datos = "https://raw.githubusercontent.com/hectorflores329/heroku/main/comunas.csv"
    dfRegion = pd.read_csv(datos)

    dfRegion = dfRegion[dfRegion["COD_REGION"] == region]
    cuts = dfRegion["ID_COM"].unique().tolist()
    cuts

    url = (
        "https://raw.githubusercontent.com/hectorflores329/heroku/main"
    )
    mapaJson = f"{url}/Lim_comunas.json"

    input_dict = json.loads(requests.get(mapaJson).content)

    '''if (region == 13):
        ubicacion = [-33.4537511827, -70.6569543965]
    else:
        ubicacion = [df["lat_comuna"][indx], df["lon_comuna"][indx]]'''

    vivi = dfRegion["TOTAL_VIVI"].sum()

    

    m = folium.Map(
        location=[-33.4537511827, -70.6569543965],
        zoom_start=11,
    )

    for i in cuts:
    
        cut = i
        # print(cut)
        
        df = pd.read_csv(datos)

        df = df[df["CUT"] == cut]
        indx = df.index[0]

        output_dict = [x for x in input_dict['features'] if x['properties']['COMUNA'] == str(cut)]

        salida = {'type:':'FeatureCollection','features':output_dict}

        hombre = round((df["TOTAL_HOMB"][indx] * 100) / df["TOTAL_PERS"][indx], 1)
        mujer = round((df["TOTAL_MUJE"][indx] * 100) / df["TOTAL_PERS"][indx], 1)

        html="""

            <style>
                *{
                    font-family: Arial, Helvetica, sans-serif;
                    font-size: 13px;
                }

                .contenedor0{
                    /* background-color: #c4732c; */
                    width: 100%;
                    height: 6%;
                    float: left;
                    text-align: center;
                    margin: 5px;
                    font-size: 14px;
                }

                .contenedor1{
                    /* background-color: #FF7800; */
                    width: 30%;
                    height: 52%;
                    float: left;
                    padding: 8px;
                    box-sizing: border-box;
                }

                .contenedor2{
                    /* background-color: #FF2500; */
                    width: 70%;
                    height: 52%;
                    float: left;
                    padding: 8px;
                    box-sizing: border-box;
                }

                .contenedor3{
                    /* background-color: #F89610; */
                    width: 30%;
                    height: 38%;
                    float: left;
                    padding: 8px;
                    box-sizing: border-box;
                    text-align: center;
                }

                .contenedor4{
                    /* background-color: #FFF000; */
                    width: 70%;
                    height: 38%;
                    float: left;
                    padding: 8px;
                    box-sizing: border-box;
                }

                .container{
                    width: 100%;
                    height: 100%;
                    /* border: 2px dashed black; */
                }

                ul{
                    margin-top: -10px;
                }

                li{
                    list-style:none;
                    margin-left: -50px;
                }

                .contenedor4 li{
                    list-style:none;
                    margin-left: -40px;
                }

                .escudo{
                    width: auto;
                    height: 100%;
                }

                .ubicacion{
                    width: 100%;
                    height: 100%;
                    border-radius: 4px;
                }

                .col1{
                    background-color: #1381c0;
                    font-size: 11px;
                    padding: 4px;
                    box-sizing: border-box;
                    color: #FFF;
                    text-align: right;
                    margin-bottom: 5px;
                    max-width: """ + str(hombre) +"""%;
                }

                .col2{
                    background-color: #f632a3;
                    font-size: 11px;
                    padding: 4px;
                    box-sizing: border-box;
                    color: #FFF;
                    text-align: right;
                    margin-bottom: 5px;
                    max-width: """ + str(mujer) +"""%;
                }
                
                .background{
                    background-color: #d2d2d2;
                }
            </style>

            <div class="container">
                <div class="contenedor0">
                    <p><b>DATOS CENSO</b></p>
                </div>

                <div class="contenedor3">
                    <img src='""" + str(df["Escudo"][indx]) + """' alt='Comuna' class='escudo' />
                </div>

                <div class="contenedor4">
                    <ul>
                        <li><h3>POBLACIÓN TOTAL EN LA COMUNA: """ + str(df["COMUNA"][indx]) + """</h3></li>
                        <li><b>HOMBRES: </b>""" + str(hombre) + """% | <b>MUJERES: </b> """ + str(mujer) + """%</li>
                    </ul>
                    <div class="background">
                        <div class="col1">
                            <h3>Hombres: """ + str(hombre) + """%</h3>
                        </div>
                    </div>
                    <div class="background">
                        <div class="col2">
                            <h3>Mujeres: """ + str(mujer) + """%</h3>
                        </div> 
                    </div>
                </div>

                <div class="contenedor1">
                    <ul>
                        <li><h3>INFORMACIÓN GENERAL</h3></li>
                        <li><b>REGIÓN:</b><br>""" + str(df["REGION"][indx]) + """</li>
                        <li><b>COMUNA:</b><br>""" + str(df["COMUNA"][indx]) + """</li>
                        <li><b>HOMBRES:</b><br>""" + str('{:,}'.format(df["TOTAL_HOMB"][indx]).replace(',','.')) + """</li>
                        <li><b>MUJERES:</b><br>""" + str('{:,}'.format(df["TOTAL_MUJE"][indx]).replace(',','.')) + """</li>
                        <li><b>TOTAL PERSONAS:</b><br>""" + str('{:,}'.format(df["TOTAL_PERS"][indx]).replace(',','.')) + """</li>
                        <li><b>TOTAL VIVIENDAS:</b><br>""" + str('{:,}'.format(df["TOTAL_VIVI"][indx]).replace(',','.')) + """</li>
                    </ul>
                </div>

                <div class="contenedor2">
                    <img src="https://github.com/hectorflores329/heroku/raw/main/santiago.png" alt="Ubicación geográfica" class="ubicacion"/>
                </div>
            </div>

        """

        iframe = folium.IFrame(html=html, width=600, height=500)
        _popup = folium.Popup(iframe, max_width=2650)

        geojson = folium.GeoJson(json.dumps(salida), 
                        name="Censo",
                        tooltip = df["COMUNA"][indx]
                        ).add_to(m)

        popup = _popup
        popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
