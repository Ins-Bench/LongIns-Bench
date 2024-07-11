import json
import yaml


# Read the YAML template
def read_yaml(config='none'):
    with open(f'config/{config}.yaml', 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

# Load the data
def load_data(split='test', mode='LIST',length=512):
    template = read_yaml(mode)
    with open(f'data/{mode}/{length}.json', 'r', encoding='utf-8') as file:
        context = json.load(file)
    prompts={}
    for task in context:
        if mode=="GIST":
            prompts.update({task:f'''{template["Instruction_0"]}
                                    {context[task]["task_prompt"]}
                                    {template["Instruction_1"]}
                                    {context[task]["Data"]}
                                    {template["Instruction_2"]}'''})
        else:
            prompts.update({task:f'''{template["Instruction_0"]}
                        {context[task]["Data"]}
                        {template["Instruction_1"]}'''})
    return prompts
        

