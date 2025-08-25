import os 
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'
import json
from longrefiner import LongRefiner

# Initialize
query_analysis_module_lora_path = "/model/step1_lora"
doc_structuring_module_lora_path = "/model/step2_lora"
selection_module_lora_path = "/model/step3_lora"

refiner = LongRefiner(
    base_model_path="/model/qwen2.5-3B-Instruct",
    query_analysis_module_lora_path=query_analysis_module_lora_path,
    doc_structuring_module_lora_path=doc_structuring_module_lora_path,
    global_selection_module_lora_path=selection_module_lora_path,
    score_model_name="bge-reranker-v2-m3",
    score_model_path="model/bge-reranker-v2-m3",
    max_model_len=25000,
)

# Load sample data
with open("sample_data.json", "r") as f:
    data = json.load(f)
question = list(data.keys())[0]
document_list = list(data.values())[0][:5]

# Process documents
refined_result = refiner.run(question, document_list, budget=2048)
print(refined_result)