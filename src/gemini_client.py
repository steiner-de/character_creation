"""Gemini AI client for character generation."""

import logging
from google.cloud import aiplatform

logger = logging.getLogger('character_creation')


def generate_from_prompt(
    project: str,
    location: str,
    model_name: str,
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 2048
) -> str:
    """Generate text from a Gemini/Vertex AI model.
    
    Args:
        project: GCP project ID
        location: Region (e.g., 'us-central1')
        model_name: Model name (e.g., 'text-bison@001')
        prompt: Input prompt
        temperature: Creativity level (0.0-1.0)
        max_output_tokens: Maximum response length
        
    Returns:
        Generated text from the model
    """
    logger.debug(f"Initializing Vertex AI with project={project}, location={location}")
    try:
        aiplatform.init(project=project, location=location)
        logger.debug(f"Loading model: {model_name}")
        model = aiplatform.TextGenerationModel.from_pretrained(model_name)
        
        logger.debug(f"Generating text with temperature={temperature}, max_tokens={max_output_tokens}")
        response = model.predict(
            prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )
        logger.debug("Generation completed successfully")
    except Exception as e:
        logger.error(f"Failed to generate text from Gemini: {e}")
        raise
    
    # Handle different response types
    if isinstance(response, str):
        logger.debug(f"Generated {len(response)} characters")
        return response
    
    text = getattr(response, 'text', None)
    if text:
        logger.debug(f"Generated {len(text)} characters")
        return text
    
    result = str(response)
    logger.debug(f"Generated {len(result)} characters")
    return result
