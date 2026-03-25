# Despliegue en Render

## Pasos para desplegar en Render

### 1. Preparar el repositorio
- Asegúrate de que todos los archivos estén en Git
- Incluye: `app.py`, `Procfile`, `requirements.txt`, `render.yaml`

### 2. Conectar a Render
1. Ve a https://render.com
2. Crea una cuenta o inicia sesión
3. Haz clic en "New +" → "Web Service"
4. Conecta tu repositorio de GitHub
5. Selecciona este repositorio

### 3. Configurar el servicio
- **Name**: motorcycle-repair-api
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 4. Agregar variables de entorno
En la sección "Environment", agrega:

```
DB_URL=https://toklwbqrgqsgaovzleev.supabase.co
DB_KEY=sb_publishable_9ToFd0mY6_QhXaGecuwxQA_ixnC9hQ0
```

### 5. Desplegar
- Haz clic en "Create Web Service"
- Render construirá e iniciará tu aplicación automáticamente

## URLs de los endpoints

Una vez desplegado, tus endpoints estarán disponibles en:

```
https://tu-servicio.onrender.com/customers
https://tu-servicio.onrender.com/repairs
https://tu-servicio.onrender.com/mechanics
https://tu-servicio.onrender.com/products
https://tu-servicio.onrender.com/cashboxes
https://tu-servicio.onrender.com/brands
```

## Verificar que funciona

```bash
curl https://tu-servicio.onrender.com/health
```

Deberías recibir:
```json
{"status": "ok"}
```

## Notas importantes

- El servidor se reiniciará automáticamente si hay cambios en el repositorio
- Los logs estarán disponibles en el dashboard de Render
- Render proporciona un dominio gratuito (*.onrender.com)
- Para dominio personalizado, configúralo en los settings del servicio

## Solución de problemas

Si hay errores de importación:
1. Verifica que la estructura de carpetas sea correcta
2. Revisa los logs en Render
3. Asegúrate de que todas las dependencias estén en `requirements.txt`
