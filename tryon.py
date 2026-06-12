import torch
import numpy as np
from PIL import Image
import os
import urllib.request

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Already downloaded: {dest_path}")
        return
    print(f"Downloading {os.path.basename(dest_path)}...")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    urllib.request.urlretrieve(url, dest_path)
    print("Downloaded!")

def load_tryon_pipeline():
    from diffusers import StableDiffusionPipeline, DDIMScheduler
    from ip_adapter.ip_adapter_faceid import IPAdapterFaceID

    print("Loading virtual try-on pipeline...")
    model_id = "runwayml/stable-diffusion-v1-5"

    if torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.float32
        print("Using Apple Silicon (MPS)")
    else:
        device = "cpu"
        dtype = torch.float32
        print("Using CPU")

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    ip_ckpt_path = "models/ip-adapter-faceid_sd15.bin"
    download_file(
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15.bin",
        ip_ckpt_path
    )

    ip_model = IPAdapterFaceID(pipe, ip_ckpt_path, device)
    print("Virtual try-on pipeline ready!")
    return ip_model, device


def extract_face_embedding(face_image_path):
    import insightface
    from insightface.app import FaceAnalysis

    print("Analysing face...")
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))

    image = Image.open(face_image_path).convert("RGB")
    img_array = np.array(image)
    faces = app.get(img_array)

    if len(faces) == 0:
        raise ValueError("No face detected! Use a clear front-facing photo.")

    print("Face detected!")
    return torch.from_numpy(faces[0].normed_embedding).unsqueeze(0)


def generate_tryon_image(face_image_path, outfit_prompt, ip_model, seed=42, scale=0.8):
    print("Generating your virtual try-on image...")
    face_embedding = extract_face_embedding(face_image_path)

    full_prompt = (
        f"portrait photo of a person, {outfit_prompt}, "
        f"looking at camera, natural studio lighting, photorealistic, sharp focus"
    )
    negative_prompt = (
        "low quality, blurry, distorted face, bad anatomy, deformed, "
        "ugly, cartoon, anime, watermark, multiple people"
    )

    generator = torch.Generator(device="cpu").manual_seed(seed)

    images = ip_model.generate(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        faceid_embeds=face_embedding,
        num_samples=1,
        width=512,
        height=768,
        num_inference_steps=25,
        guidance_scale=7.5,
        scale=scale,
        generator=generator,
    )

    print("Try-on image generated!")
    return images[0]
