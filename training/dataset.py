import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from transformers import AutoTokenizer

"""
Dataset object for custom datasets 
"""
class ContentDataset(Dataset):
    def __init__(self, isTrain = True):
        data = pd.read_json("hf://datasets/mmathys/openai-moderation-api-evaluation/samples-1680.jsonl.gz", lines=True).fillna(0)
        data_OK = data.drop(columns=["prompt"]).astype(bool)
        OK = data_OK[["S", "H", "V", "HR","SH","S3","H2","V2"]].all(axis=1).astype(float)
        data["OK"] = OK
        shuffle = data.sample(frac=1, random_state=42).reset_index(drop=True)
        split = int(0.8 * shuffle.shape[0])
        if isTrain:
            self.df = shuffle.iloc[0:split]
        else:
            self.df = shuffle.iloc[split:]
        self.tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        item = self.df.iloc[idx]
        query = item.iloc[0]
        tokenized_query = self.tokenizer(query, padding="max_length", truncation=True, max_length=64, return_tensors="pt")
        one_hot = torch.tensor([item.iloc[iidx] for iidx in range(1, len(item))])
        return tokenized_query["input_ids"].squeeze(0), one_hot, query

def custom_collate(batch):
    ft = []
    lb = []
    q = []
    for idx, (feature, label, query) in enumerate(batch):
        ft.append(feature)
        lb.append(label)
        q.append(query)
    return torch.stack(ft), torch.stack(lb), q
    
def get_dataloader(batch = 16, isTrain = True):
    dataset = ContentDataset(isTrain = isTrain)
    loader = DataLoader(dataset, batch_size=batch, shuffle=True, drop_last=True, collate_fn=custom_collate)
    return loader

if __name__ == "__main__":
    loader = get_dataloader()
    for i, batch in enumerate(loader):
        feature, label, tokenizer_out = batch
        print(feature.shape)
        print(label.shape)
        print(tokenizer_out)
        exit()
