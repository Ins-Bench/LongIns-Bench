from .Qwen2_7B_Instruct import load_model as Qwen2_7B_Instruct_load_model, infer as Qwen2_7B_Instruct_infer

models = {
    'Qwen2-7B-Instruct': { # model name
        'load': Qwen2_7B_Instruct_load_model,
        'infer': Qwen2_7B_Instruct_infer,
        'model-path': '<your-location-path>'
    },
}

def load_model(choice):
    if choice in models:
        return models[choice]['load'](models[choice]['model-path'])
    else:
        raise ValueError(f"Model choice '{choice}' is not supported.")

def infer(choice):
    if choice in models:
        return models[choice]['infer']
    else:
        raise ValueError(f"Inference choice '{choice}' is not supported.")

