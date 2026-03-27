import streamlit as st
from PIL import Image
import zipfile
import io

# Configuración de la página
st.set_page_config(page_title="Optimizador WebP | Armando Rangel", page_icon="🖼️")

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

    # SECCIÓN: Apoyo / Ko-fi (VERSIÓN IMAGEN - 100% VISIBLE)
    st.write("### ☕ ¿Te sirvió?")
    
    # Link directo y botón oficial de Ko-fi
    kofi_link = "https://ko-fi.com/armandorangel76306"
    kofi_img_url = "https://storage.ko-fi.com/cdn/kofiv2.png"
    
    st.markdown(f'''
        <a href="{kofi_link}" target="_blank">
            <img src="{kofi_img_url}" style="border:0px;width:100%;" alt="Invítame un café en ko-fi.com" />
        </a>
    ''', unsafe_allow_html=True)
    
    st.caption("Apoya este proyecto para seguir creando herramientas gratuitas.")

# --- CUERPO PRINCIPAL ---
st.title("🖼️ Optimizador de Imágenes WebP")
st.write("Convierte tus imágenes a WebP, redimensiónalas y optimízalas para Framer o WordPress en segundos.")

# Cargador de archivos
files = st.file_uploader("Arrastra tus archivos JPG o PNG", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    
    # Barra de estado moderna
    with st.status("Procesando imágenes...", expanded=True) as status:
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, file in enumerate(files):
                img = Image.open(file)
                
                # Redimensionar manteniendo la proporción
                if img.width > ancho_max:
                    w_percent = (ancho_max / float(img.width))
                    h_size = int((float(img.height) * float(w_percent)))
                    img = img.resize((ancho_max, h_size), Image.Resampling.LANCZOS)
                
                # Convertir a WebP en memoria
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='WEBP', quality=calidad)
                
                # Guardar en el ZIP
                zip_file.writestr(f"optimizada_{i+1}.webp", img_byte_arr.getvalue())
        
        status.update(label="¡Optimización completa!", state="complete", expanded=False)

    st.success(f"✅ Se han optimizado {len(files)} imágenes.")
    
    # Botón de descarga
    st.download_button(
        label="📥 Descargar todas en .ZIP",
        data=zip_buffer.getvalue(),
        file_name="imagenes_optimizadas_Rangel.zip",
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
