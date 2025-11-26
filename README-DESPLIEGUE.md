# Guía de Despliegue Manual - Backend y Frontend en Azure

Esta guía te ayudará a desplegar el backend (FastAPI) y el frontend (Angular) en Azure usando el portal web, manteniendo la base de datos en Neon PostgreSQL.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración de Base de Datos (Neon)](#configuración-de-base-de-datos-neon)
3. [Despliegue del Backend (FastAPI)](#despliegue-del-backend-fastapi)
4. [Despliegue del Frontend (Angular)](#despliegue-del-frontend-angular)
5. [Configuración Final](#configuración-final)
6. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- Cuenta de Azure con suscripción activa
- Cuenta de Neon (https://neon.tech) con base de datos configurada
- Node.js y npm instalados (para el frontend)
- Python 3.8+ instalado (para el backend)

---

## Configuración de Base de Datos (Neon)

**Respuesta rápida:** Puedes mantener tu base de datos en Neon. NO necesitas usar Azure para la base de datos. Neon es suficiente y funciona perfectamente con Azure App Service.

### Pasos para configurar Neon:

1. Accede a tu cuenta de Neon
   - Ve a https://console.neon.tech
   - Inicia sesión en tu cuenta

2. Obtén la cadena de conexión
   - Selecciona tu proyecto
   - Ve a la sección "Connection Details"
   - Copia la cadena de conexión completa
   - Formato: `postgresql://usuario:password@host/database?sslmode=require`

3. Guarda la cadena de conexión
   - La usarás más adelante al configurar el backend en Azure

---

## Despliegue del Backend (FastAPI)

### Paso 1: Preparar el código del backend

1. Navega a la carpeta del backend:
   ```
   cd "03-Introduccion-ORM con fastAPI"
   ```

2. Verifica que tienes los siguientes archivos:
   - `main.py` (archivo principal)
   - `requirements.txt` (debe incluir gunicorn)
   - `startup.sh` (ya está creado)
   - `.deployment` (ya está creado)

3. Verifica que `requirements.txt` contiene gunicorn:
   ```
   gunicorn==21.2.0
   ```

### Paso 2: Crear Grupo de Recursos en Azure Portal

1. Abre tu navegador y ve a https://portal.azure.com
2. Inicia sesión con tu cuenta de Azure
3. En la barra de búsqueda superior, escribe "Grupos de recursos"
4. Haz clic en "Grupos de recursos"
5. Haz clic en el botón "+ Crear" (arriba a la izquierda)
6. Completa el formulario:
   - **Suscripción:** Selecciona tu suscripción
   - **Grupo de recursos:** Escribe `rg-proyecto-software` (o el nombre que prefieras)
   - **Región:** Selecciona la región más cercana (ej: Este de EE. UU.)
7. Haz clic en "Revisar + crear"
8. Haz clic en "Crear"
9. Espera a que se cree el grupo de recursos (aparecerá una notificación)

### Paso 3: Crear App Service Plan en Azure Portal

1. En la barra de búsqueda superior, escribe "App Service plans"
2. Haz clic en "App Service plans"
3. Haz clic en el botón "+ Crear" (arriba a la izquierda)
4. Completa el formulario:

   **Pestaña "Aspectos básicos":**
   - **Suscripción:** Selecciona tu suscripción
   - **Grupo de recursos:** Selecciona `rg-proyecto-software` (el que creaste antes)
   - **Nombre:** Escribe `plan-backend-fastapi`
   - **Sistema operativo:** Selecciona "Linux"
   - **Región:** Selecciona la misma región que el grupo de recursos
   - **Plan de tarifa:** Haz clic en "Cambiar tamaño y plan"
     - Selecciona "Básico B1" (o el plan que prefieras)
     - Haz clic en "Aplicar"

5. Haz clic en "Revisar + crear"
6. Haz clic en "Crear"
7. Espera a que se cree el plan (aparecerá una notificación)

### Paso 4: Crear App Service para el Backend en Azure Portal

1. En la barra de búsqueda superior, escribe "App Services"
2. Haz clic en "App Services"
3. Haz clic en el botón "+ Crear" (arriba a la izquierda)
4. Completa el formulario:

   **Pestaña "Aspectos básicos":**
   - **Suscripción:** Selecciona tu suscripción
   - **Grupo de recursos:** Selecciona `rg-proyecto-software`
   - **Nombre:** Escribe un nombre único, por ejemplo: `backend-fastapi-proyecto-2025`
     - IMPORTANTE: El nombre debe ser único en todo Azure
     - Solo letras minúsculas, números y guiones
   - **Publicar:** Selecciona "Código"
   - **Pila en tiempo de ejecución:** Selecciona "Python 3.11" (o la versión disponible)
   - **Sistema operativo:** Debe estar en "Linux" (se selecciona automáticamente)
   - **Región:** Selecciona la misma región que antes
   - **App Service Plan:** Selecciona `plan-backend-fastapi` (el que creaste antes)

5. Haz clic en "Revisar + crear"
6. Haz clic en "Crear"
7. Espera a que se cree el App Service (puede tardar 2-3 minutos)
8. Cuando termine, haz clic en "Ir al recurso"

### Paso 5: Configurar Variables de Entorno en Azure Portal

1. En la página del App Service que acabas de crear, en el menú lateral izquierdo, busca la sección "Configuración"
2. Haz clic en "Configuración"
3. Haz clic en la pestaña "Configuración de la aplicación"
4. Haz clic en "+ Nueva configuración de la aplicación"
5. Agrega la variable `DATABASE_URL`:
   - **Nombre:** `DATABASE_URL`
   - **Valor:** Pega tu cadena de conexión de Neon completa
     - Ejemplo: `postgresql://usuario:password@ep-xxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require`
6. Haz clic en "Aceptar"
7. Haz clic en "Guardar" (arriba)
8. Confirma haciendo clic en "Continuar"

### Paso 6: Configurar el Comando de Inicio en Azure Portal

1. En el menú lateral izquierdo del App Service, busca "Configuración"
2. Haz clic en "Configuración general"
3. Busca la sección "Comando de inicio"
4. En el campo "Comando de inicio", escribe:
   ```
   bash startup.sh
   ```
5. Haz clic en "Guardar" (arriba)
6. Confirma haciendo clic en "Continuar"

### Paso 7: Crear Archivo ZIP del Backend

1. Abre PowerShell o Terminal en la carpeta del backend:
   ```
   cd "03-Introduccion-ORM con fastAPI"
   ```

2. Crea un archivo ZIP con todos los archivos necesarios (excluyendo archivos innecesarios):
   
   **En Windows PowerShell:**
   ```powershell
   Compress-Archive -Path * -DestinationPath backend-deploy.zip -Exclude @('__pycache__','*.pyc','.env','.git','*.zip')
   ```

   **Nota:** Asegúrate de que el ZIP incluya:
   - `main.py`
   - `requirements.txt`
   - `startup.sh`
   - `.deployment`
   - Todas las carpetas: `apis/`, `auth/`, `crud/`, `database/`, `entities/`, `migrations/`
   - Todos los archivos `.py` necesarios

### Paso 8: Desplegar el Código desde Azure Portal

1. En el portal de Azure, ve a tu App Service (backend-fastapi-proyecto-2025)
2. En el menú lateral izquierdo, busca "Centro de implementación"
3. Haz clic en "Centro de implementación"
4. Selecciona la pestaña "Configuración"
5. En "Origen", selecciona "Carga local"
6. Haz clic en "Elegir archivo"
7. Selecciona el archivo `backend-deploy.zip` que creaste
8. Haz clic en "Guardar"
9. Espera a que se complete el despliegue (puede tardar 2-5 minutos)
10. Verás el progreso en la pestaña "Registros"

### Paso 9: Verificar el Despliegue del Backend

1. En el portal de Azure, en tu App Service, en el menú lateral izquierdo, haz clic en "Información general"
2. Copia la URL que aparece en "URL predeterminada" (algo como: `https://backend-fastapi-proyecto-2025.azurewebsites.net`)
3. Abre una nueva pestaña en tu navegador y pega la URL
4. Debes ver un JSON con información de la API
5. Prueba la documentación agregando `/docs` al final de la URL:
   - Ejemplo: `https://backend-fastapi-proyecto-2025.azurewebsites.net/docs`
   - Debe mostrar la documentación Swagger de FastAPI

### Paso 10: Revisar Logs si hay Problemas

1. En el portal de Azure, en tu App Service, en el menú lateral izquierdo, busca "Supervisión"
2. Haz clic en "Registro de transmisión"
3. Verás los logs en tiempo real
4. Si hay errores, aparecerán aquí

---

## Despliegue del Frontend (Angular)

### Paso 1: Preparar el código del frontend

1. Navega a la carpeta del frontend:
   ```
   cd "04-Frontend-angular"
   ```

2. Actualiza el archivo `environment.prod.ts`:
   - Abre `src/environments/environment.prod.ts`
   - Reemplaza `'https://your-api-domain.com'` con la URL real de tu backend en Azure
   - Ejemplo: `apiUrl: 'https://backend-fastapi-proyecto-2025.azurewebsites.net'`
   - IMPORTANTE: No incluyas `/api` al final, solo la URL base

3. Instala las dependencias (si no lo has hecho):
   ```
   npm install
   ```

4. Verifica que `server.js` existe en la raíz del proyecto (ya está creado)

### Paso 2: Construir el proyecto para producción

1. En la carpeta del frontend, ejecuta:
   ```
   npm run build:prod
   ```
   
   O si no funciona:
   ```
   npm run build -- --configuration production
   ```

2. Esto creará una carpeta `dist/` con los archivos optimizados

3. Verifica que la carpeta `dist/frontend-angular-clean-architecture/` existe y contiene archivos

### Paso 3: Crear App Service para el Frontend en Azure Portal

1. En el portal de Azure, en la barra de búsqueda superior, escribe "App Services"
2. Haz clic en "App Services"
3. Haz clic en el botón "+ Crear" (arriba a la izquierda)
4. Completa el formulario:

   **Pestaña "Aspectos básicos":**
   - **Suscripción:** Selecciona tu suscripción
   - **Grupo de recursos:** Selecciona `rg-proyecto-software` (el mismo que antes)
   - **Nombre:** Escribe un nombre único, por ejemplo: `frontend-angular-proyecto-2025`
     - IMPORTANTE: El nombre debe ser único en todo Azure
   - **Publicar:** Selecciona "Código"
   - **Pila en tiempo de ejecución:** Selecciona "Node 18 LTS" (o la versión disponible)
   - **Sistema operativo:** Debe estar en "Linux"
   - **Región:** Selecciona la misma región que antes
   - **App Service Plan:** Puedes reutilizar `plan-backend-fastapi` o crear uno nuevo
     - Para crear uno nuevo, haz clic en "Crear nuevo" y sigue los mismos pasos del backend

5. Haz clic en "Revisar + crear"
6. Haz clic en "Crear"
7. Espera a que se cree el App Service
8. Cuando termine, haz clic en "Ir al recurso"

### Paso 4: Configurar el Comando de Inicio del Frontend en Azure Portal

1. En el portal de Azure, en tu App Service del frontend, en el menú lateral izquierdo, busca "Configuración"
2. Haz clic en "Configuración general"
3. Busca la sección "Comando de inicio"
4. En el campo "Comando de inicio", escribe:
   ```
   node server.js
   ```
5. Haz clic en "Guardar" (arriba)
6. Confirma haciendo clic en "Continuar"

### Paso 5: Crear Archivo ZIP del Frontend

1. Abre PowerShell o Terminal en la carpeta del frontend:
   ```
   cd "04-Frontend-angular"
   ```

2. Crea un archivo ZIP con los archivos necesarios:

   **En Windows PowerShell:**
   ```powershell
   Compress-Archive -Path dist,server.js,package.json,package-lock.json -DestinationPath frontend-deploy.zip
   ```

   **Nota:** Asegúrate de que el ZIP incluya:
   - Carpeta `dist/` completa (con `frontend-angular-clean-architecture/` dentro)
   - `server.js`
   - `package.json`
   - `package-lock.json`

### Paso 6: Desplegar el Frontend desde Azure Portal

1. En el portal de Azure, ve a tu App Service del frontend
2. En el menú lateral izquierdo, busca "Centro de implementación"
3. Haz clic en "Centro de implementación"
4. Selecciona la pestaña "Configuración"
5. En "Origen", selecciona "Carga local"
6. Haz clic en "Elegir archivo"
7. Selecciona el archivo `frontend-deploy.zip` que creaste
8. Haz clic en "Guardar"
9. Espera a que se complete el despliegue (puede tardar 2-5 minutos)
10. Verás el progreso en la pestaña "Registros"

### Paso 7: Verificar el Despliegue del Frontend

1. En el portal de Azure, en tu App Service del frontend, en el menú lateral izquierdo, haz clic en "Información general"
2. Copia la URL que aparece en "URL predeterminada"
3. Abre una nueva pestaña en tu navegador y pega la URL
4. Debe cargar la aplicación Angular
5. Prueba hacer login y verificar que se conecta al backend

---

## Configuración Final

### 1. Actualizar CORS en el Backend

Asegúrate de que el backend permita peticiones desde el frontend:

1. Obtén la URL del frontend desde el portal de Azure (en "Información general" del App Service del frontend)

2. Edita el archivo `main.py` del backend localmente:
   - Abre `03-Introduccion-ORM con fastAPI/main.py`
   - Busca la sección de CORS (alrededor de la línea 22)
   - Actualiza `allow_origins` con la URL real del frontend:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://frontend-angular-proyecto-2025.azurewebsites.net",  # URL de tu frontend
           "http://localhost:4200"  # Para desarrollo local
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. Crea un nuevo ZIP del backend con este cambio

4. Vuelve a desplegar el backend siguiendo los pasos del "Paso 8: Desplegar el Código desde Azure Portal"

### 2. Verificar que todo funciona

1. **Backend:**
   - Abre la URL del backend en el navegador
   - Debe mostrar un JSON con información de la API
   - Prueba la documentación: `https://tu-backend.azurewebsites.net/docs`

2. **Frontend:**
   - Abre la URL del frontend en el navegador
   - Debe cargar la aplicación Angular
   - Prueba hacer login y verificar que se conecta al backend

3. **Base de datos:**
   - Verifica en Neon que las tablas existen
   - Prueba crear un usuario desde el frontend y verifica que se guarda en Neon

---

## Solución de Problemas

### Problema: El backend no inicia

**Solución:**
1. En el portal de Azure, ve a tu App Service del backend
2. En el menú lateral, haz clic en "Registro de transmisión" (en la sección "Supervisión")
3. Revisa los logs para ver el error específico
4. Verifica que:
   - La variable `DATABASE_URL` esté configurada correctamente (ve a "Configuración" > "Configuración de la aplicación")
   - El comando de inicio sea `bash startup.sh` (ve a "Configuración" > "Configuración general")
   - El archivo `startup.sh` esté en el ZIP desplegado

### Problema: Error 404 en el frontend al navegar

**Solución:**
- Verifica que el archivo `server.js` esté en el ZIP desplegado
- Verifica que el comando de inicio sea `node server.js`
- Verifica que la carpeta `dist/` esté completa en el ZIP

### Problema: CORS error

**Solución:**
1. Obtén la URL exacta del frontend desde el portal de Azure
2. Actualiza el CORS en `main.py` del backend con esa URL (incluyendo `https://`)
3. Vuelve a desplegar el backend

### Problema: No se conecta a la base de datos

**Solución:**
1. En el portal de Azure, ve a tu App Service del backend
2. Ve a "Configuración" > "Configuración de la aplicación"
3. Verifica que `DATABASE_URL` tenga el valor correcto de Neon
4. Verifica que la URL de Neon incluya `?sslmode=require` al final
5. Revisa los logs en "Registro de transmisión" para ver el error específico

### Problema: El frontend muestra errores de API

**Solución:**
1. Verifica que `environment.prod.ts` tenga la URL correcta del backend (sin `/api` al final)
2. Reconstruye el frontend: `npm run build:prod`
3. Crea un nuevo ZIP con los archivos actualizados
4. Vuelve a desplegar el frontend

### Problema: Error al desplegar el ZIP

**Solución:**
- Asegúrate de que el ZIP no esté vacío
- Verifica que todos los archivos necesarios estén incluidos
- Intenta crear el ZIP de nuevo
- Verifica que no excedas el tamaño máximo (generalmente 100MB)

---

## Resumen de URLs

Después del despliegue, tendrás estas URLs:

- **Backend API:** `https://tu-backend.azurewebsites.net`
- **Backend Docs:** `https://tu-backend.azurewebsites.net/docs`
- **Frontend:** `https://tu-frontend.azurewebsites.net`

Reemplaza `tu-backend` y `tu-frontend` con los nombres reales que usaste.

---

## Checklist Final

- [ ] Grupo de recursos creado en Azure
- [ ] App Service Plan creado
- [ ] Backend desplegado y accesible
- [ ] Variable DATABASE_URL configurada en Azure
- [ ] Frontend desplegado y accesible
- [ ] Base de datos en Neon configurada y funcionando
- [ ] CORS configurado correctamente
- [ ] Frontend se conecta al backend
- [ ] Puedo hacer login desde el frontend
- [ ] Los datos se guardan en Neon

---

## Notas Importantes

- La base de datos puede quedarse en Neon (no necesitas Azure para BD)
- Los nombres de App Services deben ser únicos en todo Azure
- Mantén las variables de entorno seguras (no las subas a Git)
- Revisa los costos de Azure regularmente en el portal
- Guarda las URLs de tus servicios para referencia futura

---

## Recursos Adicionales

- [Documentación de Azure App Service](https://docs.microsoft.com/azure/app-service/)
- [Documentación de Neon](https://neon.tech/docs)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Angular](https://angular.io/docs)
