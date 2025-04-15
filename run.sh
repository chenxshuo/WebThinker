#!/bin/bash


# # single question
# python scripts/run_web_thinker_report_brave_search.py \
#   --single_question "What are the models of OpenAI and what are the differences?" \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/QwQ-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/QwQ-32B"

# # strongreject + report -> implement in the new script run_web_thinker_strongreject.py
# python scripts/run_web_thinker_strongreject.py \
#     --dataset_path "data/strongreject/strongreject_small_dataset.csv" \
#     --subset_num 10 \
#     --api_base_url "http://localhost:8000/v1" \
#     --model_name "Qwen/QwQ-32B" \
#     --aux_api_base_url "http://localhost:8000/v1" \
#     --aux_model_name "Qwen/QwQ-32B" \

# # strongreject + report -> implement in run_web_thinker_report_brave_search.py
#python scripts/run_web_thinker_report_brave_search.py \
#    --dataset_name strongreject \
#    --split small \
#    --concurrent_limit 32 \
#    --api_base_url "http://localhost:8000/v1" \
#    --model_name "Qwen/QwQ-32B" \
#    --aux_api_base_url "http://localhost:8000/v1" \
#    --aux_model_name "Qwen/QwQ-32B"

# # evaluate
# python scripts/evaluate/evaluate.py \
#     --output_path "./outputs/gaia.qwq.webthinker/test.json" \
#     --task qa \
#     --use_llm \
#     --api_base_url "http://localhost:8000/v1" \
#     --model_name "Qwen/QwQ-32B" \
#     --extract_answer

# # qwq strongreject baseline
#python scripts/run_strongreject_baseline.py --api_base_url "http://localhost:8000/v1" --model_name "Qwen/QwQ-32B"

# # evaluate qwq strongreject baseline
python scripts/evaluate/evaluate_strongreject_baseline.py
