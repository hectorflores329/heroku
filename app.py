from flask import Flask
import folium
import folium.plugins as plugins
from flask import request
import numpy as np
import pandas as pd
import requests
import json
import requests
from branca.element import Template, MacroElement

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

    indxR = dfRegion.index[0]

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

    
    if(region == 13):
        ubicacion = [-33.4537511827, -70.6569543965]
    else:
        ubicacion = [dfRegion["lat_comuna"][indxR], dfRegion["lon_comuna"][indxR]]

    m = folium.Map(
        location=ubicacion,
        zoom_start=8,
    )

    for i in cuts:
    
        cut = i
        # print(cut)
        
        df = pd.read_csv(datos)

        df = df[df["CUT"] == cut]
        indx = df.index[0]

        output_dict = [x for x in input_dict['features'] if x['properties']['COMUNA'] == str(cut)]

        salida = {'type':'FeatureCollection','features':output_dict}

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
                        tooltip = "<b>Comuna: </b>" + str(df["COMUNA"][indx]),
                        style_function = lambda feature: {
                                "fillColor": "#1381c0"
                                if feature["properties"]["T_HOM"] > feature["properties"]["T_MUJ"]
                                else "#f632a3",
                                "color": "black",
                                "weight": 2,
                                "dashArray": "5, 5",
                            },
                        ).add_to(m)

        popup = _popup
        popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dataintelligence</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

    <script>
        function recargar() {
            parent.document.location.href = "https://geemapa.herokuapp.com/mapa2?region=8";
        }
    </script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>CENSO (POBLACIÓN)</div>
    <div class='legend-title'>""" + str(df["REGION"][indx]) + """</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:#1381c0;opacity:0.7;'></span>Hombres</li>
        <li><span style='background:#f632a3;opacity:0.7;'></span>Mujeres</li>
        <br>
        <li>Región con más poblacion:</li>
        <li><a href="#" onclick="recargar()">Ver región</></li>

    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    m.get_root().add_child(macro)

    return m._repr_html_()

# TERCER MAPA

@app.route('/mapa3')
def mapa3():

    try:
        cut = request.args.get("cut")
        cut = int(cut)

        variable = request.args.get("var")
        variable = str(variable)
        
    except:
        cut = 13101
        variable = "TOTAL_PERS"

    _variable = ""

    if (variable == "TOTAL_PERS"):
        _variable = "Total personas"

    elif (variable == "TOTAL_HOMB"):
        _variable = "Total hombres"

    elif (variable == "TOTAL_MUJE"):
        _variable = "Total mujeres"

    elif (variable == "PUEBLOS_IN"):
        _variable = "Pueblos indígenas"

    elif (variable == "TOTAL_VIV_"):
        _variable = "Total viviendas"

    elif (variable == "VIV_OCUPA_"):
        _variable = "Viviendas ocupadas"

    else:
        _variable = "No definida"

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

            .col2{
                background-color: #2a7fce;
                font-size: 11px;
                padding: 4px;
                box-sizing: border-box;
                color: #FFF;
                text-align: right;
                margin-bottom: 5px;
                max-width: 100%;
            }

            .counter{
                padding-top: 10px;
                font-size:30px;
                font-weight:bold;
                text-align:center;
                cursor: pointer;
            } 

        </style>

        <h3><b>DATOS CENSO</b></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["REGION"][indx]) + """</li>
                <li><b>REGIÓN:</b> """ + str(df["PROVINCIA"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["COMUNA"][indx]) + """</li>
                <li><b>VARIABLE:</b> """ + _variable + """</li>
            </ul>
        </div>

        <div class="col2">
            <div class="counter">""" + str('{:,}'.format(df[variable][indx]).replace(',','.')) + """</div>
            <h3><center>CANTIDAD</center></h3>
        </div>

    """

    if (cut == 13101):
        ubicacion = [-33.4537511827, -70.6569543965]
    else:
        ubicacion = [df["lat_comuna"][indx], df["lon_comuna"][indx]]

    iframe = folium.IFrame(html=html, width=250, height=250)
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

if __name__ == '__main__':
    app.run()
