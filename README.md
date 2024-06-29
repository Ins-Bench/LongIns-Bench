# LongIns-Bench
[**📖 arXiv**](https://arxiv.org/abs/2406.17588) | [**GitHub**](https://github.com/II-Bench/II-Bench)


This repo contains the evaluation code for the paper "[LongIns: A Challenging Long-context Instruction-based Exam for LLMs](https://arxiv.org/abs/2406.17588)"


## Introduction
The long-context capabilities of large language models (LLMs) have been a hot topic in recent years. To evaluate the performance of LLMs in different scenarios, various assessment benchmarks have emerged. However, as most of these benchmarks focus on identifying key information to answer questions, which mainly requires the retrieval ability of LLMs, these benchmarks can partially represent the reasoning performance of LLMs from large amounts of information. Meanwhile, although LLMs often claim to have context windows of 32k, 128k, 200k, or even longer, these benchmarks fail to reveal the actual supported length of these LLMs. To address these issues, we propose the LongIns benchmark dataset, a challenging long-context instruction-based exam for LLMs, which is built based on the existing instruction datasets. Specifically, in our LongIns, we introduce three evaluation settings: Global Instruction & Single Task (GIST), Local Instruction & Single Task (LIST), and Local Instruction & Multiple Tasks (LIMT). Based on LongIns, we perform comprehensive evaluations on existing LLMs and have the following important findings: (1). The top-performing GPT-4 with 128k context length performs poorly on the evaluation context window of 16k in our LongIns. (2). For the multi-hop reasoning ability of many existing LLMs, significant efforts are still needed under short context windows (less than 4k).

<p align="center">
  <img src="image.png" alt="introduction">
</p>

## 🏆 Mini-Leaderboard
| Open-source Models        | Score |
|---------------------------|-------|
| InstructBLIP-T5-XL        | 47.3  |
| BLIP-2 FLAN-T5-XL         | 52.8  |
| mPLUGw-OWL2               | 53.2  |
| Qwen-VL-Chat              | 53.4  |
| InstructBLIP-T5-XXL       | 56.7  |
| Mantis-8B-siglip-Llama3   | 57.5  |
| BLIP-2 FLAN-T5-XXL        | 57.8  |
| DeepSeek-VL-Chat-7B       | 60.3  |
| Yi-VL-6B-Chat             | 61.3  |
| InternLM-XComposer2-VL    | 62.1  |
| InternVL-Chat-1.5         | 66.3  |
| Idefics2-8B               | 67.7  |
| Yi-VL-34B-Chat            | 67.9  |
| MiniCPM-Llama3-2.5        | 69.4  |
| CogVLM2-Llama3-Chat       | 70.3  |
| LLaVA-1.6-34B             |**73.8**|
| **Closed-source Models**  |**Score**|
| GPT-4V                    | 65.9  |
| GPT-4o                    | 72.6  |
| Gemini-1.5 Pro            | 73.9  |
| Qwen-VL-MAX               | 74.8  |
| Claude 3.5 Sonnet         |**80.9**|



## Installation
```python
pip install -r requirements.txt
```

## Inference
You can directly perform inference on `Qwen2_7B_Instruct` model to be tested using the following command:
```python
python infer/infer.py --model_name Qwen2_7B_Instruct --mode LIST --output_dir ./results
```

`--mode`: We offer various evaluation models, including Global Instruction & Single Task (GIST), Local Instruction & Single Task (LIST), and Local Instruction & Multiple Tasks (LIMT).

`--infer_limit`: The input for this parameter is an integer, used to limit the number of problems for this inference. In the context of long text, some models may output without limit, and this parameter aims to save inference time.

During inference, a temporary file .jsonl.tmp will be saved. If the inference is unexpectedly interrupted, you can directly rerun the command to resume inference from the breakpoint.

### Run Custom Model
`--model_name` needs to align with the filenames in the `infer/models` directory. We have some built-in models available for direct selection. 

If you add a `custom model` to be tested, you need to refer to the files in the `infer/models` directory to add a new `.py` file and add your config in [\_\_init\_\_.py](infer/models/__init__.py).


## Evaluation

After you finish inference and confirm there are no error messages, please run the answer parsing and evaluation pipeline as follows: 
```
python eval.py --model_name yi-vl-6b-chat --mode none --output_dir ./results --save_dir ./results_with_status
```
Detailed evaluation results can be found in the `save_dir`.

Alternatively, you can use the following command to evaluate the inference results of all models:
```
python eval.py --evaluate_all --output_dir ./results --save_dir ./results_with_status
```


## Citation

**BibTeX:**
```bibtex
@misc{gavin2024longinschallenginglongcontextinstructionbased,
      title={LongIns: A Challenging Long-context Instruction-based Exam for LLMs}, 
      author={Shawn Gavin and Tuney Zheng and Jiaheng Liu and Quehry Que and Noah Wang and Jian Yang and Chenchen Zhang and Wenhao Huang and Wenhu Chen and Ge Zhang},
      year={2024},
      eprint={2406.17588},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2406.17588}, 
}
```
