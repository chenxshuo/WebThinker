#!/bin/bash


# # WebThinker + any dataset -> implement in run_web_thinker_report_brave_search.py
python scripts/question_run_web_thinker_report_brave_search.py \
   --dataset_name strongreject \
   --split question\
   --concurrent_limit 32 \
   --api_base_url "http://localhost:8000/v1" \
   --model_name "GAIR/DeepResearcher-7b" \
   --aux_api_base_url "http://localhost:8000/v1" \
   --aux_model_name "GAIR/DeepResearcher-7b"

# Qwen/QwQ-32B, deepseek-ai/DeepSeek-R1-Distill-Qwen-32B, deepseek-ai/DeepSeek-R1-Distill-Llama-70B, Qwen/Qwen2.5-72B-Instruct, GAIR/DeepResearcher-7b, Qwen/Qwen2.5-7B-Instruct, Qwen/Qwen3-32B