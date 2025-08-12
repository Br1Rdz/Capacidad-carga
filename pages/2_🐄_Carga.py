import streamlit as st
from streamlit_folium import st_folium
import ee
import geemap.foliumap as geemap
import geemap.colormaps as cm
import datetime
import pandas as pd
import datetime
import json

# Cargar los secretos
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

# Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data = json_data)
ee.Initialize(credentials)

# Configuración de página
st.set_page_config(
    page_title="Capacidad de carga",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)
st.logo("./Informacion.png", icon_image="./info2.png")
# Sidebar
# st.sidebar.title(":red-background[INFORMACION]\nV.1.0")
# st.sidebar.info("""
# Cálculo de área idónea para el pastoreo a partir de imágenes LANDSAT 8.
# - Selección de píxeles con **NDVI idóneo**.
# - Cálculo del área total en m².
# - Estimación de unidades animales para el predio.  
# \n
# Developed by Bruno Rodriguez
# """)
# st.sidebar.info("Github: [Br1Rdz](https://github.com/Br1Rdz/)")
# st.sidebar.image("./Clicker.jpg")

    #-------- Hide streamlit style ------------    
hide_st_style = '''
                      <style>
                      #Main Menu {visibility:hidden;}
                      footer {visibility:hidden;}
                      header {visibility:hidden;}
                      </style>
      '''
st.markdown(hide_st_style, unsafe_allow_html= True)

# Título
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">

<h1 style='font-family: "Bebas Neue", sans-serif; text-align: center; font-size: 25px; color: #ffffff;
           letter-spacing: 10px;
           text-shadow: 2px 2px 6px rgba(255,255,255,0.2),
           -2px -2px 6px rgba(0,0,0,0.5);'>
  Cálculo de unidades animales
</h1>
""", unsafe_allow_html=True)
# st.title("📈 Cálculo de unidades animales")

# Parámetros
with st.expander("🔧 Configuración de parámetros", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        Inicio = st.date_input("🗓️ Fecha Inicial", datetime.date(2024, 5, 1))
        
    with col2:
        Final = st.date_input("🗓️ Fecha Final", datetime.date(2024, 5, 31))
    Consumo_por_animal = st.number_input("🐄 Consumo por animal ha", value=10.56)
    
    with col3:
    	umbral = st.number_input("🌿Umbral de NDVI", value=0.10)

# Fechas en formato string
Fecha_inicio = Inicio.strftime("%Y-%m-%d")
Fecha_final = Final.strftime("%Y-%m-%d")

# Crear mapa base
Map = geemap.Map(
    center=[25.5725, -103.4945],
    zoom=10,
    basemap="SATELLITE",
    zoom_control=False,
    fullscreen_control=False,
    scale_control=False,
    attribution_control=False,
    toolbar_control=False
)


# Mostrar mapa inicial para que el usuario dibuje
map_output = st_folium(Map, height=350, width=700, key="main_map_draw", use_container_width = True)

# Si el usuario dibuja un polígono
if map_output and 'all_drawings' in map_output and map_output['all_drawings']:
    geojson = map_output['all_drawings'][0]['geometry']
    predio = ee.Geometry(geojson)

    # Cargar imagen satelital
    # image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')\
    #     .filterBounds(predio)\
    #     .filterDate(Fecha_inicio, Fecha_final)\
    #     .sort("CLOUD_COVER")\
    #     .first()
    #imagenes sentinel
    image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")\
                .filterBounds(predio)\
                .filterDate(Fecha_inicio, Fecha_final)\
                .sort("CLOUD_COVER")\
                .map(lambda image : image.expression(
                    '(NIR - RED ) / (NIR + RED)',
                    {'NIR':image.select('B8'),
                     'RED':image.select('B4')}
                ).rename('NDVI').copyProperties(image, image.propertyNames()))\
                .first()    

    if image:
        # Calcular NDVI
        # NDVI = image.normalizedDifference(['SR_B5', 'SR_B4'])
        palette = cm.get_palette("ndvi", n_class=8)
        vis_params = {"min": 0, "max": 1, "palette": palette}

        # Clasificar áreas idóneas
        zones = ee.Image(0).where(image.gt(umbral), 1).unmask(0)
        area_idonea = zones.multiply(ee.Image.pixelArea())

        # Calcular área total
        area_dict = area_idonea.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=predio,
            scale=30,
            maxPixels=1e13
        )

        area = area_dict.getInfo().get('constant', 0) / 10000
        estimacion_consumo = area / Consumo_por_animal

        legend_dict = {'0':'#000000','1':'#FFFFFF'}
        # Agregar capa NDVI al mapa
        Map.addLayer(zones.clip(predio),{'min':0,'max':1, 'palette':['black','white']}, f'Idoneo "{umbral}"')
        Map.addLayer(image.clip(predio), vis_params, 'NDVI')
        Map.center_object(predio, zoom = 13)
        Map.add_colorbar(vis_params, label = 'NDVI', layer_name ='NDVI', background_color=None)
        # Map.add_colorbar_branca({'min':0, 'max':1, 'palette':['#000000','#000000','#FFFFFF']},
        #                         step=2, vmin=0, vmax=2, position='bottomright')
        # Map.add_legend(title="Idoneo", legend_dict=legend_dict,
        #                style = {
        #                 'position': 'fixed', 'z-index': '9999', 'border': '2px solid grey', 'background-color':
        #                 'rgba(200, 255, 255, 10)', 'border-radius': '5px', 'padding': '10px', 'font-size':
        #                 '20px', 'bottom': '20px', 'right': '5px'
        #                 })
        Map.add_layer_control()
        # Map.add_minimap()

        # Mostrar resultados
        #sentinel
        fecha_raw = image.get('system:time_start').getInfo()
        fecha = datetime.datetime.fromtimestamp(fecha_raw/1000).strftime('%Y-%m-%d')
        #Dataframe
        df_resultados = pd.DataFrame({
            "📅 Fecha": [fecha],
            "🌿 Área idónea (ha)": [round(area,2)],
            "🐄 Unidades animales": [round(estimacion_consumo,2)],
            "📈 Umbral NDVI": [umbral]
        })

        # Mostrar tabla con formato
        st.dataframe(df_resultados, use_container_width=True, hide_index = True) 
        # st.markdown(
        #     f""":gray-background[📅 {image.get('DATE_ACQUIRED').getInfo()} | 🌿 Área idónea: {area:.2f} ha
        #     | 🐄 Unidades animales: {estimacion_consumo:.2f} |📈 Umbral de NDVI de {umbral:.2f}]"""
        #     )

        # Renderizar mapa actualizado
        st_folium(Map, height=350, width=700, key="main_map_ndvi", use_container_width = True)
    else:
        st.warning("No se encontró imagen para las fechas seleccionadas.")
else:
    st.info("Dibuja tu predio en el mapa para continuar.")

