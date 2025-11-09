# <div align="center">LongRefiner | Hierarchical Document Refinement for Long-context Retrieval-augmented Generation</div>
<div align="center">

**This is a fork of the original [LongRefiner](https://github.com/jinjiajie/LongRefiner) repository with added support for Apple Silicon (macOS) and modernized dependency management using [uv](https://github.com/astral-sh/uv).**

</div>

<div align="center">
<p>
<a href="#️-installation">Installation</a> |
<a href="#-quick-start">Quick-Start</a> |
<a href="#-training">Training</a> |
<a href="#-evaluation">Evaluation</a> |
<a href='https://huggingface.co/collections/jinjiajie/longrefiner-683ac32af1dc861d4c5d00e2'>Huggingface Models</a>
</p>
</div>

## 🔍 Overview

LongRefiner is an efficient plug-and-play refinement system for long-context RAG applications. It achieves 10x compression while maintaining superior performance through hierarchical document refinement.

<div align="center">
<img src="/assets/main_figure.jpg" width="800px">
</div>

## ✨ Key Features of this Fork

*   **Cross-Platform Execution**: Run inference on both NVIDIA GPUs (via `vllm`) for high performance and Apple Silicon Macs (via Hugging Face `transformers`) for local development and debugging.
*   **Modern Dependency Management**: Utilizes `uv` and `pyproject.toml` for fast, reliable, and easy-to-manage dependency installation. This replaces `requirements.txt` for clearer separation of dependencies and better project structure.
*   **Original Features**: All original features of LongRefiner are preserved.

## 🛠️ Installation

This project uses `uv` for package management. If you don't have it, install it first:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, create a virtual environment and install the dependencies:
```bash
# Create venv
uv venv

# Activate venv
source .venv/bin/activate

# Install base dependencies (for Apple Silicon / CPU)
uv pip install -e .

# For NVIDIA GPU users, install with HPC extras for vllm
# This will automatically use the correct PyTorch version with CUDA support
uv pip install -e ".[vllm]"
```
> **Why `uv` and `pyproject.toml`?**
> Using a `pyproject.toml` file provides a standardized way to define project metadata and dependencies. `uv` is an extremely fast Python package installer and resolver that reads this file, making the process of setting up development environments significantly faster and more reliable than traditional methods.

## 🚀 Quick Start

You can download the pre-trained LoRA models from [here](https://huggingface.co/collections/jinjiajie/longrefiner-683ac32af1dc861d4c5d00e2).

### On Apple Silicon (macOS) or standard CPU/GPU machines

For local development or environments without `vllm`, use the `LongRefinerHF` class.

```python
import json
from longrefiner import LongRefinerHF # Use the Hugging Face-based refiner

# Initialize
# This will automatically run on MPS if available
refiner = LongRefinerHF(
    base_model_path="Qwen/Qwen2.5-3B-Instruct",
    query_analysis_module_lora_path="jinjiajie/Query-Analysis-Qwen2.5-3B-Instruct",
    doc_structuring_module_lora_path="jinjiajie/Doc-Structuring-Qwen2.5-3B-Instruct",
    global_selection_module_lora_path="jinjiajie/Global-Selection-Qwen2.5-3B-Instruct",
    score_model_name="bge-reranker-v2-m3",
    score_model_path="BAAI/bge-reranker-v2-m3",
)

# Load sample data
with open("assets/sample_data.json", "r") as f:
    data = json.load(f)
question = list(data.keys())[0]
document_list = list(data.values())[0]

# Process documents
refined_result = refiner.run(question, document_list, budget=2048)
print(refined_result)
```

### On HPC with NVIDIA GPUs (High-Performance)

For the best performance, use the original `LongRefiner` which leverages `vllm`.

```python
import json
from longrefiner import LongRefiner # The original vllm-based refiner

# Initialize
refiner = LongRefiner(
    base_model_path="Qwen/Qwen2.5-3B-Instruct",
    query_analysis_module_lora_path="jinjiajie/Query-Analysis-Qwen2.5-3B-Instruct",
    doc_structuring_module_lora_path="jinjiajie/Doc-Structuring-Qwen2.5-3B-Instruct",
    global_selection_module_lora_path="jinjiajie/Global-Selection-Qwen2.5-3B-Instruct",
    score_model_name="bge-reranker-v2-m3",
    score_model_path="BAAI/bge-reranker-v2-m3",
    max_model_len=25000,
)

# Load sample data
with open("assets/sample_data.json", "r") as f:
    data = json.load(f)
question = list(data.keys())[0]
document_list = list(data.values())[0]

# Process documents
refined_result = refiner.run(question, document_list, budget=2048)
print(refined_result)
```

## 📚 Training

Training remains unchanged. For training purposes, please additionally install the `Llama-Factory` framework by following the instructions in the [official repository](https://github.com/hiyouga/LLaMA-Factory):

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
uv pip install -e ".[torch,metrics]"
```

Before training, prepare the datasets for three tasks in JSON format. Reference samples can be found in the training_data folder. We use the `Llama-Factory` framework for training. After setting up the training data, run:

```bash
cd scripts/training
# Train query analysis module
llamafactory-cli train train_config_step1.yaml  
# Train doc structuring module
llamafactory-cli train train_config_step2.yaml  
# Train global selection module
llamafactory-cli train train_config_step3.yaml  
```

## 📊 Evaluation

Evaluation remains unchanged. We use the [FlashRAG framework](https://github.com/RUC-NLPIR/FlashRAG) for RAG task evaluation. Required files:

- Evaluation dataset (recommended to obtain from FlashRAG's [official repository](https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets))
- Retrieval results for each query in the dataset
- Model paths (same as above)

After preparation, configure the paths in `scripts/evaluation/run_eval.sh` and run:

```bash
cd scripts/evaluation
bash run_eval.sh
```


