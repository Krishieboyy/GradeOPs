from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
from app.config import MODEL_NAME

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageTextToText.from_pretrained(MODEL_NAME)
model = model.to(device)
model.eval()