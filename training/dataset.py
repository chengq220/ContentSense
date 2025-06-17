import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from transformers import AutoTokenizer
import ast

"""
Dataset object for custom datasets 
"""
class ContentDataset(Dataset):
    def __init__(self, isTrain = True):
        data = pd.read_csv("training/dataset.csv")
        shuffle = data.sample(frac=1, random_state=42).reset_index(drop=True)
        full_logit = shuffle["logit"]
        shuffle = shuffle.drop(columns = ["logit"])
        split = int(0.8 * shuffle.shape[0])
        if isTrain:
            self.df = shuffle.iloc[0:split]
            self.logit = full_logit.iloc[0:split]
        else:
            self.df = shuffle.iloc[split:]
            self.logit = full_logit.iloc[split:]
        self.tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")
        

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        item = self.df.iloc[idx]
        query = item.iloc[0]
        tokenized_query = self.tokenizer(query, padding="max_length", truncation=True, return_tensors="pt")
        one_hot = torch.tensor([item.iloc[iidx] for iidx in range(1, len(item))])
        cur_logit = torch.tensor(ast.literal_eval(self.logit.iloc[idx])[0], dtype=float)
        return tokenized_query["input_ids"].squeeze(0), one_hot, cur_logit, query
    
    @property
    def tokenizer_vocab_size(self):
        return self.tokenizer.vocab_size


def custom_collate(batch):
    ft = []
    lb = []
    logits = []
    q = []
    for idx, (feature, label, logit, query) in enumerate(batch):
        ft.append(feature)
        lb.append(label)
        logits.append(logit)
        q.append(query)
    return torch.stack(ft), torch.stack(lb), torch.stack(logits), q
    
def get_dataloader(batch = 16, isTrain = True):
    dataset = ContentDataset(isTrain = isTrain)
    loader = DataLoader(dataset, batch_size=batch, shuffle=True, drop_last=True, collate_fn=custom_collate)
    return loader, dataset.tokenizer_vocab_size

if __name__ == "__main__":
    loader, vocab = get_dataloader(isTrain=False)
    for i, batch in enumerate(loader):
        feature, label, logits = batch
        print(feature.shape)
        print(label.shape)
        print(logits.shape)

