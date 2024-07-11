from data_loader import load_data
from models import load_model, infer
import json
import sys
import argparse
from tqdm import tqdm
import random
import os
import shutil

def check_completed(output_file):
    completed = {}
    no_response_id = []
    try:
        with open(output_file, 'r') as file:
            for line in file:
                data = json.loads(line)
                if 'response' in data and (isinstance(data['response'], str) or (isinstance(data['response'], dict) and 'error' not in data['response'])):
                    completed[data['id']] = data['response']
                else:
                    no_response_id.append(data['id'])
    except FileNotFoundError:
        pass  # 文件未找到时忽略
    except json.JSONDecodeError:
        pass  # JSON 解码错误时忽略
    return completed, no_response_id

def main(model_name='Qwen2_7B_Instruct',  modes=['GIST', 'LIST'], output_dir='results',length=512,infer_limit=None):
    tokenizer, model = load_model(model_name)
    os.makedirs(output_dir, exist_ok=True)
    for mode in modes:
        output_file_path = f'{output_dir}/{model_name}_{length}_{mode}.jsonl'
        temp_output_file_path = f'{output_file_path}.tmp'
        
        completed, _ = check_completed(output_file_path)
        temp_completed, _ = check_completed(temp_output_file_path)
        merged = {**temp_completed, **completed}
        infer_count = 0
        
        with open(temp_output_file_path, 'w') as temp_file:
            result={}
            all_prompts=load_data(mode=mode,length=length)
            
            for question in tqdm(all_prompts, desc=f'Processing {mode}'):
                #print(all_prompts[question])
                response = infer(model_name)(tokenizer, model, all_prompts[question])
                result['id'] = question
                result['response'] = response
                json.dump(result, temp_file)
                temp_file.write('\n')
                temp_file.flush()
                if infer_limit is not None and infer_count >= infer_limit:
                    break
        
        # Only rename the temp file to the final output file if the entire process completes successfully
        shutil.move(temp_output_file_path, output_file_path)
        _, no_response_id = check_completed(output_file_path)
        if len(no_response_id) > 0:
            print(f"Failed to get response for {len(no_response_id)} questions in {mode} mode. IDs: {no_response_id}", file=sys.stderr)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run inference and save results.')
    parser.add_argument('--model_name', type=str, default='Qwen2_7B_Instruct', help='Model name to use')
    
    parser.add_argument('--mode', nargs='+', default=['LIST', 'GIST'], help='Modes to use for data loading, separated by space')
    parser.add_argument('--output_dir', type=str, default='results', help='File to write results')
    parser.add_argument('--length', type=int, default=8192, help='Data length to use')
    parser.add_argument('--infer_limit', type=int, default=4096,help='Limit the number of inferences per run, default is no limit')
    args = parser.parse_args()

    main(model_name=args.model_name, modes=args.mode, output_dir=args.output_dir,length=args.length,infer_limit=args.infer_limit)
