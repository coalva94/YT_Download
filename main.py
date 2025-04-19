import yt_dlp
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os


# Crear la ventana principal
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("410x410")
root.resizable(False, False)



def ruta_recurso(rel_path):
    try:
        base_path = sys._MEIPASS  # Cuando se ejecuta como binario
    except AttributeError:
        base_path = os.path.abspath(".")  # Cuando se ejecuta como script

    return os.path.join(base_path, rel_path)

# Cargar la imagen PNG
image_path = ruta_recurso('images/banner.png')
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)


#Logo
path = ruta_recurso('images/alvabits.png')  # Reemplázalo con la ruta de tu imagen
logo = Image.open(path)
logo = ImageTk.PhotoImage(logo)


# Crear un widget Label para mostrar la imagen
image_label = tk.Label(root, image=image)
image_label.pack()
ttk.Label(root, text="Descarga audios o videos de Youtube:").pack()


# Funciones
#Explorador de carpetas
selected_folder = os.getcwd()
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_folder)
        path_entry.configure(foreground="black") 
                
        
 # Diccionario para convertir resoluciones de "ancho x alto" a estándar (360p, 720p, etc.)
resolution_map = {
    "3840x2160": "2160p",
    "2560x1440": "1440p",
    "1920x1080": "1080p",
    "1280x720": "720p",
    "854x480": "480p",
}       
   
        
selected_format_id = tk.StringVar(value='')

               
def list_formats(url):
    """Muestra una lista filtrada de formatos estándar sin repetidos y permite descargar"""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)  # Obtener info sin descargar
            formats = info.get('formats', [])

            format_dict = {}  # Diccionario para evitar resoluciones repetidas

            for f in formats:
                raw_resolution = f.get('resolution', 'Desconocida')  # Ej. "640x360"
                standard_resolution = resolution_map.get(raw_resolution, raw_resolution)  # Convertir a 360p, 720p...

                ext = f['ext']  # Obtener formato (mp4, webm, etc.)
                format_id = f['format_id']  # ID del formato

                # Solo guardar una versión por resolución (priorizando mp4)
                if standard_resolution not in format_dict or ext == 'mp4':
                    format_dict[standard_resolution] = (format_id, ext)

            # Ordenar según calidad (de mayor a menor)
            quality_order = ["2160p", "1440p", "1080p", "720p", "480p"]
            available_formats = {}
            radio = ttk.Frame(root)   
            radio.pack(anchor="center", padx=2, pady=5)
            ttk.Label(radio, text="Elije la calidad:").pack(pady=5) 
            for resolution in quality_order:
                if resolution in format_dict:
                    format_id, ext = format_dict[resolution]
                    available_formats[format_id] = resolution  # Guardar formato disponible
                    print(f"{format_id} | {ext}  | {resolution}")                                             
                    ttk.Radiobutton(radio, text=resolution, variable=selected_format_id, value=format_id).pack(side='left', padx = 5)     
            return available_formats # Retornar los formatos disponibles

    except Exception:
        ttk.Label(root, text="❌ Error al obtener formatos").pack(pady=5)     
        return None        

               
# Descargar solo audio
def descargar_audio(url, folder):
    """Descarga el audio"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("✅ Descarga completada")

    except Exception as e:
        print(f"❌ Error al descargar el audio: {e}")
        return None
    
    
# Botón para iniciar la descarga (video)
def button_download():
    download_button = ttk.Button(root, text="Descargar video", command=lambda: download_video(url_entry.get(), selected_format_id.get(), selected_folder ))
    download_button.pack(pady=5)
    
      
# Variable para la barra de progreso
#progress_var = IntVar()  # Variable que controlará el progreso (0-100)

# Hook de progreso para actualizar la barra
'''def progress_hook(d):
    if d['status'] == 'downloading':
        # Obtener el porcentaje descargado
        percent = d.get('_percent_str', '0.0%').strip('%')
        progress_var.set(int(float(percent)))       '''
      
      
      
def download_video(url, format_id, folder):
    """Descarga el video con el formato seleccionado"""
    ydl_opts = {
        'format': f'{format_id}+ba/b',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        print(f"❌ Error al descargar el video:{e} ")   
   
  

# Label para link
ttk.Label(root, text="Ingrese el enlace:").pack(pady=5)
url_entry = ttk.Entry(root, width=80)
url_entry.pack(padx=2)


# Botón para abrir explorador de carpetas 
carpeta = ttk.Frame(root)
carpeta.pack(anchor="center", pady=5, padx = 2)
ttk.Label(carpeta, text="Ubicacion del archivo:").pack(pady=5)
path_entry = ttk.Entry(carpeta, width=37)
path_entry.pack(side = 'left')
path_entry.insert(0, selected_folder)
path_entry.configure(foreground="gray") 
ttk.Button(carpeta, text = '📂',command=select_folder).pack(side = 'left', pady = 5)


#Botones de calidades (video) y descarga (audio)
botones = ttk.Frame(root)
botones.pack(anchor="center")
# Crear el botón inicial
ttk.Button(botones, text="Calidades disponibles (videos)", command=lambda:(list_formats(url_entry.get()), button_download())).pack(side = 'left')
# Descargar solo audio
ttk.Button(botones, text="Descargar solo audio", command=lambda:descargar_audio(url_entry.get(),selected_folder)).pack(side = 'left')



#Logo
image_logo = tk.Label(root, image=logo)
image_logo.pack(side='bottom', padx=2, pady=5)


'''
#Barra de progreso
# Barra de progreso
bar = ttk.Frame(root)
bar.pack(anchor="center", pady=5)
ttk.Progressbar(bar, length=390, variable=progress_var, maximum=100).pack(pady=5)


'''

if __name__ == "__main__":
    root.mainloop()

