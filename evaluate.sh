#!/bin/bash


### Evaluation WebThinker
# # Evaluation strongreject | evaluate WebThinker in strongreject
#python scripts/evaluate/evaluate_strongreject.py \
#    --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.full.4.20,22:48.60" \
#    --output_dir "" # default: "" = markdown_dir






# # Evaluation deepreject | evaluate WebThinker in our deepreject
python scripts/evaluate/evaluate_deepreject.py \
      --markdown_dir "outputs/strongreject.dpsk-llama-70b.webthinker/markdown.question.5.5,22:39.65" \
      --output_dir "" \
      --dataset "data/strongreject/full.json"

python scripts/evaluate/evaluate_deepreject.py \
      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.question.5.6,0:27.07" \
      --output_dir "" \
      --dataset "data/strongreject/full.json"

python scripts/evaluate/evaluate_deepreject.py \
      --markdown_dir "outputs/strongreject.qwen2.5-7b.webthinker/markdown.question.5.5,23:1.47" \
      --output_dir "" \
      --dataset "data/strongreject/full.json"







# 5.4
### Evaluation refusal words
# for webthinker -> only give markdown_dir (must keep baseline_file empty "")
# for baseline -> should give baseline_file and metrics_file (can keep markdown_dir empty "")
# if want to evaluate in lower ASR model -> add "--lower"

## 1
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""
#
## 2
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.dpsk-llama-70b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.dpsk-llama-70b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""
#
## 3
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-72b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-72b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""
#
## 4
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-7b.webthinker/markdown.test.2025.05.04,00:44" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-7b.webthinker/markdown.test.2025.05.04,00:44" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""
#
## 5
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.test.2025.05.03,21:10" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.test.2025.05.03,21:10" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""
#
## 6
## for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower
#
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""


### Evaluation LLM Judge
# for webthinker -> only give markdown_dir (must keep baseline_file empty "")
# for baseline -> should give baseline_file and metrics_file (can keep markdown_dir empty "")

# 1
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.qwq.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""


# 2
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.dpsk-llama-70b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""


# 3
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-72b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""

# 4
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.qwen2.5-7b.webthinker/markdown.test.2025.05.04,00:44" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""


# 5
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.test.2025.05.03,21:10" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""


# 6
# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.test" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""








### Evaluation Baseline
# # deepreject | evaluate baseline our deepreject
#python scripts/evaluate/evaluate_deepreject_baseline.py \
#      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.full.4.30,9:2.27" \
#      --output_dir "outputs/baseline/qwen3-32b" \
#      --metrics_file "outputs/strongreject.qwen3-32b.webthinker/markdown.full.4.30,9:2.27/eval_metrics_all_ids_DeepReject_DeepReject_vllm.csv" \
#      --baseline_file "outputs/baseline/qwen3-32b/strongreject_baseline_04.29,01:12.json"  # only evaluate the items with file_exit=true or R=1



### Evaluation refusal words
# for webthinker -> only give markdown_dir (must keep baseline_file empty "")
# for baseline -> should give baseline_file and metrics_file (can keep markdown_dir empty "")
# if want to evaluate in lower ASR model -> add "--lower"


# for webthinker
#python scripts/evaluate/evaluate_refusal_words.py \
#      --markdown_dir "outputs/strongreject.qwen3-32b.webthinker/markdown.full.4.30,9:2.27" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file "" \
#      --lower






### Evaluation LLM Judge
# for webthinker -> only give markdown_dir (must keep baseline_file empty "")
# for baseline -> should give baseline_file and metrics_file (can keep markdown_dir empty "")

# for webthinker
#python scripts/evaluate/evaluate_llm_judge.py \
#      --markdown_dir "outputs/strongreject.deepresearcher-7b.webthinker/markdown.full.4.28,16:42.67" \
#      --output_dir "" \
#      --metrics_file "" \
#      --baseline_file ""

