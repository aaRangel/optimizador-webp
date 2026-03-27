import streamlit as st
from PIL import Image
import os
import zipfile
import io
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Optimizador WebP para Diseñadores", page_icon="🖼️")

# --- BARRA LATERAL (Monetización y Referidos) ---
with st.sidebar:
    st.title("Configuración")
    calidad = st.slider("Calidad de compresión", 10, 100, 80)
    ancho_max = st.number_input("Ancho máximo (px)", value=1920)
    
    st.divider()
    
    # Sección Hosting Chileno (V2 Networks)
    st.write("### 🚀 Hosting Recomendado")
    st.info("""
    **¿Buscas un Hosting rápido y con soporte real en Chile?**
    Para mis proyectos personales y de clientes uso **V2 Networks**. 
    Precios excelentes y servidores optimizados.
    """)
    st.link_button("Ver planes en V2 Networks 🇨🇱", "https://clientes.v2networks.cl/aff.php?aff=304")
    st.caption("Apoya este proyecto contratando desde este link.")

# --- CUERPO PRINCIPAL ---
st.title("🖼️ Optimizador de Imágenes WebP")
st.write("Sube tus imágenes (PNG/JPG) para convertirlas a WebP, redimensionarlas y optimizarlas para la web.")

files = st.file_uploader("Arrastra tus imágenes aquí", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, file in enumerate(files):
            img = Image.open(file)
            
            # Redimensionar manteniendo proporción
            if img.width > ancho_max:
                w_percent = (ancho_max / float(img.width))
                h_size = int((float(img.height) * float(w_percent)))
                img = img.resize((ancho_max, h_size), Image.Resampling.LANCZOS)
            
            # Convertir a WebP en memoria
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='WEBP', quality=calidad)
            
            # Agregar al ZIP con numeración
            zip_file.writestr(f"{i+1}.webp", img_byte_arr.getvalue())
            
    st.success(f"✅ {len(files)} imágenes procesadas con éxito.")
    
    st.download_button(
        label="📥 Descargar todas en .ZIP",
        data=zip_buffer.getvalue(),
        file_name="imagenes_optimizadas.zip",
        mime="application/zip"
    )

# --- PIE DE PÁGINA ---
st.divider()
st.caption("Herramienta creada para la comunidad de diseñadores de LATAM.")

# --- BOTÓN FLOTANTE DE KO-FI ---
kofi_button = """
<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
<script>
  kofiWidgetOverlay.draw('armandorangel76306', {
    'type': 'floating-chat',
    'floating-chat.donateButton.text': '¿Te ahorré unos MB? ☕',
    'floating-chat.donateButton.background-color': '#f45d22',
    'floating-chat.donateButton.text-color': '#fff'
  });
</script>
"""
components.html(kofi_button, height=0)
