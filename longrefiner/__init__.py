import os

__version__ = "0.0.1"

# Make both backends available for explicit import
from .refiner_hf import LongRefinerHF

try:
    from .refiner import LongRefiner as LongRefinerVLLM

    VLLM_AVAILABLE = True
except ImportError:
    LongRefinerVLLM = None
    VLLM_AVAILABLE = False


# Determine which class to alias as the default `LongRefiner`
backend = os.environ.get("LONGREFINER_BACKEND")

if backend == "vllm":
    if not VLLM_AVAILABLE:
        raise ImportError(
            "LONGREFINER_BACKEND is set to 'vllm', but it could not be imported. "
            "Ensure vllm and its dependencies are installed (e.g., `uv pip install -e '.[vllm]'`)."
        )
    LongRefiner = LongRefinerVLLM
elif backend == "hf":
    LongRefiner = LongRefinerHF
elif backend is None:
    # Auto-detection: prefer vllm if available, otherwise fallback to hf
    if VLLM_AVAILABLE:
        print("Detected vLLM backend, using LongRefinerVLLM. Set LONGREFINER_BACKEND='hf' to override.")
        LongRefiner = LongRefinerVLLM
    else:
        print("vLLM not found, using Hugging Face backend (LongRefinerHF).")
        LongRefiner = LongRefinerHF
else:
    raise ValueError(f"Invalid LONGREFINER_BACKEND: '{backend}'. Choose from 'vllm' or 'hf'.")

# Expose for `from longrefiner import *`
__all__ = ["LongRefiner", "LongRefinerHF", "LongRefinerVLLM"]