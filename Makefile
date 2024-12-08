llama:
	uv run vllm serve hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 --dtype auto --max-model-len 8192 --gpu-memory-utilization 0.95 --port 8001

api:
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000