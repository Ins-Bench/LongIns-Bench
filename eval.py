import re
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Run inference and save results.')
parser.add_argument('--model_name', type=str, default='Qwen2_7B_Instruct', help='Model name to use')

parser.add_argument('--mode', type=str, default='LIST', help='Modes to use for data loading, separated by space')
parser.add_argument('--length', type=int, default=8192, help='Data length to use')
args = parser.parse_args()

def read_or_create_json(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个新的空 JSON 文件
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}
    
    # 如果文件存在，读取并返回其内容
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def extract_numbers(s):
    numbers = re.findall(r'\d+', s)
    return list(map(int, numbers))
def calculate_f1_score(pred_list, true_list):
    # 转换为集合，便于计算交集和差集
    pred_set = set(pred_list)
    true_set = set(true_list)
    
    # 计算TP, FP, FN
    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    
    if tp + fp == 0 or tp + fn == 0:
        return 0.0
    
    # 计算Precision和Recall
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    # 计算F1值
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    
    return f1
def read_jsonl_files_to_dict(directory):
    json_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r', encoding='utf-8') as file:
                file_content={}
                for line in file:
                    file_content .update({json.loads(line)["id"]:json.loads(line)["response"]})
                file_key = os.path.splitext(filename)[0]  # 去除文件后缀
                json_dict[file_key] = file_content
    return json_dict


output_file_path=f"results/{args.model_name}_{args.length}_{args.mode}.jsonl"
with open(output_file_path, 'r', encoding='utf-8') as file:
    inference_result = [json.loads(line) for line in file]

answer_file=f"data/{args.mode}/{args.length}.json"
with open(answer_file, 'r', encoding='utf-8') as file:
    answer = json.load(file)

f1=read_or_create_json('f1.json')
for q in inference_result:
    response=q['response']
    matches = set(re.findall(r'\[(.*?)\]', response))
    result = []
    for match in matches:
        result+=extract_numbers(match)
    if f'{args.model_name}_{args.length}_{args.mode}' in f1.keys():
        f1[f'{args.model_name}_{args.length}_{args.mode}'].append(calculate_f1_score(result,answer[q['id']]['error']))
    else:
        f1[f'{args.model_name}_{args.length}_{args.mode}']=[calculate_f1_score(result,answer[q['id']]['error'])]

for model_length_mode in f1:
    if isinstance(f1[model_length_mode],list):
        f1[model_length_mode]=sum(f1[model_length_mode])/len(f1[model_length_mode])
with open(f'f1.json', 'w', encoding='utf-8') as f:
    json.dump(f1, f, ensure_ascii=False, indent=4)
