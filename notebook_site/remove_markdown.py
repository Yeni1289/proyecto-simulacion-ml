import json
import os

# Archivos a procesar
files = [
    'templates/notebooks/05_Regrecion_Loguistica.json',
    'templates/notebooks/06_Visualizacion_DtaSet.json',
    'templates/notebooks/07_Divicion_del_DataSet.json',
    'templates/notebooks/08_Preparacion_del_DataSet.json',
    'templates/notebooks/09_Creacion-de-Transformadores-y-Pipeline-Personalizados.json',
    'templates/notebooks/10_Evalucion-de-Resultados.json'
]

for file_path in files:
    try:
        # Leer el archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filtrar eliminando todas las entradas con type: markdown
        filtered_data = [entry for entry in data if entry.get('type') != 'markdown']
        
        # Guardar el archivo filtrado
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        
        print(f'✓ Procesado: {os.path.basename(file_path)} - Eliminados {len(data) - len(filtered_data)} elementos markdown')
    except Exception as e:
        print(f'✗ Error en {os.path.basename(file_path)}: {str(e)}')

print('\n✓ Proceso completado')
