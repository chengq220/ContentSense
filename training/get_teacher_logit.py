import pandas as pd
from models.KoalaAIDeberta import ModerationModel
from tqdm import tqdm
import numpy as np

model = ModerationModel()
data = pd.read_json("hf://datasets/mmathys/openai-moderation-api-evaluation/samples-1680.jsonl.gz", lines=True).fillna(0)
data_OK = data.drop(columns=["prompt"]).astype(bool)
OK = (data_OK[["S", "H", "V", "HR","SH","S3","H2","V2"]] == 0).all(axis=1).astype(float)
prompt = list(data["prompt"])
logit = []
for pt in tqdm(prompt):
    logit.append(model.pred_logit(pt).numpy().tolist())
df = pd.DataFrame({'logit':logit})
data["OK"] = OK
data["logit"] = df["logit"]
data.to_csv('dataset.csv', index=False) 