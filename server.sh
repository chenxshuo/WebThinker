export HF_HOME=/dss/dssfs05/pn39qo/pn39qo-dss-0001/.cache/huggingface

# Inference
#nohup vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#nohup vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2

#nohup vllm serve Qwen/Qwen3-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#nohup vllm serve Qwen/Qwen3-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve Qwen/Qwen3-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2

nohup vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#nohup vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2

# Large
#nohup vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-70B --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-70B --dtype auto --api-key token-abc123 --tensor-parallel-size 4

#nohup vllm serve Qwen/Qwen2.5-72B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#vllm serve Qwen/Qwen2.5-72B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 4

# RL
#nohup vllm serve GAIR/DeepResearcher-7b --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#nohup vllm serve GAIR/DeepResearcher-7b --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve GAIR/DeepResearcher-7b --dtype auto --api-key token-abc123 --tensor-parallel-size 2

#nohup vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 4 > server.log 2>&1 &
#nohup vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 2 > server.log 2>&1 &
#vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 2



#vllm serve Qwen/QwQ-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2
#vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --dtype auto --api-key token-abc123 --tensor-parallel-size 2
#vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-70B --dtype auto --api-key token-abc123 --tensor-parallel-size 4
#vllm serve Qwen/Qwen2.5-72B-Instruct --dtype auto --api-key token-abc123 --tensor-parallel-size 4