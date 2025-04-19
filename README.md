# 🖼️ YouTube Download App Multiplataforma

Aplicación de escritorio hecha con **Python** y **Tkinter**, con compatibilidad para **macOS** y **Windows**.
> ✅ 100% gratuito, multiplataforma y de código abierto

---

## 🚀 Características principales

- 🔽 Descarga videos de YouTube en cualquier duración
- 📺 Soporta resoluciones desde 144p hasta 4K (cuando esté disponible)
- 🎧 Extrae solo audio (MP3)
- 🛠️ Compilación automática para Windows desde GitHub

---

## 📸 Captura de pantalla

> ![Vista previa de la app](assets/captura.png)

---

## ⚙️ Tecnologías usadas

- [Python](https://www.python.org/)
- [yt_dlp](https://github.com/yt-dlp/yt-dlp)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller](https://pyinstaller.org/)
- [GitHub Actions](https://github.com/features/actions)

---

## 🧩 Requisitos

- Python 3.12 o superior
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## 💻 Cómo usar

### 1. Clona este repositorio

```bash
git clone https://github.com/tu_usuario/YT_Download.git
cd YT_Download
```

### 2. Para generar el ejecutable en windows
```bash
pyinstaller main.py --name YT_Download --noconfirm --windowed --icon=images/icono.ico --add-data "images;images"
```

### 3. Para generar el ejecutable en MacOs
```bash
pyinstaller main.py --name YT_Download --noconfirm --windowed --icon=images/icon.icns --add-data "images:images"

```

### Descargar la versión para macOS y Windows

- [Descargar para macOS](https://github.com/coalva94/YT_Download/actions/artifacts/YT_Download-macOS)
- [Descargar para Windows](https://github.com/coalva94/YT_Download/actions/artifacts/YT_Download-Windows)
