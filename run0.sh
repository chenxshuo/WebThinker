#!/bin/bash

# # WebThinker + any dataset -> implement in run_web_thinker_report_brave_search.py
#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question1\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"
##   --max_tokens 30000
#
#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question2\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"
#
#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question3\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"
#
#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question4\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"
#
#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question5\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"

#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question6\
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"

#python scripts/question_run_web_thinker_report_brave_search.py \
#   --dataset_name strongreject \
#   --split question_patch1 \
#   --concurrent_limit 32 \
#   --api_base_url "http://localhost:8000/v1" \
#   --model_name "Qwen/Qwen3-32B" \
#   --aux_api_base_url "http://localhost:8000/v1" \
#   --aux_model_name "Qwen/Qwen3-32B"

# Qwen/QwQ-32B, deepseek-ai/DeepSeek-R1-Distill-Qwen-32B, deepseek-ai/DeepSeek-R1-Distill-Llama-70B, Qwen/Qwen2.5-72B-Instruct, GAIR/DeepResearcher-7b, Qwen/Qwen2.5-7B-Instruct, Qwen/Qwen3-32B


# 5.7 Evaluation: LLM Judge
python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.question" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""

python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.question" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""

python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.dpsk-llama-70b.webthinker/markdown.question.5.5,22:39.65" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""

python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.qwen2.5-72b.webthinker/markdown.question.5.6,2:13.51" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""

python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.qwen2.5-7b.webthinker/markdown.question.5.5,23:1.47" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""

python scripts/evaluate/evaluate_llm_judge.py \
      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.question.5.6,0:27.07" \
      --output_dir "" \
      --metrics_file "" \
      --baseline_file ""