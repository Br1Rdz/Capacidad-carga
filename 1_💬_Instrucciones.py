import streamlit as st 

st.set_page_config(page_title="Introducción", 
                    page_icon="🐄", 
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items=None)

# url = "https://github.com/Br1Rdz/"
    
# markdown = """
#     Developed by Bruno Rodriguez
#     """
st.sidebar.markdown("""
                    <div style='background-color:#FFD700; display:inline-block; padding:4px 8px; border-radius:4px; color:#000000; font-size: 12px
                    font-family:serif;'>
                     <em><i>Developed by Bruno Rodriguez</i></em>
                    </div>
                    """, 
                    unsafe_allow_html= True)
    #-------- Hide streamlit style ------------    
hide_st_style = '''
                      <style>
                      #Main Menu {visibility:hidden;}
                      footer {visibility:hidden;}
                      header {visibility:hidden;}
                      </style>
      '''
st.markdown(hide_st_style, unsafe_allow_html= True)

# st.sidebar.info(markdown)
# st.sidebar.info("Github: [Br1Rdz](%s)" % url)

logo = "./LOGO.png"
st.sidebar.image(logo) 
st.logo("./Informacion.png", icon_image="./info2.png")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<h1 style='font-family: "Bebas Neue", sans-serif; text-align: center; font-size: 52px; color: #ffffff;
           letter-spacing: 10px;
           text-shadow: 2px 2px 6px rgba(255,255,255,0.2),
           -2px -2px 6px rgba(0,0,0,0.5);'>
  Capacidad de carga
</h1>
""", unsafe_allow_html=True)

# st.title('Instrucciones')
# https://github.com/streamlit/streamlit/issues/2338
col1, col2, col3 = st.columns(3)

with col2:
    # Display the image in the middle column
    # Adjust the 'width' parameter to control the image size
    st.image("./carga.png", width=300) 

# st.markdown(
#     """
#     <style>
#     # @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
#     .custom-text {
#         font-family: 'Bebas Neue', sans-serif;
#         font-size: 12px;
#         text-align: justify;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

    
st.markdown(
    """
    <div style="text-align: justify; font-family: sans-serif; font-size:12px">
       La <span style="color:yellow">carga animal</span> se refiere al número de unidades animales que un terreno o ecosistema puede sostener de manera saludable.
       En la actualidad, estimar este valor es fundamental para planificar y garantizar un aprovechamiento sustentable de los recursos.
       Los avances en sensores remotos y el análisis de imágenes satelitales permiten realizar estas estimaciones de forma más práctica,
       precisa y eficiente, facilitando la toma de decisiones para un manejo responsable del territorio. 
       En esta aproximación se utilizó como ejemplo el ganado bovino para estimar cuántas unidades animales podría soportar
       un sitio definido por el usuario. Para determinar el área idónea, se emplearon imágenes <span style="color:yellow">Sentinel-2</span> (2015 a la actualidad)
       con resolución espacial de 10 metros por píxel. A partir de estas imágenes se calculó el <span style="color:yellow">Índice de Vegetación de Diferencia
       Normalizada (NDVI)</span>, aplicando un umbral predeterminado para identificar las zonas con cobertura vegetal suficiente.
       Además, se incorporó el parámetro de consumo de una unidad animal por hectárea, todo lo anterior puede ser configurable.
       Con esta información, la aplicación estima de forma dinámica cuántas unidades animales puede sostener el área seleccionada.
       <br>
       <br><strong>Nota importante:
       Para crear un polígono correctamente, espera aproximadamente 3 segundos entre cada punto que marques.
       Esto permite que el mapa se actualice sin problemas. Si agregas los puntos muy rápido, el mapa se reiniciara. <i>...Por favor espera un poquio mas..</i>.</strong>
    </div>
    """,
    unsafe_allow_html=True
)
st.video("video/video.mp4", format="video/mp4")
