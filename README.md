```markdown
# PrintOptimizer_BD

![PrintOptimizer Logo](/static/logo.svg)

**PrintOptimizer_BD** es una herramienta de gestión de proyectos de impresión 3D, orientada a automatizar la generación de descripciones, análisis de costos, gestión de insumos y estadísticas de mercado. Es especialmente útil para diseñadores de modelos 3D y técnicos de producción que buscan optimizar y centralizar el flujo de trabajo.

## Tabla de Contenidos

- [Características del Proyecto](#características-del-proyecto)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Configuración Inicial](#configuración-inicial)
- [Ejecución](#ejecución)
- [Estructura de la Base de Datos](#estructura-de-la-base-de-datos)
- [Rutas de la API](#rutas-de-la-api)
- [Ejemplo de Uso](#ejemplo-de-uso)
- [Pruebas](#pruebas)
- [Contribuciones](#contribuciones)

---

## Características del Proyecto

### Usuarios Potenciales

- **Diseñadores/Creadores de Modelos 3D**: Profesionales o aficionados que desean automatizar descripciones, etiquetas y gestionar costos de insumos.
- **Gerentes/Técnicos de Producción**: Personal técnico que optimiza el uso de materiales, costos de impresión y generación de reportes de rentabilidad.

### Objetivos Principales

1. **Automatización de Metadatos**: Generación automática de descripciones, etiquetas y parámetros para proyectos de impresión 3D.
2. **Gestión de Insumos y Costos**: Registro de costos de materiales, energía y mano de obra para optimizar procesos de producción.
3. **Análisis de Mercado**: Visualización de estadísticas de rendimiento en plataformas de venta como Thingiverse, MyMiniFactory, y Cults3D.
4. **Optimización del Proceso de Subida**: Administración centralizada para cargar proyectos en múltiples plataformas de forma eficiente.

---

## Arquitectura del Proyecto

La arquitectura del proyecto está basada en **FastAPI** para el backend y la gestión de rutas de la API. **SQLAlchemy** es utilizado para la interacción con la base de datos, y **Alembic** facilita el control de versiones y migraciones de la base de datos. **PostgreSQL** es el sistema de gestión de bases de datos, alojado en un servidor de WSL para pruebas y desarrollo.

### Estructura del Proyecto

```plaintext
PrintOptimizer_BD/
├── app/
│   ├── main.py              # Archivo principal de FastAPI
│   ├── models.py            # Modelos de SQLAlchemy
│   ├── schemas.py           # Esquemas de Pydantic
│   ├── database.py          # Configuración de la conexión a la base de datos
│   ├── crud.py              # Operaciones CRUD de cada entidad
│   ├── populate_db.py       # Script para llenar la base de datos con datos de ejemplo
│   └── config.py            # Configuración y variables de entorno
├── migrations/              # Archivos de migración generados por Alembic
├── tests/                   # Pruebas unitarias y de integración
├── .gitignore               # Archivo de exclusión de Git
├── requirements.txt         # Lista de dependencias del proyecto
└── README.md                # Documentación del proyecto
```

---

## Configuración Inicial

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/PrintOptimizer_BD.git
   cd PrintOptimizer_BD
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en `config.py` o en un archivo `.env` para especificar la conexión a PostgreSQL.

4. Realiza las migraciones de base de datos:
   ```bash
   alembic upgrade head
   ```

5. (Opcional) Llena la base de datos con datos de ejemplo:
   ```bash
   python app/populate_db.py
   ```

---

## Ejecución

Inicia el servidor de desarrollo de FastAPI:

```bash
uvicorn PrintOptimazer_BD.app.main:app --reload --log-level debug
```

La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Estructura de la Base de Datos

El modelo de datos incluye las siguientes tablas principales:

- **Usuarios y Roles**: Administración de roles y permisos para la plataforma.
- **Proyectos**: Registro de proyectos de impresión 3D con detalles como nombre, descripción, categoría, y costos.
- **Estadísticas de Mercado**: Registro de visualizaciones, descargas y ventas, junto con estadísticas por región.
- **Historial de Costos de Proyectos**: Registro de costos de materiales, energía, mano de obra, y mantenimiento para cada proyecto.

---

## Rutas de la API

Las rutas de la API permiten gestionar las principales entidades del proyecto:

- **/users**: Gestión de usuarios (creación, actualización, consulta).
- **/projects**: Administración de proyectos de impresión (creación, edición, y listado).
- **/market-stats**: Registro y consulta de estadísticas de mercado.
- **/cost-history**: Registro y consulta del historial de costos de proyectos.

Para ver la documentación interactiva de la API, visita [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) una vez que el servidor esté en ejecución.

---

## Ejemplo de Uso

1. Crear un nuevo usuario:
   ```json
   POST /users
   {
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123"
   }
   ```

2. Crear un proyecto con descripción y categoría:
   ```json
   POST /projects
   {
       "name": "Modelo 3D de Ejemplo",
       "description": "Este es un modelo 3D de ejemplo para pruebas",
       "category_id": 1
   }
   ```

3. Registrar estadísticas de mercado para un proyecto:
   ```json
   POST /market-stats
   {
       "project_id": 1,
       "views": 100,
       "downloads": 10,
       "sales": 5,
       "revenue": 50.0,
       "platform_id": 2
   }
   ```

---

## Pruebas

Las pruebas unitarias y de integración se encuentran en la carpeta `tests/`. Para ejecutar las pruebas, usa:

```bash
pytest
```

---

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas colaborar, abre un **issue** o crea un **pull request**. Por favor, asegúrate de seguir las guías de estilo y documentar adecuadamente tus cambios.

---

Con esta estructura y funcionalidades, **PrintOptimizer_BD** busca facilitar la gestión de proyectos de impresión 3D, optimizando la carga y monitoreo de modelos en el mercado.
```