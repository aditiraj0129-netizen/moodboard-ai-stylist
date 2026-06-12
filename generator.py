import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import os

def load_generator():
    """
    Downloads and loads Stable Diffusion.
    First time: downloads ~5GB (takes 10-20 mins depending on internet)
    After that: loads in about 30 seconds
    """
    print("Loading Stable Diffusion model...")
    print("First time will download ~5GB - please wait...")

    model_id = "runwayml/stable-diffusion-v1-5"

    # Check if Mac Apple Silicon (M1/M2/M3)
    if torch.backends.mps.is_available():
        device = "mps"
        print("Using Apple Silicon GPU (MPS) - good performance!")
    elif torch.cuda.is_available():
        device = "cuda"
        print("Using NVIDIA GPU - great performance!")
    else:
        device = "cpu"
        print("Using CPU - will be slow (5-10 mins per image) but works!")

    # Load the pipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32,  # float32 works on all devices
        safety_checker=None,        # disable for fashion (blocks clothing sometimes)
        requires_safety_checker=False
    )

    # Use a faster scheduler - cuts generation time in half
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config
    )

    # Move to the right device
    pipe = pipe.to(device)

    # Memory optimization - helps on Macs with limited RAM
    pipe.enable_attention_slicing()

    print(f"Stable Diffusion loaded on {device}!")
    return pipe, device


def generate_outfit_image(outfit_prompt, negative_prompt, pipe, device, seed=42):
    """
    Takes a text prompt and generates a fashion outfit image.

    outfit_prompt: detailed description of the outfit
    negative_prompt: what NOT to draw
    pipe: the loaded Stable Diffusion model
    seed: random seed - same seed = same image every time
    """

    print(f"Generating outfit image...")
    print(f"Prompt: {outfit_prompt[:80]}...")

    # Set seed for reproducibility
    # Same seed + same prompt = same image every time
    generator = torch.Generator(device=device if device != "mps" else "cpu")
    generator.manual_seed(seed)

    # Generate the image
    result = pipe(
        prompt=outfit_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=25,   # 25 steps = good quality, reasonable speed
        guidance_scale=7.5,       # how closely to follow the prompt (7-8 is ideal)
        width=512,                # image width in pixels
        height=768,               # image height - taller = better for full body
        generator=generator
    )

    image = result.images[0]
    return image


def save_image(image, filename, output_dir="outputs"):
    """Saves the generated image to the outputs folder"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    image.save(filepath)
    print(f"Image saved to: {filepath}")
    return filepath
