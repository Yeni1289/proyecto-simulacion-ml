import os
import json
import base64
from nbformat import read

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'datasets')
TEMPLATES_OUT_DIR = os.path.join(BASE_DIR, 'notebook_site', 'templates', 'notebooks')
STATIC_OUT_DIR = os.path.join(BASE_DIR, 'notebook_site', 'static', 'notebooks')

TARGET_FILES = [
    '05_Regrecion_Loguistica.ipynb',
    '06_Visualizacion_DtaSet.ipynb',
    '07_Divicion_del_DataSet.ipynb',
    '08_Preparacion_del_DataSet.ipynb',
    '09_Creacion-de-Transformadores-y-Pipeline-Personalizados.ipynb',
    '10_Evalucion-de-Resultados.ipynb',
]


def ensure_dirs(path):
    os.makedirs(path, exist_ok=True)


def save_image(b64data, out_path):
    data = base64.b64decode(b64data.encode('utf-8'))
    with open(out_path, 'wb') as f:
        f.write(data)


def extract_outputs(nb_path, base_name):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = read(f, as_version=4)

    items = []
    static_dir = os.path.join(STATIC_OUT_DIR, base_name)
    ensure_dirs(static_dir)

    img_counter = 1
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            items.append({'type': 'markdown', 'content': cell.source})
        elif cell.cell_type == 'code':
            for output in cell.get('outputs', []) or []:
                data = output.get('data', {}) if isinstance(output, dict) else {}
                # images (png/jpeg)
                if 'image/png' in data:
                    fname = f'img_{img_counter}.png'
                    outpath = os.path.join(static_dir, fname)
                    save_image(data['image/png'], outpath)
                    items.append({'type': 'image', 'path': f'/static/notebooks/{base_name}/{fname}'})
                    img_counter += 1
                elif 'image/jpeg' in data:
                    fname = f'img_{img_counter}.jpg'
                    outpath = os.path.join(static_dir, fname)
                    save_image(data['image/jpeg'], outpath)
                    items.append({'type': 'image', 'path': f'/static/notebooks/{base_name}/{fname}'})
                    img_counter += 1
                # HTML output (tables rendered as HTML)
                elif 'text/html' in data:
                    html = data['text/html']
                    if isinstance(html, list):
                        html = ''.join(html)
                    items.append({'type': 'html', 'content': html})
                # plain text (streams or repr)
                elif 'text/plain' in data:
                    txt = data['text/plain']
                    if isinstance(txt, list):
                        txt = '\n'.join(txt)
                    items.append({'type': 'text', 'content': txt})
                elif output.get('output_type') == 'stream':
                    txt = output.get('text', '')
                    items.append({'type': 'text', 'content': txt})

    return items


def main():
    ensure_dirs(TEMPLATES_OUT_DIR)
    ensure_dirs(STATIC_OUT_DIR)

    for fname in TARGET_FILES:
        src = os.path.join(NOTEBOOKS_DIR, fname)
        if not os.path.exists(src):
            print(f'No existe: {src}  — la salto')
            continue
        base = os.path.splitext(fname)[0]
        print(f'Procesando {fname} → {base}')
        items = extract_outputs(src, base)
        out_json = os.path.join(TEMPLATES_OUT_DIR, f'{base}.json')
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f'Guardado metadata: {out_json}')


if __name__ == '__main__':
    main()

