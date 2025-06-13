# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os 

exist = os.path.exists("root/.cache/huggingface/models--KoalaAI--Text-Moderation")
tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation", locallocal_files_only=exist)
model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation", local_files_only=exist)