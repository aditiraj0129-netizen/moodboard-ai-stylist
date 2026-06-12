import gradio as gr
import sys, os, torch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import MoodToOutfitPipeline
from src.styling_advisor import STYLE_TEMPLATES

print("Loading models...")
pipeline = MoodToOutfitPipeline()
pipeline.load()
print("Ready!")

last_result = {}

TRYON_AVAILABLE = False
try:
    from src.tryon import load_tryon_pipeline, generate_tryon_image
    ip_model, device = load_tryon_pipeline()
    TRYON_AVAILABLE = True
    print("Try-on ready!")
except:
    print("Try-on not available — outfit mode only")

def match_style(mood):
    mood = mood.lower()
    if any(w in mood for w in ["dark", "academia", "library", "book", "candle", "study", "vintage scholar"]):
        return "dark academia"
    elif any(w in mood for w in ["cottage", "garden", "flower", "meadow", "wildflower", "nature"]):
        return "cottagecore"
    elif any(w in mood for w in ["y2k", "2000", "millennium", "retro pop", "2000s"]):
        return "Y2K"
    elif any(w in mood for w in ["minimal", "clean", "simple", "capsule", "neutral", "quiet"]):
        return "minimalist"
    elif any(w in mood for w in ["street", "urban", "hype", "rap", "city", "tokyo", "grunge", "edgy", "dark"]):
        return "streetwear"
    elif any(w in mood for w in ["romantic", "feminine", "soft girl", "pink", "love", "dreamy", "spring", "pastel", "soft", "beach", "summer", "happy", "bright"]):
        return "romantic"
    elif any(w in mood for w in ["boho", "bohemian", "festival", "free", "earthy", "desert"]):
        return "boho"
    elif any(w in mood for w in ["old money", "elegant", "luxury", "classic", "rich", "posh", "refined", "paris", "cafe"]):
        return "old money"
    else:
        return "minimalist"

def generate_outfit(mood_text, seed):
    global last_result
    if not mood_text.strip():
        return None, "<p style='color:#888;text-align:center;padding:40px'>Enter a mood above to get started ✨</p>", gr.update(visible=False), gr.update(visible=False)
    try:
        seed = int(seed) if seed else 42
        result = pipeline.generate(mood_text, seed=seed, save=True)
        last_result = result
        style_key = match_style(mood_text)
        s = STYLE_TEMPLATES.get(style_key, STYLE_TEMPLATES["minimalist"])
        style_name = style_key.title()
        makeup_color = "#e879a0" if s["makeup"] == "dark" else "#9b8aff"
        makeup_label = "Dark Glam" if s["makeup"] == "dark" else "Light Natural"

        color_swatches = "".join([
            f"""<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>
                <div style='width:18px;height:18px;border-radius:50%;background:{c};
                    flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.3)'></div>
                <span style='font-size:13px;color:#555;text-transform:capitalize'>{c}</span>
            </div>""" for c in s["colors"]
        ])

        kw_tags = "".join([
            f"<span style='display:inline-block;background:#f5f0ff;color:#7c5cbf;"
            f"border:1px solid #e0d5f5;padding:4px 12px;border-radius:20px;"
            f"font-size:12px;margin:3px;font-weight:500'>{k}</span>"
            for k in s["keywords"]
        ])

        accessories = "".join([
            f"""<div style='display:flex;align-items:flex-start;gap:10px;
                padding:10px 0;border-bottom:1px solid #f0f0f0'>
                <div style='width:6px;height:6px;border-radius:50%;background:#c9b4e8;
                    margin-top:5px;flex-shrink:0'></div>
                <span style='font-size:13px;color:#444;line-height:1.4'>{a}</span>
            </div>""" for a in s["accessories"]
        ])

        shoe_list = "".join([
            f"""<div style='display:flex;align-items:center;gap:10px;padding:8px 0;
                border-bottom:1px solid #f0f0f0'>
                <span style='color:#e879a0;font-size:14px'>→</span>
                <span style='font-size:13px;color:#444'>{sh}</span>
            </div>""" for sh in s["shoes"]
        ])

        hair_list = "".join([
            f"""<div style='display:flex;align-items:flex-start;gap:10px;padding:8px 0;
                border-bottom:1px solid #f0f0f0'>
                <span style='color:#9b8aff;font-size:14px'>✦</span>
                <span style='font-size:13px;color:#444;line-height:1.4'>{h}</span>
            </div>""" for h in s["hairstyle"]
        ])

        makeup_steps = "".join([
            f"""<div style='display:flex;justify-content:space-between;
                align-items:flex-start;padding:7px 0;border-bottom:1px solid #f5f5f5'>
                <span style='font-size:12px;color:#888;font-weight:500;
                    text-transform:uppercase;letter-spacing:0.5px;
                    min-width:60px'>{step}</span>
                <span style='font-size:13px;color:#444;text-align:right;
                    max-width:220px;line-height:1.4'>{desc}</span>
            </div>""" for step, desc in s["makeup_details"].items()
        ])

        card = f"""
<div style='font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    max-width:100%;padding:4px'>

    <!-- Hero banner -->
    <div style='background:linear-gradient(135deg,#2d1b54 0%,#1a1035 100%);
        border-radius:16px;padding:24px 28px;margin-bottom:20px;
        position:relative;overflow:hidden'>
        <div style='position:absolute;top:-20px;right:-20px;width:120px;height:120px;
            border-radius:50%;background:rgba(155,138,255,0.1)'></div>
        <div style='position:absolute;bottom:-30px;left:30px;width:80px;height:80px;
            border-radius:50%;background:rgba(232,121,160,0.08)'></div>
        <p style='color:rgba(255,255,255,0.5);font-size:11px;letter-spacing:2px;
            text-transform:uppercase;margin:0 0 6px'>Your style match</p>
        <h2 style='color:white;font-size:1.6rem;font-weight:700;margin:0 0 8px;
            letter-spacing:-0.5px'>{style_name}</h2>
        <p style='color:rgba(255,255,255,0.55);font-size:13px;margin:0 0 14px'>
            Based on your mood: <em>"{mood_text}"</em>
        </p>
        <div>{kw_tags}</div>
    </div>

    <!-- Color palette -->
    <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
        padding:20px 24px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:14px'>
            <div style='width:3px;height:18px;background:linear-gradient(#9b8aff,#e879a0);
                border-radius:2px'></div>
            <h3 style='font-size:13px;font-weight:600;color:#1a1a2e;margin:0;
                text-transform:uppercase;letter-spacing:1px'>Color Palette</h3>
        </div>
        {color_swatches}
    </div>

    <!-- Accessories -->
    <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
        padding:20px 24px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <div style='width:3px;height:18px;background:linear-gradient(#667eea,#764ba2);
                border-radius:2px'></div>
            <h3 style='font-size:13px;font-weight:600;color:#1a1a2e;margin:0;
                text-transform:uppercase;letter-spacing:1px'>💎 Accessories to Pair</h3>
        </div>
        <p style='color:#aaa;font-size:12px;margin:0 0 8px'>Complete the look with these pieces</p>
        {accessories}
    </div>

    <!-- Shoes row -->
    <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
        padding:20px 24px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <div style='width:3px;height:18px;background:linear-gradient(#e879a0,#f43f5e);
                border-radius:2px'></div>
            <h3 style='font-size:13px;font-weight:600;color:#1a1a2e;margin:0;
                text-transform:uppercase;letter-spacing:1px'>👠 Shoes & Heels</h3>
        </div>
        <p style='color:#aaa;font-size:12px;margin:0 0 8px'>Pick any of these to complete your outfit</p>
        {shoe_list}
        <div style='margin-top:10px;padding:10px 14px;background:#fff8fb;
            border-left:3px solid #e879a0;border-radius:0 8px 8px 0'>
            <span style='color:#e879a0;font-size:11px;font-weight:600'>HEELS TIP &nbsp;</span>
            <span style='color:#666;font-size:12px'>{s["heels"]}</span>
        </div>
    </div>

    <!-- Hair -->
    <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
        padding:20px 24px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <div style='width:3px;height:18px;background:linear-gradient(#a78bfa,#9b8aff);
                border-radius:2px'></div>
            <h3 style='font-size:13px;font-weight:600;color:#1a1a2e;margin:0;
                text-transform:uppercase;letter-spacing:1px'>💇 Recommended Hairstyles</h3>
        </div>
        <p style='color:#aaa;font-size:12px;margin:0 0 8px'>Any of these will elevate your look</p>
        {hair_list}
    </div>

    <!-- Makeup -->
    <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
        padding:20px 24px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
        <div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:4px;flex-wrap:wrap;gap:8px'>
            <div style='display:flex;align-items:center;gap:8px'>
                <div style='width:3px;height:18px;background:linear-gradient({makeup_color},{makeup_color}88);
                    border-radius:2px'></div>
                <h3 style='font-size:13px;font-weight:600;color:#1a1a2e;margin:0;
                    text-transform:uppercase;letter-spacing:1px'>💄 Makeup Look</h3>
            </div>
            <span style='background:{makeup_color}18;color:{makeup_color};
                border:1px solid {makeup_color}44;padding:3px 12px;
                border-radius:20px;font-size:11px;font-weight:600'>{makeup_label}</span>
        </div>
        <p style='color:#aaa;font-size:12px;margin:0 0 10px'>Step-by-step guide for this aesthetic</p>
        {makeup_steps}
    </div>

    <!-- Bottom 3 cards -->
    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px'>
        <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
            padding:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
            <p style='color:#f59e0b;font-size:10px;font-weight:600;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 8px'>💅 Nails</p>
            <p style='color:#444;font-size:12px;margin:0;line-height:1.5'>{s["nails"]}</p>
        </div>
        <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
            padding:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
            <p style='color:#10b981;font-size:10px;font-weight:600;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 8px'>🌸 Fragrance</p>
            <p style='color:#444;font-size:12px;margin:0;line-height:1.5'>{s["fragrance"]}</p>
        </div>
        <div style='background:white;border:1px solid #f0edf8;border-radius:14px;
            padding:16px;box-shadow:0 2px 12px rgba(0,0,0,0.04)'>
            <p style='color:#3b82f6;font-size:10px;font-weight:600;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 8px'>💡 Stylist Tip</p>
            <p style='color:#444;font-size:12px;margin:0;line-height:1.5'>{s["tip"]}</p>
        </div>
    </div>

    <!-- Try-on CTA -->
    <div style='background:linear-gradient(135deg,#1a1035,#2d1b54);
        border-radius:14px;padding:22px 24px;text-align:center'>
        <p style='color:rgba(255,255,255,0.9);font-size:16px;font-weight:600;
            margin:0 0 6px'>Want to see how this looks on YOU?</p>
        <p style='color:rgba(255,255,255,0.45);font-size:13px;margin:0 0 16px'>
            Upload your photo below and our AI will place you in this outfit
        </p>
        <div style='display:inline-flex;align-items:center;gap:8px;
            background:rgba(155,138,255,0.15);border:1px solid rgba(155,138,255,0.3);
            border-radius:30px;padding:8px 20px'>
            <span style='color:#c4b5fd;font-size:13px'>↓ Scroll down to try it on</span>
        </div>
    </div>
</div>"""

        return result["image"], card, gr.update(visible=True), gr.update(visible=True)

    except Exception as e:
        return None, f"<p style='color:red;padding:20px'>Error: {str(e)}</p>", gr.update(visible=False), gr.update(visible=False)


def generate_tryon(face_image, seed):
    global last_result
    if face_image is None:
        return None, "Please upload your face photo first."
    if not last_result:
        return None, "Please generate an outfit first."
    if not TRYON_AVAILABLE:
        return None, "Try-on not available. Run: pip install ip-adapter insightface onnxruntime"
    try:
        seed = int(seed) if seed else 42
        os.makedirs("outputs", exist_ok=True)
        face_path = face_image if isinstance(face_image, str) else "outputs/temp_face.jpg"
        if not isinstance(face_image, str):
            from PIL import Image as PILImage
            PILImage.fromarray(face_image).save(face_path)
        image = generate_tryon_image(
            face_image_path=face_path,
            outfit_prompt=last_result.get("outfit_prompt", ""),
            ip_model=ip_model, seed=seed, scale=0.8
        )
        image.save(f"outputs/tryon_{seed}.png")
        return image, "Here's how you'd look in this outfit!"
    except Exception as e:
        return None, f"Error: {str(e)}"


EXAMPLES = [
    ["rainy Tokyo cafe cozy dark", 42],
    ["bright summer beach happy", 123],
    ["old library books candlelight", 7],
    ["neon city night electric", 99],
    ["soft spring garden pastel", 55],
    ["vintage paris cafe romantic", 200],
    ["dark edgy grunge rock", 77],
    ["old money luxury elegant", 33],
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { box-sizing:border-box; margin:0; padding:0; }
body, .gradio-container {
    background:#fafaf9 !important;
    font-family:'Inter',-apple-system,sans-serif !important;
    color:#1a1a2e !important;
}
.gradio-container { max-width:1160px !important; margin:0 auto !important; padding:0 20px !important; }
textarea, input[type=number] {
    background:white !important;
    border:1.5px solid #e8e4f0 !important;
    color:#1a1a2e !important;
    border-radius:12px !important;
    font-size:14px !important;
    font-family:'Inter',sans-serif !important;
    transition:all 0.2s !important;
    padding:12px 16px !important;
    box-shadow:0 2px 8px rgba(0,0,0,0.04) !important;
}
textarea:focus, input:focus {
    border-color:#9b8aff !important;
    box-shadow:0 0 0 3px rgba(155,138,255,0.12) !important;
    outline:none !important;
}
label > span:first-child {
    color:#888 !important;
    font-size:11px !important;
    font-weight:600 !important;
    text-transform:uppercase !important;
    letter-spacing:1.5px !important;
}
button.primary {
    background:linear-gradient(135deg,#7c5cbf 0%,#9b8aff 100%) !important;
    border:none !important;
    border-radius:12px !important;
    color:white !important;
    font-size:14px !important;
    font-weight:600 !important;
    padding:13px 24px !important;
    cursor:pointer !important;
    transition:all 0.25s !important;
    letter-spacing:0.2px !important;
    box-shadow:0 4px 14px rgba(124,92,191,0.3) !important;
    width:100% !important;
}
button.primary:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 8px 22px rgba(124,92,191,0.4) !important;
}
button.secondary {
    background:linear-gradient(135deg,#c9507a 0%,#e879a0 100%) !important;
    border:none !important;
    border-radius:12px !important;
    color:white !important;
    font-size:14px !important;
    font-weight:600 !important;
    padding:13px 24px !important;
    cursor:pointer !important;
    transition:all 0.25s !important;
    box-shadow:0 4px 14px rgba(201,80,122,0.3) !important;
    width:100% !important;
}
button.secondary:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 8px 22px rgba(201,80,122,0.4) !important;
}
.block, .panel, .form {
    background:white !important;
    border:1.5px solid #f0edf8 !important;
    border-radius:16px !important;
    box-shadow:0 2px 16px rgba(0,0,0,0.04) !important;
}
.examples-holder .label-wrap { display:none !important; }
.examples-holder table td button {
    background:white !important;
    border:1.5px solid #ede8f5 !important;
    color:#7c5cbf !important;
    border-radius:8px !important;
    font-size:12px !important;
    font-weight:500 !important;
    transition:all 0.2s !important;
    padding:5px 10px !important;
}
.examples-holder table td button:hover {
    background:#f5f0ff !important;
    border-color:#9b8aff !important;
}
footer { display:none !important; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#fafaf9; }
::-webkit-scrollbar-thumb { background:#ddd8ef; border-radius:3px; }
"""

with gr.Blocks(css=CSS) as demo:

    # ── NAV ──
    gr.HTML("""
    <div style='display:flex;align-items:center;justify-content:space-between;
        padding:20px 4px 28px;border-bottom:1px solid #f0edf8;margin-bottom:28px'>
        <div style='display:flex;align-items:center;gap:10px'>
            <div style='width:34px;height:34px;border-radius:10px;
                background:linear-gradient(135deg,#7c5cbf,#e879a0);
                display:flex;align-items:center;justify-content:center;
                font-size:16px'>🎨</div>
            <div>
                <div style='font-size:15px;font-weight:700;color:#1a1a2e;
                    letter-spacing:-0.3px'>MoodBoard</div>
                <div style='font-size:11px;color:#aaa;letter-spacing:0.3px'>AI Fashion Stylist</div>
            </div>
        </div>
        <div style='display:flex;gap:6px'>
            <span style='background:#f5f0ff;color:#7c5cbf;padding:5px 14px;
                border-radius:20px;font-size:12px;font-weight:500;
                border:1px solid #e0d5f5'>AI Powered</span>
            <span style='background:#fff8fb;color:#e879a0;padding:5px 14px;
                border-radius:20px;font-size:12px;font-weight:500;
                border:1px solid #f5d5e5'>Virtual Try-On</span>
        </div>
    </div>
    """)

    # ── HERO ──
    gr.HTML("""
    <div style='text-align:center;padding:10px 20px 36px'>
        <div style='display:inline-block;background:#f5f0ff;color:#7c5cbf;
            padding:5px 16px;border-radius:20px;font-size:12px;font-weight:600;
            letter-spacing:0.5px;margin-bottom:16px;border:1px solid #e0d5f5'>
            ✦ Your Personal AI Stylist
        </div>
        <h1 style='font-size:2.4rem;font-weight:800;color:#1a1a2e;
            letter-spacing:-1.5px;line-height:1.15;margin-bottom:12px'>
            Tell me your mood.<br>
            <span style='background:linear-gradient(135deg,#7c5cbf,#e879a0);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
                I'll dress you perfectly.
            </span>
        </h1>
        <p style='color:#888;font-size:15px;max-width:480px;
            margin:0 auto;line-height:1.6;font-weight:400'>
            Describe how you feel, where you're going, or what vibe you want.
            Get a complete outfit with styling advice — then see it on you.
        </p>
    </div>
    """)

    # ── STEP 1: MOOD INPUT ──
    with gr.Row():
        with gr.Column(scale=5):
            gr.HTML("""
            <div style='margin-bottom:8px'>
                <span style='background:#1a1a2e;color:white;width:22px;height:22px;
                    border-radius:50%;display:inline-flex;align-items:center;
                    justify-content:center;font-size:11px;font-weight:700;
                    margin-right:8px'>1</span>
                <span style='font-size:14px;font-weight:600;color:#1a1a2e'>
                    Describe your mood or vibe
                </span>
            </div>
            """)
            mood_input = gr.Textbox(
                label="",
                placeholder="e.g.  \"rainy Sunday morning, cozy and introspective\"  or  \"girls night out, confident and bold\"  or  \"soft spring picnic\"",
                lines=3
            )
            with gr.Row():
                seed_input = gr.Number(label="Variation seed", value=42, precision=0, scale=1)
            generate_btn = gr.Button("✦  Generate My Outfit", variant="primary", size="lg")

            gr.HTML("<div style='margin:12px 0 6px;font-size:11px;color:#bbb;text-align:center;letter-spacing:1px;text-transform:uppercase'>— or try one of these —</div>")
            gr.Examples(examples=EXAMPLES, inputs=[mood_input, seed_input], label="")

        with gr.Column(scale=5):
            outfit_image = gr.Image(
                label="Your Outfit",
                height=480,
                show_label=False
            )
            gr.HTML("""
            <div style='text-align:center;padding:10px 0 0'>
                <p style='color:#ccc;font-size:12px'>
                    Your AI-generated outfit will appear here
                </p>
            </div>
            """)

    # ── STYLE CARD ──
    style_card = gr.HTML("""
    <div style='background:white;border:1.5px solid #f0edf8;border-radius:16px;
        padding:40px;text-align:center;margin-top:8px;
        box-shadow:0 2px 16px rgba(0,0,0,0.04)'>
        <div style='font-size:2rem;margin-bottom:12px'>✨</div>
        <p style='color:#ccc;font-size:14px'>
            Your complete style guide will appear here after generation
        </p>
        <p style='color:#ddd;font-size:12px;margin-top:6px'>
            Includes: accessories · shoes · hairstyle · makeup · nails · fragrance
        </p>
    </div>""")

    # ── DIVIDER ──
    tryon_section = gr.Column(visible=False)
    with tryon_section:
        gr.HTML("""
        <div style='margin:32px 0 24px;display:flex;align-items:center;gap:16px'>
            <div style='flex:1;height:1px;background:linear-gradient(to right,transparent,#e0d5f5)'></div>
            <div style='background:linear-gradient(135deg,#7c5cbf,#e879a0);color:white;
                padding:8px 22px;border-radius:30px;font-size:13px;font-weight:600;
                white-space:nowrap;box-shadow:0 4px 14px rgba(124,92,191,0.3)'>
                ✦ Virtual Try-On
            </div>
            <div style='flex:1;height:1px;background:linear-gradient(to left,transparent,#e0d5f5)'></div>
        </div>
        """)

        # ── STEP 2: TRY-ON ──
        with gr.Row():
            with gr.Column(scale=5):
                gr.HTML("""
                <div style='margin-bottom:8px'>
                    <span style='background:#1a1a2e;color:white;width:22px;height:22px;
                        border-radius:50%;display:inline-flex;align-items:center;
                        justify-content:center;font-size:11px;font-weight:700;
                        margin-right:8px'>2</span>
                    <span style='font-size:14px;font-weight:600;color:#1a1a2e'>
                        Upload your photo to try it on
                    </span>
                </div>
                """)
                face_input = gr.Image(
                    label="",
                    type="filepath",
                    height=280,
                    show_label=False
                )
                tryon_seed = gr.Number(label="Variation seed", value=42, precision=0)
                tryon_btn = gr.Button("👗  See This Outfit On Me", variant="secondary", size="lg")
                gr.HTML("""
                <div style='background:#fafaf9;border:1px solid #f0edf8;border-radius:12px;
                    padding:16px;margin-top:12px'>
                    <p style='font-size:12px;font-weight:600;color:#888;margin-bottom:10px;
                        text-transform:uppercase;letter-spacing:1px'>
                        📸 For best results
                    </p>
                    <div style='display:flex;flex-direction:column;gap:6px'>
                        <div style='display:flex;align-items:center;gap:8px'>
                            <div style='width:5px;height:5px;border-radius:50%;
                                background:#9b8aff;flex-shrink:0'></div>
                            <span style='font-size:12px;color:#666'>Clear front-facing photo</span>
                        </div>
                        <div style='display:flex;align-items:center;gap:8px'>
                            <div style='width:5px;height:5px;border-radius:50%;
                                background:#9b8aff;flex-shrink:0'></div>
                            <span style='font-size:12px;color:#666'>Good natural lighting</span>
                        </div>
                        <div style='display:flex;align-items:center;gap:8px'>
                            <div style='width:5px;height:5px;border-radius:50%;
                                background:#9b8aff;flex-shrink:0'></div>
                            <span style='font-size:12px;color:#666'>Face and shoulders visible</span>
                        </div>
                        <div style='display:flex;align-items:center;gap:8px'>
                            <div style='width:5px;height:5px;border-radius:50%;
                                background:#9b8aff;flex-shrink:0'></div>
                            <span style='font-size:12px;color:#666'>Plain or simple background</span>
                        </div>
                    </div>
                </div>
                """)

            with gr.Column(scale=5):
                tryon_image = gr.Image(
                    label="",
                    height=480,
                    show_label=False
                )
                tryon_status = gr.HTML("""
                <div style='text-align:center;padding:10px 0 0'>
                    <p style='color:#ccc;font-size:12px'>
                        Your virtual try-on will appear here
                    </p>
                </div>""")

    # ── FOOTER ──
    gr.HTML("""
    <div style='text-align:center;padding:40px 20px 24px;margin-top:20px;
        border-top:1px solid #f0edf8'>
        <p style='color:#ddd;font-size:12px'>
            Built with CLIP · Stable Diffusion · IP-Adapter &nbsp;·&nbsp;
            <span style='color:#c4b5fd'>MoodBoard AI Fashion Stylist</span>
        </p>
    </div>
    """)

    generate_btn.click(
        fn=generate_outfit,
        inputs=[mood_input, seed_input],
        outputs=[outfit_image, style_card, tryon_section, tryon_section]
    )
    mood_input.submit(
        fn=generate_outfit,
        inputs=[mood_input, seed_input],
        outputs=[outfit_image, style_card, tryon_section, tryon_section]
    )
    tryon_btn.click(
        fn=generate_tryon,
        inputs=[face_input, tryon_seed],
        outputs=[tryon_image, tryon_status]
    )

if __name__ == "__main__":
    demo.launch(
        show_error=True,
        server_port=7860,
        theme=gr.themes.Base(),
        share=False
    )
