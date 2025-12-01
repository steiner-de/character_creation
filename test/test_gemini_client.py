"""Test script for updated GeminiClient using vertexai library."""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_client import GeminiClient

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_gemini')


def test_imports():
    """Test that all imports work correctly."""
    print("\n[TEST] Checking imports...")
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        print("[OK] All imports successful")
        print(f"     - vertexai: {vertexai.__version__ if hasattr(vertexai, '__version__') else 'installed'}")
        return True
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False


def test_client_initialization():
    """Test GeminiClient initialization."""
    print("\n[TEST] Testing GeminiClient initialization...")
    try:
        client = GeminiClient(
            project="test-project",
            location="us-central1",
            model_name="gemini-1.5-flash"
        )
        print("[OK] GeminiClient initialized successfully")
        print(f"     - Project: {client.project}")
        print(f"     - Location: {client.location}")
        print(f"     - Model: {client.model_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize GeminiClient: {e}")
        return False


def test_set_methods():
    """Test setter methods."""
    print("\n[TEST] Testing setter methods...")
    try:
        client = GeminiClient("proj1", "us-central1", "gemini-1.5-flash")
        
        client.set_project("proj2")
        assert client.project == "proj2"
        print("[OK] set_project() works")
        
        client.set_location("europe-west1")
        assert client.location == "europe-west1"
        print("[OK] set_location() works")
        
        client.set_model("gemini-2.0-flash")
        assert client.model_name == "gemini-2.0-flash"
        print("[OK] set_model() works")
        
        client.reset()
        assert client._model is None
        print("[OK] reset() works")
        
        return True
    except Exception as e:
        print(f"[ERROR] Setter methods test failed: {e}")
        return False


def test_backward_compatibility():
    """Test backward compatibility function."""
    print("\n[TEST] Testing backward compatibility function...")
    try:
        from gemini_client import generate_from_prompt
        print("[OK] generate_from_prompt function exists")
        print("[OK] Backward compatibility maintained")
        return True
    except ImportError as e:
        print(f"[ERROR] Backward compatibility failed: {e}")
        return False


def test_extract_text():
    """Test _extract_text static method with mock responses."""
    print("\n[TEST] Testing _extract_text method...")
    try:
        # Test with string
        result = GeminiClient._extract_text("Hello world")
        assert result == "Hello world"
        print("[OK] String response handling works")
        
        # Test with mock object
        class MockResponse:
            text = "Generated text"
        
        result = GeminiClient._extract_text(MockResponse())
        assert result == "Generated text"
        print("[OK] Object with .text attribute works")
        
        return True
    except Exception as e:
        print(f"[ERROR] _extract_text test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("GeminiClient (vertexai) Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Client Initialization": test_client_initialization(),
        "Setter Methods": test_set_methods(),
        "Backward Compatibility": test_backward_compatibility(),
        "Extract Text": test_extract_text(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "[OK]" if passed else "[FAILED]"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] All tests passed!")
    else:
        print("[ERROR] Some tests failed!")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
