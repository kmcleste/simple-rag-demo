# Simple RAG Demo

## Getting Started

Install the project dependencies:

```shell
uv sync --frozen

# OR

poetry install
```

## Start Services

In two separate terminals, run `make llama` and `make api`. As is, the demo consumes 13GB of VRAM. If this is too much for your system, you can alter the max model length and gpu memory utilization settings in the [Makefile](./Makefile).

## Usage

You can access the vllm api at [http://127.0.0.1:8001](http://127.0.0.1:8001/docs) and the RAG api at [http://127.0.0.1:8000](http://127.0.0.1:8000/docs).
