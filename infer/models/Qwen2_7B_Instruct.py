import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig,AutoModel
from zhipuai import ZhipuAI 
from tqdm import tqdm
import openai
import time
def load_model(model_path="Qwen/Qwen2-7B-Instruct"):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True).eval()
    return tokenizer, model

def infer(tokenizer, model, instruction):
    outputs=[]
    messages = [{"role": "user", "content": instruction}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to('cuda')
    output_ids = model.generate(model_inputs['input_ids'], max_new_tokens=10000)
    generated_ids = [
        output_ids[0][model_inputs['input_ids'].shape[1]:]
    ]
    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return     response



