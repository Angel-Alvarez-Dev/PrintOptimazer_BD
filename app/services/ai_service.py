import openai
import json
from typing import List
from app.core.config import settings
from app.schemas.ai_task import ComplexityReport, PrintTimeRequest, PrintTimeResponse


class AIServiceError(Exception):
    """Excepción genérica para errores en AIService"""
    pass


class AIService:
    """
    Servicio para interacción con motor de IA (OpenAI).
    Provee generación de títulos SEO, descripciones, tags,
    análisis de complejidad y predicción de tiempo de impresión.
    """
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"

    def generate_seo_title(self, model_id: str) -> str:
        """
        Genera un título optimizado para SEO a partir del ID del modelo 3D.
        """
        prompt = (
            f"Eres un experto en SEO para marketplaces de impresión 3D. "
            f"Genera un título breve (<= 60 caracteres) y muy atractivo para el modelo con ID: {model_id}."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
        except Exception as e:
            raise AIServiceError(f"Error en OpenAI generate_seo_title: {e}")

        choices = getattr(resp, 'choices', None)
        if not choices or not choices[0].message.content:
            raise AIServiceError("Respuesta vacía de OpenAI para generate_seo_title")

        return choices[0].message.content.strip()

    def generate_market_description(self, model_id: str) -> str:
        """
        Genera una descripción optimizada para marketplaces basada en el ID del modelo.
        """
        prompt = (
            f"Eres un copywriter especializado en marketplaces de impresión 3D. "
            f"Crea una descripción detallada (100-150 palabras) para el modelo con ID: {model_id}, "
            f"incluyendo beneficios, materiales sugeridos y público objetivo."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
        except Exception as e:
            raise AIServiceError(f"Error en OpenAI generate_market_description: {e}")

        content = getattr(resp.choices[0].message, 'content', '').strip()
        if not content:
            raise AIServiceError("Respuesta vacía de OpenAI para generate_market_description")

        return content

    def generate_tags(self, model_id: str) -> List[str]:
        """
        Genera una lista de tags relevantes para el modelo 3D.
        """
        prompt = (
            f"Como experto en SEO, sugiere entre 5 y 10 etiquetas descriptivas "
            f"para el modelo con ID: {model_id}. Responde en JSON con clave 'tags'."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
        except Exception as e:
            raise AIServiceError(f"Error en OpenAI generate_tags: {e}")

        text = resp.choices[0].message.content
        try:
            data = json.loads(text)
            tags = data.get("tags")
            if not isinstance(tags, list):
                raise ValueError
            return tags
        except Exception:
            raise AIServiceError("No se pudo parsear JSON de tags de OpenAI: " + text)

    def analyze_complexity(self, model_file_url: str) -> ComplexityReport:
        """
        Analiza la complejidad de un modelo 3D a partir de su URL.
        """
        prompt = (
            f"Analiza el modelo 3D en la URL: {model_file_url}. "
            f"Devuelve JSON con vertices (int), polygons (int), file_size_kb (float), complexity_score (float 0-1)."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return ComplexityReport.parse_raw(resp.choices[0].message.content)
        except Exception as e:
            raise AIServiceError(f"Error al parsear ComplexityReport: {e}")

    def predict_print_time(self, request: PrintTimeRequest) -> PrintTimeResponse:
        """
        Predice el tiempo de impresión (minutos) para un modelo 3D.
        """
        prompt = (
            f"Calcula tiempo de impresión para: URL={request.model_file_url}, "
            f"Material={request.material}, Layer={request.layer_height_mm}mm, Infill={request.infill_percent}%. "
            "Responde JSON con 'estimated_time_minutes'."
        )
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return PrintTimeResponse.parse_raw(resp.choices[0].message.content)
        except Exception as e:
            raise AIServiceError(f"Error al parsear PrintTimeResponse: {e}")