"""Gemini AI client for character generation."""

import logging
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel

logger = logging.getLogger('character_creation')


class GeminiClient:
    """Gemini/Vertex AI text generation client.
    
    Manages text generation requests to Gemini models with
    configurable temperature, token limits, and error handling.
    """

    def __init__(
        self,
        project: str,
        location: str,
        model_name: str
    ) -> None:
        """Initialize the Gemini client.
        
        Args:
            project: GCP project ID
            location: GCP region (e.g., 'us-central1')
            model_name: Gemini model name (e.g., 'gemini-2.5-flash')
        """
        self.project: str = project
        self.location: str = location
        self.model_name: str = model_name
        self._model: Optional[GenerativeModel] = None
        
        logger.debug(
            f"GeminiClient initialized with model: {model_name} "
            f"(project: {project}, location: {location})"
        )

    def _initialize_model(self) -> GenerativeModel:
        """Initialize the Vertex AI Generative model if not already loaded.
        
        Returns:
            The loaded GenerativeModel instance
            
        Raises:
            Exception: If model initialization fails
        """
        if self._model is not None:
            return self._model

        logger.debug(
            f"Initializing Vertex AI with project={self.project}, "
            f"location={self.location}"
        )
        try:
            vertexai.init(project=self.project, location=self.location)
            logger.debug(f"Loading model: {self.model_name}")
            self._model = GenerativeModel(self.model_name)
            logger.debug("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI model: {e}")
            raise

        return self._model

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ) -> str:
        """Generate text from a prompt using Gemini.
        
        Args:
            prompt: Input prompt for text generation
            temperature: Creativity level (0.0-1.0, default: 0.7)
            max_output_tokens: Maximum response length (default: 2048)
            
        Returns:
            Generated text from the model
            
        Raises:
            Exception: If text generation fails
        """
        logger.debug(
            f"Generating text with temperature={temperature}, "
            f"max_tokens={max_output_tokens}"
        )
        try:
            model = self._initialize_model()
            
            # Use the generative_models API
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_output_tokens,
                }
            )
            logger.debug("Generation completed successfully")
        except Exception as e:
            logger.error(f"Failed to generate text from Gemini: {e}")
            raise

        # Handle different response types
        text = self._extract_text(response)
        logger.debug(f"Generated {len(text)} characters")
        return text

    @staticmethod
    def _extract_text(response) -> str:
        """Extract text from Gemini response.
        
        Handles various response types from Vertex AI's generative models.
        
        Args:
            response: Response object from Vertex AI (ContentResponse)
            
        Returns:
            Extracted text string
        """
        if isinstance(response, str):
            return response

        # For generative_models API, response has .text attribute
        if hasattr(response, 'text') and response.text:
            return response.text
        
        # Handle candidates from generative API
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                parts = candidate.content.parts
                if parts and hasattr(parts[0], 'text'):
                    return parts[0].text

        return str(response)

    def set_model(self, model_name: str) -> None:
        """Change the Gemini model being used.
        
        Args:
            model_name: New model name (e.g., 'gemini-2.5-flash')
        """
        self.model_name = model_name
        self._model = None  # Reset loaded model
        logger.info(f"Model changed to: {model_name}")

    def set_location(self, location: str) -> None:
        """Change the GCP region.
        
        Args:
            location: New GCP region (e.g., 'us-central1')
        """
        self.location = location
        self._model = None  # Reset loaded model
        logger.info(f"Location changed to: {location}")

    def set_project(self, project: str) -> None:
        """Change the GCP project.
        
        Args:
            project: New GCP project ID
        """
        self.project = project
        self._model = None  # Reset loaded model
        logger.info(f"Project changed to: {project}")

    def reset(self) -> None:
        """Reset the cached model instance.
        
        Use this if you've changed project, location, or model name.
        The model will be reloaded on the next generation request.
        """
        self._model = None
        logger.debug("Model cache reset")


# Backward compatibility: Keep module-level function
def generate_from_prompt(
    project: str,
    location: str,
    model_name: str,
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 2048
) -> str:
    """Generate text from a Gemini/Vertex AI model.
    
    Deprecated: Use GeminiClient class instead.
    
    Args:
        project: GCP project ID
        location: Region (e.g., 'us-central1')
        model_name: Model name (e.g., 'gemini-2.5-flash')
        prompt: Input prompt
        temperature: Creativity level (0.0-1.0)
        max_output_tokens: Maximum response length
        
    Returns:
        Generated text from the model
    """
    client = GeminiClient(project, location, model_name)
    return client.generate(prompt, temperature, max_output_tokens)
