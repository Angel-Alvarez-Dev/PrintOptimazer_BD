# PrintOptimizer_BD

![PrintOptimizer Logo](https://via.placeholder.com/150) <!-- Sustituye este link con el logo si tienes uno disponible -->

**PrintOptimizer_BD** es una herramienta de gestión de proyectos de impresión 3D, orientada a automatizar la generación de descripciones, análisis de costos, gestión de insumos y estadísticas de mercado, especialmente útil para diseñadores de modelos 3D y técnicos de producción.

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
2. **Gestión de Insumos y Costos**: Registro de costos de materiales, energía y mano de obra para optimizar procesos.
3. **Análisis de Mercado**: Visualización de estadísticas de rendimiento en plataformas de venta como Thingiverse, MyMiniFactory, y Cults3D.
4. **Optimización del Proceso de Subida**: Administración centralizada para cargar proyectos en múltiples plataformas.

---

## Arquitectura del Proyecto

La arquitectura del proyecto se basa en **FastAPI** como backend para las rutas de la API, **SQLAlchemy** para la gestión de la base de datos y **Alembic** para manejar migraciones. PostgreSQL es el sistema de gestión de base de datos, alojado en un servidor de WSL.

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
