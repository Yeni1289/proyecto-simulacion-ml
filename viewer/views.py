import os
import json
import html as _html
import base64
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

try:
    from nbformat import read as nb_read
except ImportError:
    nb_read = None

# Intentar importar markdown; si no está instalado, usar un fallback seguro
try:
    import markdown as md
except Exception:
    md = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_NOTES_DIR = os.path.join(BASE_DIR, 'templates', 'notebooks')
STATIC_NOTES_DIR = os.path.join(BASE_DIR, 'static', 'notebooks')
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

# Crear carpeta de datasets si no existe
if not os.path.exists(DATASETS_DIR):
    os.makedirs(DATASETS_DIR)


def index(request):
    files = []
    if os.path.isdir(TEMPLATES_NOTES_DIR):
        for fname in sorted(os.listdir(TEMPLATES_NOTES_DIR)):
            if fname.lower().endswith('.json'):
                base = os.path.splitext(fname)[0]
                if any(base.startswith(prefix) for prefix in ('05_', '06_', '07_', '08_', '09_', '10_')):
                    thumb = None
                    static_dir = os.path.join(STATIC_NOTES_DIR, base)
                    if os.path.isdir(static_dir):
                        for f in sorted(os.listdir(static_dir)):
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                                thumb = f'/static/notebooks/{base}/{f}'
                                break
                    title = base.replace('_', ' ')
                    files.append({'base': base, 'title': title, 'thumb': thumb})
    return render(request, 'index.html', {'files': files})


def notebook_view(request, filename):
    base = os.path.basename(filename)
    json_path = os.path.join(TEMPLATES_NOTES_DIR, f'{base}.json')
    if not os.path.exists(json_path):
        raise Http404('Notebook no encontrada')
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    title = base.replace('_', ' ')
    # extraer primer markdown como resumen completo (convertir a HTML)
    summary = None
    sections = []  # recoger encabezados '##' / '###' como secciones
    # Buscar el primer markdown que usaremos como resumen y quitarlo de la lista
    for idx, it in enumerate(items):
        if it.get('type') == 'markdown' and it.get('content'):
            raw = it.get('content')
            # extraer encabezados secundarios (##, ###) para mostrar como secciones
            for ln in raw.splitlines():
                s = ln.strip()
                if s.startswith('##') or s.startswith('###'):
                    heading = s.lstrip('#').strip()
                    # filtrar encabezados demasiado genéricos o repetitivos
                    if not heading:
                        continue
                    bad = {'dataset', 'data set', 'datafiles', 'data files', 'data', 'descripcion', 'descripción', 'datos', 'data files', 'datafile'}
                    norm = heading.lower().replace(':', '').strip()
                    if any(norm == b or norm.startswith(b + ' ') for b in bad):
                        continue
                    if heading and heading not in sections:
                        sections.append(heading)

            # quitar encabezados markdown de primer nivel para evitar duplicados en el resumen
            lines = [ln for ln in raw.splitlines() if not ln.strip().startswith('#')]
            txt = '\n'.join(lines).strip()
            if txt:
                if md:
                    # convertir Markdown a HTML completo
                    try:
                        summary = md.markdown(txt, extensions=['extra', 'sane_lists'])
                    except Exception:
                        summary = '<p>' + _html.escape(txt).replace('\n\n', '</p><p>').replace('\n', '<br>') + '</p>'
                else:
                    # Fallback: escapar y convertir saltos de línea a <br>
                    summary = '<p>' + _html.escape(txt).replace('\n\n', '</p><p>').replace('\n', '<br>') + '</p>'
                # Eliminar el item markdown para que no se muestre otra vez en el bucle de outputs
                try:
                    items.pop(idx)
                except Exception:
                    pass
                break

    return render(request, 'notebook_detail.html', {'items': items, 'title': title, 'summary': summary, 'sections': sections})


def dataset_loader(request):
    """Vista para carga inicial de dataset"""
    return render(request, 'dataset_loader.html', {})


@require_http_methods(["POST"])
def list_files(request):
    """API endpoint para listar archivos de una carpeta"""
    try:
        folder_path = request.POST.get('folder_path', '')
        
        # Validación de seguridad: asegurarse de que no salga del directorio base
        if not folder_path:
            return JsonResponse({
                'success': False,
                'error': 'Ruta de carpeta requerida'
            })
        
        # Normalizar ruta
        full_path = os.path.normpath(os.path.join(folder_path))
        
        # Verificar que la carpeta existe
        if not os.path.isdir(full_path):
            return JsonResponse({
                'success': False,
                'error': 'Carpeta no encontrada'
            })
        
        files = []
        try:
            for item in sorted(os.listdir(full_path)):
                item_path = os.path.join(full_path, item)
                if os.path.isfile(item_path) and item.lower().endswith('.ipynb'):
                    size = os.path.getsize(item_path)
                    base, _ = os.path.splitext(item)
                    files.append({
                        'name': item,
                        'path': item_path,
                        'size': size,
                        'type': 'notebook',
                        'slug': base,  # para abrir en /notebook/<slug>
                    })
        except PermissionError:
            return JsonResponse({
                'success': False,
                'error': 'Permiso denegado para acceder a la carpeta'
            })
        
        return JsonResponse({
            'success': True,
            'folder': full_path,
            'files': files
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
def open_notebook(request):
    """API endpoint para procesar y abrir un notebook desde cualquier ruta"""
    try:
        file_path = request.POST.get('file_path', '')
        
        if not file_path:
            return JsonResponse({
                'success': False,
                'error': 'Ruta de archivo requerida'
            })
        
        # Normalizar y validar ruta
        full_path = os.path.normpath(file_path)
        
        if not os.path.isfile(full_path):
            return JsonResponse({
                'success': False,
                'error': 'Archivo no encontrado'
            })
        
        if not full_path.lower().endswith('.ipynb'):
            return JsonResponse({
                'success': False,
                'error': 'Solo se aceptan archivos .ipynb'
            })
        
        # Procesar el notebook
        try:
            base = os.path.splitext(os.path.basename(full_path))[0]
            
            # Crear carpetas de salida si no existen
            json_out_path = os.path.join(TEMPLATES_NOTES_DIR, f'{base}.json')
            static_out_dir = os.path.join(STATIC_NOTES_DIR, base)
            os.makedirs(static_out_dir, exist_ok=True)
            
            # Leer notebook
            with open(full_path, 'r', encoding='utf-8') as f:
                nb = nb_read(f, as_version=4)
            
            # Extraer outputs
            items = []
            img_counter = 0
            
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    content = ''.join(cell.source)
                    if content.strip():
                        items.append({'type': 'markdown', 'content': content})
                
                elif cell.cell_type == 'code' and hasattr(cell, 'outputs'):
                    for output in cell.outputs:
                        # Imágenes
                        if hasattr(output, 'data') and 'image/png' in output.data:
                            img_counter += 1
                            img_filename = f'output_{img_counter}.png'
                            img_path = os.path.join(static_out_dir, img_filename)
                            
                            # Guardar imagen
                            img_data = base64.b64decode(output.data['image/png'])
                            with open(img_path, 'wb') as img_file:
                                img_file.write(img_data)
                            
                            items.append({
                                'type': 'image',
                                'path': f'/static/notebooks/{base}/{img_filename}'
                            })
                        
                        # HTML/tablas
                        elif hasattr(output, 'data') and 'text/html' in output.data:
                            html_content = ''.join(output.data['text/html'])
                            items.append({'type': 'html', 'content': html_content})
                        
                        # Texto plano
                        elif hasattr(output, 'text'):
                            text_content = ''.join(output.text)
                            if text_content.strip():
                                items.append({'type': 'text', 'content': text_content})
            
            # Guardar JSON
            with open(json_out_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            
            return JsonResponse({
                'success': True,
                'slug': base,
                'message': f'Notebook procesado: {base}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error procesando notebook: {str(e)}'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
