from transformers import AutoModelForCausalLM
import os
from dotenv import load_dotenv

load_dotenv()

base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct", token=os.getenv('HF_TOKEN'))
base_model.save_pretrained("/ContentSense/app/model/")