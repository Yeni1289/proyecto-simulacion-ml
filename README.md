# Vista de Notebooks con Django

Pasos rápidos:

1. Crear entorno virtual e instalar dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```


2. Extraer sólo resultados (imágenes, tablas, textos) desde los notebooks y guardarlos como JSON + assets estáticos:

```bash
python convert_notebooks.py
```

Esto generará `notebook_site/templates/notebooks/05_....json` y las imágenes en `notebook_site/static/notebooks/05_/...`.

3. Ejecutar servidor Django:

```bash
python notebook_site/manage.py migrate
python notebook_site/manage.py runserver
```

4. Abrir http://127.0.0.1:8000/ y hacer clic en las notebooks (05-10) para ver sólo resultados (tablas, imágenes, gráficos) en una plantilla presentable.
