#!/bin/bash


# # single question
#python scripts/run_web_thinker_report_brave_search.py \
#    --single_question "What are the models of OpenAI and what are the differences?" \
#    --api_base_url "http://localhost:8000/v1" \
#    --model_name "Qwen/QwQ-32B" \
#    --aux_api_base_url "http://localhost:8000/v1" \
#    --aux_model_name "Qwen/QwQ-32B"

# # WebThinker + any dataset -> implement in run_web_thinker_report_brave_search.py
#python scripts/run_web_thinker_report_brave_search.py \
#    --dataset_name strongreject \
#    --split full \
#    --concurrent_limit 32 \
#    --api_base_url "http://localhost:8000/v1" \
#    --model_name "Qwen/QwQ-32B" \
#    --aux_api_base_url "http://localhost:8000/v1" \
#    --aux_model_name "Qwen/QwQ-32B"

# # modified script "test_run_web_thinker_report_brave_search.py"
#python scripts/test_run_web_thinker_report_brave_search.py \
#    --dataset_name strongreject \
#    --split full \
#    --concurrent_limit 32 \
#    --api_base_url "http://localhost:8000/v1" \
#    --model_name "Qwen/QwQ-32B" \
#    --aux_api_base_url "http://localhost:8000/v1" \
#    --aux_model_name "Qwen/QwQ-32B"


### Evaluation
# # evaluate WebThinker in strongreject
#python scripts/evaluate/evaluate_strongreject.py \
#    --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.full.4.20,22:48.60" \
#    --output_dir "" # default: "" = markdown_dir

# # evaluate WebThinker in our deepreject
#python scripts/evaluate/evaluate_deepreject.py \
#      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.full.4.20,22:48.60" \
#      --output_dir "" \
#      --dataset "data/strongreject/full.json"

# # evaluate WebThinker exclude - strongreject
# python scripts/evaluate/evaluate.py \
#     --output_path "./outputs/gaia.qwq.webthinker/test.json" \
#     --task qa \
#     --use_llm \
#     --api_base_url "http://localhost:8000/v1" \
#     --model_name "Qwen/QwQ-32B" \
#     --extract_answer

# # qwq baseline strongreject
#python scripts/run_strongreject_baseline.py --api_base_url "http://localhost:8000/v1" --model_name "Qwen/QwQ-32B"

# # evaluate qwq baseline strongreject
#python scripts/evaluate/evaluate_strongreject_baseline.py

# # evaluate qwq baseline our deepreject
python scripts/evaluate/evaluate_deepreject_baseline.py \
      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.full.4.20,22:48.60" \
      --output_dir "outputs/baseline" \
      --metrics_file "outputs/strongreject.qwq.webthinker/markdown.full.4.20,22:48.60/eval_metrics_all_ids_DeepReject_DeepReject_vllm.csv" # only evaluate the items with file_exit=true or R=1