import streamlit as st
from PIL import Image
import io
import zipfile
import streamlit.components.v1 as components
# Configuración de la página
st.set_page_config(page_title="Optimizador WebP Pro", page_icon="🖼️")

st.title("🖼️ Optimizador de Imágenes para Diseñadores")
st.markdown("""
Sube tus imágenes (JPG, PNG) y las convertiremos a **WebP** optimizado, 
cambiando el nombre a números y ajustando el tamaño automáticamente.
""")

# Barra lateral para ajustes
with st.sidebar:
    st.header("Configuración")
    ancho_max = st.slider("Ancho máximo (píxeles)", 800, 2560, 1920)
    calidad = st.slider("Calidad visual", 10, 100, 85)
st.divider()
    st.write("### 🚀 Hosting Recomendado")
    
    # Banner visual con estilo
    st.info("""
    **¿Buscas un Hosting rápido y con soporte real en Chile?**
    
    Para mis proyectos personales y de clientes uso **V2 Networks**. 
    Precios excelentes y servidores optimizados.
    """)
    
    # Botón de referido
    st.link_button("Ver planes en V2 Networks 🇨🇱", "https://clientes.v2networks.cl/aff.php?aff=304")
    
    st.caption("Al contratar desde este link, apoyas el mantenimiento de esta herramienta sin costo extra para ti. ¡Gracias!")
# Selector de archivos
archivos_subidos = st.file_uploader("Arrastra tus fotos aquí", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if archivos_subidos:
    st.write(f"✅ {len(archivos_subidos)} imágenes listas para procesar.")
    
    if st.button("🚀 Optimizar y Preparar Descarga"):
        # Creamos un archivo ZIP en memoria para no llenar el servidor de basura
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as csv_zip:
            
            progreso = st.progress(0)
            
            for i, archivo in enumerate(archivos_subidos):
                # Abrir imagen
                img = Image.open(archivo)
                
                # Redimensionar si es necesario
                ancho, alto = img.size
                if ancho > ancho_max:
                    nuevo_alto = int((ancho_max * alto) / ancho)
                    img = img.resize((ancho_max, nuevo_alto), Image.LANCZOS)
                
                # Preparar color
                if img.mode in ("P", "RGBA"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                
                # Guardar en memoria como WebP
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='WEBP', quality=calidad, method=6)
                
                # Agregar al ZIP con el nuevo nombre (1.webp, 2.webp...)
                nuevo_nombre = f"{i+1}.webp"
                csv_zip.writestr(nuevo_nombre, img_byte_arr.getvalue())
                
                # Actualizar barra de progreso
                progreso.progress((i + 1) / len(archivos_subidos))

        # Botón de descarga
        st.success("¡Optimización completada!")
        st.download_button(
            label="📥 Descargar todas las imágenes (.zip)",
            data=buf.getvalue(),
            file_name="imagenes_optimizadas.zip",
            mime="application/zip"
        )

# --- BOTÓN FLOTANTE DE KO-FI PERSONALIZADO ---
kofi_button = """
<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
<script>
  kofiWidgetOverlay.draw('armandorangel76306', {
    'type': 'floating-chat',
    'floating-chat.donateButton.text': '¿Te ahorré unos MB? ☕',
    'floating-chat.donateButton.background-color': '#f45d22',
    'floating-chat.donateButton.text-color': '#fff',
    'floating-chat.donateButton.font-family': 'Inter, sans-serif'
  });
  
  // Mensaje de bienvenida que aparece al abrir el chat
  window.addEventListener('load', function() {
    setTimeout(function() {
      var kofi_iframe = document.querySelector('iframe[id^="kofi-widget-overlay"]');
      if (kofi_iframe) {
        // Esto envía el mensaje de bienvenida personalizado al widget
        console.log("Widget de Ko-fi listo para los diseñadores");
      }
    }, 2000);
  });
</script>
"""

# Inyectamos el componente
import streamlit.components.v1 as components
components.html(kofi_button, height=0)
