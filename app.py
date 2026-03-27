import streamlit as st
from PIL import Image
import os
import zipfile
import io
import streamlit.components.v1 as components

# Configuración de la página (Pestaña del navegador)
st.set_page_config(page_title="Optimizador WebP | aaRangel", page_icon="🖼️")

# --- BARRA LATERAL (Configuración y Monetización) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    calidad = st.slider("Calidad de compresión", 10, 100, 80)
    ancho_max = st.number_input("Ancho máximo (px)", value=1920)
    
    st.divider()
    
    # SECCIÓN: Hosting Recomendado (V2 Networks)
    st.write("### 🚀 Hosting Recomendado")
    st.info("""
    **¿Buscas un Hosting rápido y con soporte real en Chile?**
    Para mis proyectos personales y de clientes uso **V2 Networks**. 
    Precios excelentes y servidores optimizados.
    """)
    st.link_button("Ver planes en V2 Networks 🇨🇱", "https://clientes.v2networks.cl/aff.php?aff=304")
    
    st.divider()

    # SECCIÓN: Apoyo / Ko-fi (Botón Estático)
    st.write("### ☕ ¿Te sirvió?")
    kofi_static_button = """
    <div style="text-align: center;">
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
        <script type='text/javascript'>
            kofiwidget2.init('Apóyame con un café', '#f45d22', 'Q5Q81VBM89');
            kofiwidget2.draw();
        </script>
    </div>
    """
    # Altura de 60px para que el botón no se corte
    components.html(kofi_static_button, height=60)
    st.caption("Hecho con ❤️ para la comunidad de LATAM.")

# --- CUERPO PRINCIPAL ---
st.title("🖼️ Optimizador de Imágenes WebP")
st.write("Convierte tus imágenes a WebP, redimensiónalas y optimízalas para Framer o WordPress en segundos.")

# Cargador de archivos
files = st.file_uploader("Arrastra tus archivos JPG o PNG", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    
    with st.status("Procesando imágenes...", expanded=True) as status:
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, file in enumerate(files):
                img = Image.open(file)
                
                # Redimensionar manteniendo la proporción (Aspect Ratio)
                if img.width > ancho_max:
                    w_percent = (ancho_max / float(img.width))
                    h_size = int((float(img.height) * float(w_percent)))
                    img = img.resize((ancho_max, h_size), Image.Resampling.LANCZOS)
                
                # Convertir a WebP en un buffer de memoria
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='WEBP', quality=calidad)
                
                # Guardar en el ZIP con nombre numerado
                zip_file.writestr(f"{i+1}.webp", img_byte_arr.getvalue())
        
        status.update(label="¡Optimización completa!", state="complete", expanded = False)

    st.success(f"✅ Se han optimizado {len(files)} imágenes.")
    
    # Botón de descarga del archivo final
    st.download_button(
        label="📥 Descargar todas en .ZIP",
        data=zip_buffer.getvalue(),
        file_name="imagenes_optimizadas.zip",
        mime="application/zip",
        use_container_width=True
    )

# --- PIE DE PÁGINA ---
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8em;">
    Optimizado para rendimiento Web | Desarrollado por Armando Rangel
</div>
""", unsafe_allow_html=True)
