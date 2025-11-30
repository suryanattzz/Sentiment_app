from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import uvicorn

app = FastAPI()

model_name = "SamLowe/roberta-base-go_emotions"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict(data: InputText):
    inputs = tokenizer(data.text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits)[0]

    labels = model.config.id2label
    threshold = 0.3  

    emotions = {
        labels[i]: float(probs[i])
        for i in range(len(probs))
        if probs[i] > threshold
    }

    return {"emotions": emotions}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
