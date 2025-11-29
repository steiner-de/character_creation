"""Gemini AI client for character generation."""

from google.cloud import aiplatform


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
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    
    response = model.predict(
        prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )
    
    # Handle different response types
    if isinstance(response, str):
        return response
    
    text = getattr(response, 'text', None)
    if text:
        return text
    
    return str(response)
