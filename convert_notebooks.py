#!/usr/bin/env python
"""
Script para convertir notebooks de Jupyter a formato JSON
para visualización web sin mostrar código.
"""
import os
import json
import base64
from pathlib import Path

try:
    import nbformat
except ImportError:
    print("ERROR: nbformat no está instalado. Instala con: pip install nbformat")
    exit(1)

BASE_DIR = Path(__file__).resolve().parent
NOTEBOOKS_DIR = BASE_DIR / 'datasets'
OUTPUT_DIR = BASE_DIR / 'templates' / 'notebooks'
STATIC_DIR = BASE_DIR / 'static' / 'notebooks'

def extract_outputs(cell):
    """Extrae solo los outputs de una celda (sin código)."""
    outputs = []
    
    if 'outputs' not in cell:
        return outputs
    
    for output in cell['outputs']:
        if output['output_type'] == 'stream':
            outputs.append({
                'type': 'text',
                'content': output.get('text', '')
            })
        elif output['output_type'] == 'display_data':
            if 'image/png' in output['data']:
                outputs.append({
                    'type': 'image',
                    'content': output['data']['image/png']
                })
            elif 'text/html' in output['data']:
                outputs.append({
                    'type': 'html',
                    'content': output['data']['text/html']
                })
        elif output['output_type'] == 'execute_result':
            if 'image/png' in output['data']:
                outputs.append({
                    'type': 'image',
                    'content': output['data']['image/png']
                })
            elif 'text/html' in output['data']:
                outputs.append({
                    'type': 'html',
                    'content': output['data']['text/html']
                })
            elif 'text/plain' in output['data']:
                outputs.append({
                    'type': 'text',
                    'content': output['data']['text/plain']
                })
    
    return outputs

def process_notebook(notebook_path):
    """Procesa un notebook y retorna su contenido en JSON."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    items = []
    image_count = 0
    notebook_name = notebook_path.stem
    
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            items.append({
                'type': 'markdown',
                'content': cell.source
            })
        elif cell.cell_type == 'code':
            outputs = extract_outputs(cell)
            
            for output in outputs:
                if output['type'] == 'image':
                    image_count += 1
                    image_data = output['content']
                    
                    # Crear carpeta si no existe
                    static_notebook_dir = STATIC_DIR / notebook_name
                    static_notebook_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Guardar imagen
                    img_path = static_notebook_dir / f'img_{image_count}.png'
                    with open(img_path, 'wb') as img_file:
                        img_file.write(base64.b64decode(image_data))
                    
                    # Agregar referencia en JSON
                    items.append({
                        'type': 'image',
                        'content': f'/static/notebooks/{notebook_name}/img_{image_count}.png'
                    })
                else:
                    items.append(output)
    
    return items

def main():
    """Función principal."""
    if not NOTEBOOKS_DIR.exists():
        print(f"ERROR: La carpeta {NOTEBOOKS_DIR} no existe")
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    notebooks = list(NOTEBOOKS_DIR.glob('*.ipynb'))
    
    if not notebooks:
        print(f"No se encontraron notebooks en {NOTEBOOKS_DIR}")
        return
    
    print(f"Procesando {len(notebooks)} notebooks...")
    
    for notebook_path in sorted(notebooks):
        try:
            print(f"  • {notebook_path.name}...", end=' ')
            items = process_notebook(notebook_path)
            
            # Guardar JSON
            output_path = OUTPUT_DIR / f'{notebook_path.stem}.json'
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
            
            print(f"✓ ({len(items)} items)")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print(f"\n✓ Conversión completada. Archivos guardados en {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
