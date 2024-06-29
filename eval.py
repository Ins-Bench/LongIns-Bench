import re
import os
import json

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
                file_content = [json.loads(line) for line in file]
                file_key = os.path.splitext(filename)[0]  # 去除文件后缀
                json_dict[file_key] = file_content
    return json_dict


output_files="result/Qwen2_7B_Instruct_16384_LIST.json"
answer_file="answer.json"
inference_result=read_jsonl_files_to_dict(output_files) 
with open(answer_file, 'r', encoding='utf-8') as file:
    answer = json.load(file)

f1={}
for length in inference_result:
    f1.update({length:[]})
    for qa in inference_result[length]:
        q,p=next(iter(qa.items()))
        
        matches = set(re.findall(r'\[(.*?)\]', p))
        result = []
        for match in matches:
            result.extend(map(int, re.findall(r'\d+', match)))
        f1[length].append(calculate_f1_score(result,answer[length][q]))
for length in f1:
    f1[length]=sum(f1[length])/len(f1[length])
with open('f1.json', 'w', encoding='utf-8') as f:
    json.dump(f1, f, ensure_ascii=False, indent=4)