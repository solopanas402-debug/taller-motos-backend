import importlib.util
import sys
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar directorios al sys.path una sola vez al inicio usando rutas absolutas
project_root = os.path.abspath(os.getcwd())
layers_dir = os.path.join(project_root, "layers", "shared")
src_dir = os.path.join(project_root, "src")

# Remover si ya existen para evitar duplicados
for path in [layers_dir, src_dir]:
    while path in sys.path:
        sys.path.remove(path)

# Agregar al inicio
sys.path.insert(0, src_dir)
sys.path.insert(0, layers_dir)

print(f"Lambda wrapper initialized - sys.path[0:2]:")
print(f"  [0]: {sys.path[0]}")
print(f"  [1]: {sys.path[1]}")

def ejecutar_lambda(dominio, accion, event, context):
    """
    Ejecuta una lambda dinámicamente.
    Los módulos ahora usan imports absolutos desde src/ y layers/shared/
    """
    try:
        lambda_path = os.path.join(project_root, f"src/domains/{dominio}/lambdas/{accion}/main.py")
        
        if not os.path.exists(lambda_path):
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Lambda no encontrada: {lambda_path}"})
            }
        
        # Cargar el módulo con un nombre único basado en timestamp para evitar caché
        import time
        module_name = f"lambda_{dominio}_{accion}_{int(time.time() * 1000000)}"
        
        spec = importlib.util.spec_from_file_location(module_name, lambda_path)
        module = importlib.util.module_from_spec(spec)
        
        # Registrar y ejecutar el módulo
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Ejecutar lambda_handler
        response = module.lambda_handler(event, context)
        
        # Limpiar el módulo después de usarlo
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        return response
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n{'='*60}")
        print(f"❌ ERROR ejecutando lambda {dominio}/{accion}")
        print(f"{'='*60}")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print(f"\nTraceback completo:")
        print(error_trace)
        print(f"{'='*60}\n")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error ejecutando lambda: {str(e)}"})
        }
