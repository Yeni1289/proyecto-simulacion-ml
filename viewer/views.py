import os
import json
import html as _html
from django.http import Http404
from django.shortcuts import render

# Intentar importar markdown; si no está instalado, usar un fallback seguro
try:
    import markdown as md
except Exception:
    md = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_NOTES_DIR = os.path.join(BASE_DIR, 'templates', 'notebooks')
STATIC_NOTES_DIR = os.path.join(BASE_DIR, 'static', 'notebooks')


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
