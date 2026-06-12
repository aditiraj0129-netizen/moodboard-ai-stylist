from src.mood_encoder import load_clip_model, encode_text_mood, find_matching_styles
from src.style_translator import get_client, translate_mood_to_style, build_negative_prompt
from src.generator import load_generator, generate_outfit_image, save_image
import time
import os

class MoodToOutfitPipeline:
    """
    The complete pipeline in one class.
    
    Usage:
        pipeline = MoodToOutfitPipeline()
        pipeline.load()
        result = pipeline.generate("rainy Tokyo cafe cozy dark")
        # result has: image, prompt, colors, keywords, filepath
    """

    def __init__(self):
        self.clip_model = None
        self.clip_processor = None
        self.llm_client = None
        self.pipe = None
        self.device = None
        self.is_loaded = False

    def load(self):
        """Load all models once. Takes ~1 min after first download."""
        print("\n" + "="*50)
        print("  MoodBoard-to-Outfit Pipeline")
        print("="*50)

        print("\n[1/3] Loading CLIP mood encoder...")
        self.clip_model, self.clip_processor = load_clip_model()

        print("\n[2/3] Loading style translator...")
        self.llm_client = get_client()

        print("\n[3/3] Loading Stable Diffusion image generator...")
        self.pipe, self.device = load_generator()

        self.is_loaded = True
        print("\n✅ All models loaded! Ready to generate outfits.\n")

    def generate(self, mood_text, seed=None, save=True):
        """
        Full pipeline: mood text → outfit image

        mood_text: any mood or vibe as a string
        seed: set a number for reproducible results, None = random
        save: whether to save the image to outputs/

        returns: dict with all results
        """
        if not self.is_loaded:
            raise RuntimeError("Call pipeline.load() first!")

        if seed is None:
            import random
            seed = random.randint(0, 999999)

        start_time = time.time()

        print(f"\n🎨 Generating outfit for mood: '{mood_text}'")
        print("-" * 40)

        # Step 1: Encode mood with CLIP
        print("Step 1/3: Understanding your mood...")
        embedding = encode_text_mood(mood_text, self.clip_model, self.clip_processor)
        matched_styles = find_matching_styles(
            embedding, self.clip_model, self.clip_processor, top_k=3
        )
        top_style = matched_styles[0]["style"]
        print(f"  → Matched style: {top_style} ({matched_styles[0]['score']}%)")

        # Step 2: Translate to outfit prompt
        print("Step 2/3: Designing outfit...")
        style_result = translate_mood_to_style(mood_text, matched_styles, self.llm_client)
        outfit_prompt = style_result["outfit_prompt"]
        negative_prompt = build_negative_prompt()
        print(f"  → Outfit: {outfit_prompt[:60]}...")

        # Step 3: Generate image
        print("Step 3/3: Drawing outfit image (please wait)...")
        image = generate_outfit_image(
            outfit_prompt, negative_prompt, self.pipe, self.device, seed=seed
        )

        # Save image
        filepath = None
        if save:
            timestamp = int(time.time())
            safe_mood = mood_text[:30].replace(" ", "_").replace("/", "-")
            filename = f"{safe_mood}_{timestamp}.png"
            filepath = save_image(image, filename)

        elapsed = round(time.time() - start_time, 1)

        result = {
            "mood": mood_text,
            "matched_style": top_style,
            "outfit_prompt": outfit_prompt,
            "color_palette": style_result["color_palette"],
            "style_keywords": style_result["style_keywords"],
            "occasion": style_result["occasion"],
            "season": style_result["season"],
            "image": image,
            "filepath": filepath,
            "seed": seed,
            "time_taken": elapsed
        }

        print(f"\n✅ Done in {elapsed}s!")
        print(f"   Colors: {', '.join(result['color_palette'])}")
        print(f"   Keywords: {', '.join(result['style_keywords'])}")
        if filepath:
            print(f"   Saved to: {filepath}")

        return result
