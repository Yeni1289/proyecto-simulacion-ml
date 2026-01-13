# 📊 Proyecto de Simulación - Machine Learning

Aplicación web Django para visualización interactiva de notebooks de Jupyter con análisis de Machine Learning aplicado a detección de intrusiones en redes.

## 🎯 Descripción

Este proyecto es una aplicación web desarrollada con Django que permite cargar, procesar y visualizar notebooks de Jupyter (.ipynb) de manera interactiva. El sistema está enfocado en mostrar métricas, gráficos y resultados de análisis de Machine Learning sin mostrar el código fuente, ideal para presentaciones y reportes.

## ✨ Características

- 📁 **Cargador de Datasets**: Interfaz para seleccionar carpetas con archivos .ipynb
- 🔄 **Procesamiento On-Demand**: Conversión automática de notebooks a formato JSON
- 📊 **Visualización de Métricas**: Muestra solo resultados, gráficos y tablas (sin código)
- 🎨 **Interfaz Responsive**: Diseño limpio y profesional
- 💾 **Persistencia Local**: Recuerda la última carpeta utilizada
- 🚀 **Fácil Despliegue**: Compatible con Heroku

## 🗂️ Estructura del Proyecto

```
notebook_site/
├── app/                          # Configuración principal de Django
│   ├── settings.py              # Configuración del proyecto
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # WSGI para producción
├── viewer/                       # Aplicación de visualización
│   ├── views.py                 # Vistas y APIs
│   └── urls.py                  # URLs de la aplicación
├── templates/                    # Plantillas HTML
│   ├── base.html               # Plantilla base
│   ├── dataset_loader.html     # Cargador de datasets
│   ├── index.html              # Lista de notebooks
│   ├── notebook_detail.html    # Visualización de notebook
│   └── notebooks/              # Notebooks procesados (JSON)
├── static/                       # Archivos estáticos
│   ├── css/
│   │   └── notebook_styles.css
│   └── notebooks/              # Imágenes extraídas
├── datasets/                     # Notebooks fuente (.ipynb)
├── convert_notebooks.py         # Script de conversión batch
├── requirements.txt             # Dependencias Python
├── Procfile                     # Configuración Heroku
└── manage.py                    # Comando Django
```

## 📚 Notebooks Incluidos

El proyecto incluye análisis completos de Machine Learning aplicado a ciberseguridad:

1. **05_Regrecion_Loguistica**: Detección de SPAM con Regresión Logística
2. **06_Visualizacion_DtaSet**: Exploración y visualización del dataset NSL-KDD
3. **07_Divicion_del_DataSet**: Técnicas de división de datos (train/test/validation)
4. **08_Preparacion_del_DataSet**: Limpieza y preparación de datos
5. **09_Creacion-de-Transformadores-y-Pipeline-Personalizados**: Pipelines de Scikit-learn
6. **10_Evalucion-de-Resultados**: Métricas y evaluación de modelos

## 🔧 Instalación

### Prerrequisitos

- Python 3.10+
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Yeni1289/proyecto-simulacion-ml.git
cd proyecto-simulacion-ml
```

2. **Crear entorno virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
cd notebook_site
pip install -r requirements.txt
```

4. **Configurar la base de datos**
```bash
python manage.py migrate
```

5. **Ejecutar el servidor**
```bash
python manage.py runserver
```

6. **Abrir en el navegador**
```
http://127.0.0.1:8000/
```

## 🚀 Uso

### Cargar Notebooks

1. Al iniciar la aplicación, verás la página del cargador de datasets
2. Ingresa la ruta de la carpeta que contiene tus archivos `.ipynb`
3. Haz clic en **"Explorar"** para listar los archivos disponibles
4. Haz clic en **"Abrir"** junto al notebook que deseas visualizar

### Visualizar Resultados

- La aplicación procesa el notebook automáticamente
- Muestra solo las salidas: gráficos, tablas, métricas y texto
- No muestra el código fuente de las celdas

### Conversión Batch (Opcional)

Para convertir todos los notebooks de una vez:

```bash
python convert_notebooks.py
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.2.10**: Framework web principal
- **nbformat**: Procesamiento de notebooks Jupyter
- **Gunicorn**: Servidor WSGI para producción
- **WhiteNoise**: Servir archivos estáticos

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript**: Interactividad
- **Fetch API**: Comunicación con el backend

### Machine Learning
- **Scikit-learn**: Algoritmos de ML
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Matplotlib**: Visualización

## 📊 Dataset

El proyecto utiliza el **ISCX NSL-KDD Dataset 2009** para análisis de detección de intrusiones en redes.

### Características del Dataset
- **125,973 registros** en total
- **42 características** por registro
- **Clases**: Normal y Anomalía (varios tipos de ataques)
- **Formato**: ARFF y CSV

### Referencia
```
M. Tavallaee, E. Bagheri, W. Lu, and A. Ghorbani, 
"A Detailed Analysis of the KDD CUP 99 Data Set," 
Second IEEE Symposium on Computational Intelligence for Security 
and Defense Applications (CISDA), 2009.
```

Más información: [UNB NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)

## 🌐 Despliegue en Heroku

El proyecto está listo para despliegue en Heroku:

```bash
# Login en Heroku
heroku login

# Crear aplicación
heroku create tu-app-nombre

# Deploy
git push heroku main

# Abrir en el navegador
heroku open
```

## 📁 APIs Disponibles

### `/api/list-files/`
**POST**: Lista archivos `.ipynb` en una carpeta

**Request Body:**
```json
{
  "folder_path": "C:/ruta/a/tus/notebooks"
}
```

**Response:**
```json
{
  "files": [
    {
      "name": "notebook.ipynb",
      "path": "C:/ruta/completa/notebook.ipynb",
      "size": 12345
    }
  ]
}
```

### `/api/open-notebook/`
**POST**: Procesa y abre un notebook

**Request Body:**
```json
{
  "notebook_path": "C:/ruta/completa/notebook.ipynb"
}
```

**Response:**
```json
{
  "success": true,
  "redirect_url": "/notebook/notebook_name.json/"
}
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

**Yeni1289**
- GitHub: [@Yeni1289](https://github.com/Yeni1289)
- Proyecto: [proyecto-simulacion-ml](https://github.com/Yeni1289/proyecto-simulacion-ml)

## 🙏 Agradecimientos

- Dataset NSL-KDD de la Universidad de New Brunswick
- Comunidad de Django y Scikit-learn
- Todos los colaboradores del proyecto

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
