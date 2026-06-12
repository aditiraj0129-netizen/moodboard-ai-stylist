import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np

FASHION_STYLES = [
    "dark academia aesthetic outfit",
    "cottagecore aesthetic outfit",
    "Y2K fashion aesthetic",
    "minimalist clean aesthetic outfit",
    "streetwear urban fashion",
    "bohemian boho fashion",
    "coastal grandmother aesthetic",
    "romantic feminine fashion",
    "edgy grunge fashion",
    "preppy classic fashion",
    "vintage retro 70s fashion",
    "athleisure sporty fashion",
    "artsy eclectic fashion",
    "soft girl pastel aesthetic",
    "old money elegant fashion"
]

def load_clip_model():
    print("Loading CLIP model...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("CLIP model loaded!")
    return model, processor

def get_text_embedding(text_list, model, processor):
    # Process ONLY text — no images at all
    inputs = processor(
        text=text_list,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    with torch.no_grad():
        # text_model processes just the text side of CLIP
        text_outputs = model.text_model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )
        # pooler_output is the final summary vector for each text
        features = text_outputs.pooler_output
        # Project to CLIP's shared space
        features = model.text_projection(features)
    # Normalize so all vectors are same scale
    features = features / features.norm(dim=-1, keepdim=True)
    return features

def encode_text_mood(mood_text, model, processor):
    features = get_text_embedding([mood_text], model, processor)
    return features.numpy()

def encode_image_mood(image_path, model, processor):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        # vision_model processes just the image side of CLIP
        vision_outputs = model.vision_model(
            pixel_values=inputs["pixel_values"]
        )
        features = vision_outputs.pooler_output
        features = model.visual_projection(features)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.numpy()

def find_matching_styles(mood_embedding, model, processor, top_k=5):
    style_features = get_text_embedding(FASHION_STYLES, model, processor)
    mood_tensor = torch.tensor(mood_embedding)
    similarities = (mood_tensor @ style_features.T).squeeze()
    top_indices = similarities.argsort(descending=True)[:top_k]
    results = []
    for idx in top_indices:
        results.append({
            "style": FASHION_STYLES[idx],
            "score": round(float(similarities[idx]) * 100, 1)
        })
    return results
