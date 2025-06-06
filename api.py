from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

MODEL_PATH = "ACE-Step/ACE-Step-v1-3.5B"

model = None
tokenizer = None

@app.on_event("startup")
async def load_model():
    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

@app.post("/generate")
async def generate_music(prompt: str, duration: int = 30):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_length=duration * 256,
        do_sample=True,
        temperature=0.7
    )
    audio = tokenizer.decode(outputs[0])
    return {"audio": audio}

@app.get("/health")
async def health_check():
    return {"status": "OK"}
