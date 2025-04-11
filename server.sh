export HF_HOME=/dss/dssfs05/pn39qo/pn39qo-dss-0001/.cache/huggingface

nohup vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2


#vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2
#vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-70B --dtype auto --api-key token-abc123 --tensor-parallel-size 4

#vllm serve Qwen/Qwen2.5-72B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 4