import importlib.util
import sys
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def ejecutar_lambda(dominio, accion, event, context):
    """
    Ejecuta una lambda dinámicamente sin importaciones directas.
    """
    try:
        lambda_path = f"src/domains/{dominio}/lambdas/{accion}/main.py"
        
        if not os.path.exists(lambda_path):
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Lambda no encontrada: {lambda_path}"})
            }
        
        # Obtener directorios
        lambda_dir = os.path.dirname(os.path.abspath(lambda_path))
        parent_dir = os.path.dirname(lambda_dir)
        domain_dir = os.path.dirname(parent_dir)
        layers_dir = os.path.join(os.getcwd(), "layers", "shared")
        
        # Guardar sys.path y sys.modules originales
        original_path = sys.path.copy()
        original_modules = dict(sys.modules)
        
        try:
            # Limpiar sys.path pero mantener site-packages
            sys.path = [p for p in sys.path if 'site-packages' in p or 'dist-packages' in p]
            
            # Agregar paths en orden correcto
            sys.path.insert(0, lambda_dir)
            sys.path.insert(0, parent_dir)
            sys.path.insert(0, domain_dir)
            sys.path.insert(0, layers_dir)
            sys.path.insert(0, os.getcwd())
            
            # Cargar el módulo
            spec = importlib.util.spec_from_file_location(
                f"{dominio}_{accion}_main",
                lambda_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[module.__name__] = module
            
            # Ejecutar el módulo
            spec.loader.exec_module(module)
            
            # Ejecutar lambda_handler
            response = module.lambda_handler(event, context)
            return response
            
        finally:
            # Restaurar estado original
            sys.path = original_path
            # Limpiar solo los módulos que se cargaron (no los estándar)
            for mod_name in list(sys.modules.keys()):
                if mod_name not in original_modules and not mod_name.startswith('_'):
                    try:
                        del sys.modules[mod_name]
                    except:
                        pass
    
    except Exception as e:
        import traceback
        print(f"Error ejecutando lambda {dominio}/{accion}: {str(e)}")
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error ejecutando lambda: {str(e)}"})
        }
