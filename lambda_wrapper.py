import importlib.util
import sys
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar directorios al sys.path una sola vez al inicio usando rutas absolutas
# Usar __file__ para obtener la ruta del script actual, más confiable que getcwd()
project_root = os.path.dirname(os.path.abspath(__file__))
layers_dir = os.path.join(project_root, "layers", "shared")
src_dir = os.path.join(project_root, "src")

# Remover si ya existen para evitar duplicados
for path in [layers_dir, src_dir]:
    while path in sys.path:
        sys.path.remove(path)

# Agregar al inicio
sys.path.insert(0, src_dir)
sys.path.insert(0, layers_dir)

print(f"Lambda wrapper initialized - sys.path configuration:")
print(f"  Project root: {project_root}")
print(f"  Layers dir: {layers_dir}")
print(f"  Src dir: {src_dir}")
print(f"  sys.path[0]: {sys.path[0]}")
print(f"  sys.path[1]: {sys.path[1]}")

class MockContext:
    """Mock de contexto Lambda para desarrollo local"""
    def __init__(self):
        self.function_name = "local-function"
        self.function_version = "$LATEST"
        self.invoked_function_arn = "arn:aws:lambda:local:000000000000:function:local-function"
        self.memory_limit_in_mb = "512"
        self.aws_request_id = "local-request-id"
    
    def get_remaining_time_in_millis(self):
        return 300000  # 5 minutos

def ejecutar_lambda(dominio, accion, event, context):
    """
    Ejecuta una lambda dinámicamente.
    Los módulos ahora usan imports absolutos desde src/ y layers/shared/
    """
    # Si no hay contexto, crear uno mock
    if context is None:
        context = MockContext()
    
    try:
        lambda_path = os.path.join(project_root, f"src/domains/{dominio}/lambdas/{accion}/main.py")
        
        if not os.path.exists(lambda_path):
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Lambda no encontrada: {lambda_path}"})
            }
        
        # Log adicional para debugging
        if dominio == "sales" and accion == "get_sales":
            print(f"\n🔍 DEBUG SALES LAMBDA:")
            print(f"   Lambda path: {lambda_path}")
            print(f"   Event keys: {list(event.keys())}")
            print(f"   Query params: {event.get('queryStringParameters')}")
        
        # Cargar el módulo con un nombre único basado en timestamp para evitar caché
        import time
        module_name = f"lambda_{dominio}_{accion}_{int(time.time() * 1000000)}"
        
        spec = importlib.util.spec_from_file_location(module_name, lambda_path)
        module = importlib.util.module_from_spec(spec)
        
        # Registrar y ejecutar el módulo
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
            if dominio == "sales" and accion == "get_sales":
                print(f"   ✅ Módulo sales cargado exitosamente")
                print(f"   Handler disponible: {hasattr(module, 'lambda_handler')}")
        except ModuleNotFoundError as mnf:
            print(f"\n⚠️ ModuleNotFoundError durante la carga del módulo:")
            print(f"   Módulo faltante: {mnf.name}")
            print(f"   Mensaje: {str(mnf)}")
            print(f"   sys.path actual:")
            for i, p in enumerate(sys.path[:5]):
                print(f"     [{i}]: {p}")
            raise
        
        # Ejecutar lambda_handler
        if dominio == "sales" and accion == "get_sales":
            print(f"   🚀 Ejecutando lambda_handler de sales...")
        
        response = module.lambda_handler(event, context)
        
        if dominio == "sales" and accion == "get_sales":
            print(f"   ✅ Lambda_handler completado. Status: {response.get('statusCode')}")
        
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
