# Flujo IA y Automatización

Este documento describe el flujo completo de la generación de metadatos de modelos 3D usando IA:

1. **Petición REST**  
   El cliente hace una llamada HTTP al endpoint correspondiente de la API:
   - `/api/v1/ai/seo/{model_id}`
   - `/api/v1/ai/description/{model_id}`
   - `/api/v1/ai/tags/{model_id}`
   - `/api/v1/ai/complexity/{model_id}`
   - `/api/v1/ai/print-time/{model_id}`

2. **Encolado de tarea Celery**  
   Cada endpoint utiliza:
   ```python
   task = <task_function>.delay(...)
