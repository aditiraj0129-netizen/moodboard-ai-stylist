# styling_advisor.py
# Place this file in your src/ folder
# Usage: from src.styling_advisor import build_styling_html

STYLE_TEMPLATES = {
    "dark academia": {
        "colors": ["dark brown", "charcoal grey", "forest green", "cream"],
        "keywords": ["intellectual", "vintage", "layered", "moody", "classic"],
        "accessories": ["Vintage leather satchel", "Round wire-frame glasses", "Silver signet ring", "Leather belt with brass buckle", "Chunky knit scarf"],
        "shoes": ["Oxford brogues in tan or brown", "Chelsea boots in dark brown", "Loafers with tassel detail"],
        "heels": "Low block heel oxfords — 2 inch max keeps it authentic",
        "hairstyle": ["Loose low bun with face-framing tendrils", "Half-up half-down with a pencil through it", "Sleek middle part with tucked ends"],
        "makeup": "light",
        "makeup_details": {"Base": "Light coverage, barely-there concealer", "Eyes": "Warm brown shadow, thin upper liner, mascara only", "Lips": "Dusty rose or terracotta lip balm tint", "Blush": "Soft peach blush swept naturally", "Finish": "Matte — no highlight for this aesthetic"},
        "nails": "Deep burgundy, forest green, or nude beige",
        "fragrance": "Woody, leather, sandalwood notes",
        "tip": "Layer a chunky knit cardigan over your blazer on colder days"
    },
    "cottagecore": {
        "colors": ["sage green", "dusty rose", "cream", "warm beige"],
        "keywords": ["romantic", "nature", "feminine", "whimsical", "soft"],
        "accessories": ["Woven straw hat", "Delicate gold chain necklace", "Small floral hair clips", "Wicker basket bag", "Thin gold rings stacked"],
        "shoes": ["Brown leather Mary Janes", "White canvas lace-up boots", "Simple leather sandals with ankle strap"],
        "heels": "Low kitten heels in nude or brown — keeps the whimsy",
        "hairstyle": ["Loose braided crown with wildflowers", "Soft wavy hair down with ribbon", "Low pigtail braids tied with lace"],
        "makeup": "light",
        "makeup_details": {"Base": "Skin-tint or tinted moisturiser only", "Eyes": "No liner — just curled lashes and clear mascara", "Lips": "Sheer pink or peach lip gloss", "Blush": "Heavy rosy blush — the garden-fresh flush look", "Finish": "Dewy glowy skin — the fresher the better"},
        "nails": "Soft pink, lavender, or floral nail art",
        "fragrance": "Floral, rose, fresh grass notes",
        "tip": "Add an apron-style pinafore over a white blouse for full cottagecore"
    },
    "Y2K": {
        "colors": ["hot pink", "electric blue", "silver", "white"],
        "keywords": ["Y2K", "retro", "bold", "playful", "maximalist"],
        "accessories": ["Butterfly hair clips everywhere", "Tinted mini sunglasses", "Tiny silver choker", "Mini rhinestone bag", "Layered thin chains"],
        "shoes": ["Platform chunky sneakers", "Strappy block heel sandals with rhinestones", "Clear PVC mules"],
        "heels": "Chunky platform heels 3-4 inches — the Y2K staple",
        "hairstyle": ["Space buns with face framing pieces", "High ponytail with baby hairs laid", "Straight sleek with butterfly clips at sides"],
        "makeup": "dark",
        "makeup_details": {"Base": "Full coverage matte skin", "Eyes": "Graphic liner — winged or coloured. Glitter on lids", "Lips": "Nude gloss or hot pink. Overline slightly", "Blush": "Pop of pink or coral on the apples", "Finish": "Dewy skin with shimmer highlight on cheekbones"},
        "nails": "Long almond nails — chrome, holographic or rhinestone art",
        "fragrance": "Sweet, fruity, vanilla bomb",
        "tip": "The more accessories the better — Y2K is maximalist"
    },
    "minimalist": {
        "colors": ["white", "beige", "light grey", "camel"],
        "keywords": ["minimalist", "clean", "elegant", "simple", "modern"],
        "accessories": ["Single thin gold chain", "Small stud earrings", "One delicate ring", "Structured leather tote in camel"],
        "shoes": ["White leather loafers", "Pointed toe ballet flats in nude", "Clean white sneakers"],
        "heels": "Pointed toe kitten heels in nude or beige — elongates silhouette",
        "hairstyle": ["Sleek low ponytail", "Clean middle part straight blowout", "Tight low bun — no flyaways"],
        "makeup": "light",
        "makeup_details": {"Base": "Skin-tint, spot conceal only", "Eyes": "Clear brow gel, one coat mascara, nothing else", "Lips": "Nude gloss or your lips but better", "Blush": "Very subtle peach or terracotta draping", "Finish": "Natural satin skin"},
        "nails": "Clean nude, sheer pink, or classic french",
        "fragrance": "Clean, musky, white tea, light citrus",
        "tip": "Remove one accessory before leaving — less is always more"
    },
    "streetwear": {
        "colors": ["black", "grey", "white", "orange"],
        "keywords": ["urban", "streetwear", "bold", "casual", "hype"],
        "accessories": ["Fitted cap or bucket hat", "Chunky gold chain", "Small crossbody bag", "Hoop earrings", "Sports socks pulled up"],
        "shoes": ["Chunky dad sneakers", "High top Air Force 1s", "Timberland boots"],
        "heels": "Chunky platform boots if you want height — keeps the street edge",
        "hairstyle": ["Slicked back bun", "High puff or ponytail", "Box braids or cornrows", "Cap over loose waves"],
        "makeup": "dark",
        "makeup_details": {"Base": "Medium to full coverage matte", "Eyes": "Bold graphic liner. Fluffy lashes", "Lips": "Dark brown liner with nude gloss or bold red", "Blush": "Bronzer first then pop of colour", "Finish": "Matte base, shine only on lips"},
        "nails": "Square long nails — black, dark red, or graphic art",
        "fragrance": "Oud, amber, strong musk",
        "tip": "Oversized is key — size up on the hoodie or jacket"
    },
    "romantic": {
        "colors": ["blush pink", "ivory", "lavender", "soft red"],
        "keywords": ["romantic", "feminine", "delicate", "soft", "elegant"],
        "accessories": ["Pearl drop earrings", "Delicate gold bracelet", "Satin hair bow", "Embroidered mini bag", "Thin layered necklaces"],
        "shoes": ["Strappy heeled sandals in nude", "Satin ballet flats with bow", "Kitten heel mules in blush"],
        "heels": "Strappy stilettos in nude or blush — 3 inches elevates the romance",
        "hairstyle": ["Soft curls half up with ribbon", "Loose romantic updo with face curls", "Long loose waves with flower pin"],
        "makeup": "light",
        "makeup_details": {"Base": "Luminous medium coverage", "Eyes": "Soft pink shimmer, white inner corner, fluffy lashes", "Lips": "Rosy pink lipstick or cherry gloss", "Blush": "Pink blush heavily on apples — doll-like", "Finish": "Glowy dewy skin"},
        "nails": "Soft pink, baby blue, or glazed donut chrome",
        "fragrance": "Rose, peony, soft powdery florals",
        "tip": "A delicate lace cardigan adds the final romantic layer"
    },
    "boho": {
        "colors": ["rust orange", "turquoise", "warm brown", "gold"],
        "keywords": ["bohemian", "free spirited", "earthy", "layered", "artistic"],
        "accessories": ["Layered beaded necklaces 3-4 strands", "Stacked bangle bracelets", "Feather earrings", "Wide brim felt hat", "Fringe bag"],
        "shoes": ["Flat tan leather sandals", "Suede ankle boots with fringe", "Beaded slide sandals"],
        "heels": "Wedge heel espadrilles — boho and practical",
        "hairstyle": ["Loose beach waves", "Long braids with gold thread woven in", "Messy half-up with fabric scarf tied in"],
        "makeup": "light",
        "makeup_details": {"Base": "Tinted SPF or light BB cream", "Eyes": "Earthy bronze shimmer, smudged brown pencil liner", "Lips": "Terracotta or brick with gloss over", "Blush": "Sun-kissed bronzer on nose and cheeks", "Finish": "Golden glowy skin — like you've been in the sun"},
        "nails": "Earthy tones — rust, terracotta, sage green",
        "fragrance": "Patchouli, amber, ylang ylang",
        "tip": "Mix patterns freely — florals with paisley is very boho"
    },
    "old money": {
        "colors": ["camel", "ivory", "navy", "dark green"],
        "keywords": ["elegant", "refined", "classic", "luxurious", "timeless"],
        "accessories": ["Single strand of pearls", "Gold stud or hoop earrings", "Classic leather gloves", "Structured Chanel-style bag", "Thin gold watch"],
        "shoes": ["Classic leather pumps in nude or black", "Pointed toe loafers", "Clean ankle strap heels"],
        "heels": "Classic pointed-toe pumps 2.5-3 inches — timeless and powerful",
        "hairstyle": ["Sleek blowout with side part", "French twist or low chignon", "Smooth low ponytail with silk scarf"],
        "makeup": "light",
        "makeup_details": {"Base": "Flawless medium coverage — no visible pores", "Eyes": "Thin precise liner, natural shadow, defined brows", "Lips": "Classic red, deep nude, or dusty rose", "Blush": "Subtle sculpting — more contour than blush", "Finish": "Polished satin — like you have good genes"},
        "nails": "Classic red, nude, or ballet pink — always clean and filed",
        "fragrance": "Chanel No.5 vibes — aldehydic, iris, jasmine",
        "tip": "The fit and tailoring matters more than the brand — get things hemmed"
    },
    "grunge": {
        "colors": ["black", "dark red", "grey", "silver"],
        "keywords": ["grunge", "edgy", "dark", "rebellious", "rock"],
        "accessories": ["Chunky silver chain", "Studded belt", "Black leather cuff bracelet", "Fishnet details", "Small skull or star earrings"],
        "shoes": ["Chunky black combat boots — non-negotiable", "Platform creepers", "Black leather ankle boots"],
        "heels": "Platform heeled boots 4-5 inches — still edgy",
        "hairstyle": ["Messy textured waves", "Half-up with face framing pieces dyed", "Sleek straight with heavy fringe"],
        "makeup": "dark",
        "makeup_details": {"Base": "Full coverage matte or slightly dewy", "Eyes": "Heavy black kohl — top and bottom. Smudged. Dark shadow in crease", "Lips": "Dark berry, black-red, or deep plum", "Blush": "Minimal — light bronzer only or skip", "Finish": "Pale base with bold eye and lip — contrast is key"},
        "nails": "Black, dark purple, or chipped nail polish is iconic",
        "fragrance": "Dark woods, smoke, black musk",
        "tip": "Layer a flannel shirt around your waist to complete the grunge"
    },
    "pastel": {
        "colors": ["baby pink", "lilac", "sky blue", "mint"],
        "keywords": ["soft", "cute", "pastel", "dreamy", "youthful"],
        "accessories": ["Lots of hair clips and bows", "Pastel beaded jewellery", "Mini heart or star earrings", "Small pastel coloured bag", "Thin charm bracelets"],
        "shoes": ["White platform Mary Janes", "Pastel coloured sneakers", "Clear jelly sandals"],
        "heels": "Low chunky heels in pastel — cute not too tall",
        "hairstyle": ["Twin space buns with bows", "High ponytail with scrunchie", "Side pigtails with clips everywhere"],
        "makeup": "light",
        "makeup_details": {"Base": "Light coverage poreless finish", "Eyes": "Pink or lilac shimmer, lower pink liner, big doll lashes", "Lips": "Pink glossy lip — the glossier the better", "Blush": "Flushed pink high on cheeks and tip of nose", "Finish": "Extremely dewy — like a glazed donut"},
        "nails": "Pastel pink, baby blue, or strawberry milk chrome",
        "fragrance": "Cotton candy, bubblegum, sweet florals",
        "tip": "Layering pastel colours together is encouraged — clash softly"
    }
}


def build_styling_html(matched_style, color_palette, style_keywords, mood):
    """
    Builds a beautiful dark-themed HTML styling card.
    matched_style: string key e.g. 'dark academia'
    color_palette: list of color strings
    style_keywords: list of keyword strings
    mood: the original mood text the user typed
    """

    # Find the right template
    s = None
    for key in STYLE_TEMPLATES:
        if key in matched_style.lower():
            s = STYLE_TEMPLATES[key]
            style_name = key.title()
            break
    if s is None:
        s = STYLE_TEMPLATES["minimalist"]
        style_name = "Minimalist"

    makeup_color = "#f43f5e" if s["makeup"] == "dark" else "#a78bfa"
    makeup_label = "✦ Dark Glam Makeup" if s["makeup"] == "dark" else "✦ Light Natural Makeup"

    # Color swatches
    swatches = "".join([
        f"<span style='display:inline-flex;align-items:center;gap:5px;"
        f"background:#1e1e3f;border-radius:20px;padding:3px 10px;margin:2px'>"
        f"<span style='width:12px;height:12px;border-radius:50%;background:{c};"
        f"border:1px solid rgba(255,255,255,0.15);display:inline-block'></span>"
        f"<span style='color:#ccc;font-size:11px'>{c}</span></span>"
        for c in color_palette
    ])

    # Keyword pills
    kw_pills = "".join([
        f"<span style='background:#2d1b6922;border:1px solid #667eea33;"
        f"color:#a78bfa;padding:3px 10px;border-radius:20px;"
        f"font-size:11px;margin:2px;display:inline-block'>{k}</span>"
        for k in style_keywords
    ])

    # Accessories
    acc_items = "".join([
        f"<div style='display:flex;align-items:center;gap:8px;padding:5px 0;"
        f"border-bottom:1px solid #1a1a35'>"
        f"<span style='color:#667eea;font-size:12px'>◆</span>"
        f"<span style='color:#ddd;font-size:12px'>{a}</span></div>"
        for a in s["accessories"]
    ])

    # Shoes
    shoe_items = "".join([
        f"<div style='display:flex;align-items:center;gap:8px;padding:4px 0'>"
        f"<span style='color:#ec4899;font-size:11px'>▸</span>"
        f"<span style='color:#ddd;font-size:12px'>{sh}</span></div>"
        for sh in s["shoes"]
    ])

    # Hair
    hair_items = "".join([
        f"<div style='display:flex;align-items:center;gap:8px;padding:4px 0'>"
        f"<span style='color:#a78bfa;font-size:11px'>✦</span>"
        f"<span style='color:#ddd;font-size:12px'>{h}</span></div>"
        for h in s["hairstyle"]
    ])

    # Makeup steps
    makeup_rows = "".join([
        f"<div style='display:flex;justify-content:space-between;"
        f"padding:5px 0;border-bottom:1px solid #1a1a35'>"
        f"<span style='color:#666;font-size:11px;text-transform:capitalize'>{step}</span>"
        f"<span style='color:#ddd;font-size:11px;text-align:right;max-width:200px'>{desc}</span></div>"
        for step, desc in s["makeup_details"].items()
    ])

    return f"""
<div style='background:#0d0d1a;border-radius:16px;padding:22px;
    font-family:Inter,sans-serif;border:1px solid #1e1e3f;margin-top:12px'>

    <div style='display:flex;justify-content:space-between;align-items:center;
        margin-bottom:16px;flex-wrap:wrap;gap:8px'>
        <h2 style='font-size:1.1rem;font-weight:700;margin:0;
            background:linear-gradient(135deg,#667eea,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
            ✨ Your Complete Style Guide
        </h2>
        <span style='background:linear-gradient(135deg,#667eea,#764ba2);
            color:white;padding:4px 14px;border-radius:20px;
            font-size:11px;font-weight:600'>{style_name}</span>
    </div>
    <p style='color:#444;font-size:12px;margin:0 0 16px'>Mood: "{mood}"</p>

    <div style='background:#13132b;border-radius:12px;padding:14px;margin-bottom:10px'>
        <p style='color:#666;font-size:10px;letter-spacing:2px;
            text-transform:uppercase;margin:0 0 8px'>🎨 Color Palette</p>
        {swatches}
    </div>

    <div style='background:#13132b;border-radius:12px;padding:14px;margin-bottom:10px'>
        <p style='color:#666;font-size:10px;letter-spacing:2px;
            text-transform:uppercase;margin:0 0 8px'>✦ Vibe Keywords</p>
        {kw_pills}
    </div>

    <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px'>
        <div style='background:#13132b;border-radius:12px;padding:14px'>
            <p style='color:#667eea;font-size:10px;letter-spacing:2px;
                text-transform:uppercase;margin:0 0 10px'>💎 Accessories</p>
            {acc_items}
        </div>
        <div style='background:#13132b;border-radius:12px;padding:14px'>
            <p style='color:#a78bfa;font-size:10px;letter-spacing:2px;
                text-transform:uppercase;margin:0 0 10px'>💇 Hairstyles</p>
            {hair_items}
        </div>
    </div>

    <div style='background:#13132b;border-radius:12px;padding:14px;margin-bottom:10px'>
        <p style='color:#ec4899;font-size:10px;letter-spacing:2px;
            text-transform:uppercase;margin:0 0 10px'>👠 Shoes & Heels</p>
        {shoe_items}
        <div style='margin-top:8px;padding:8px;background:#0d0d1a;border-radius:8px'>
            <span style='color:#ec4899;font-size:11px'>Heels tip: </span>
            <span style='color:#888;font-size:11px'>{s["heels"]}</span>
        </div>
    </div>

    <div style='background:#13132b;border-radius:12px;padding:14px;margin-bottom:10px'>
        <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px'>
            <p style='color:{makeup_color};font-size:10px;letter-spacing:2px;
                text-transform:uppercase;margin:0'>💄 Makeup Look</p>
            <span style='background:{makeup_color}22;color:{makeup_color};
                padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600'>
                {makeup_label}
            </span>
        </div>
        {makeup_rows}
    </div>

    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px'>
        <div style='background:#13132b;border-radius:12px;padding:12px'>
            <p style='color:#f59e0b;font-size:10px;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 6px'>💅 Nails</p>
            <p style='color:#ddd;font-size:12px;margin:0'>{s["nails"]}</p>
        </div>
        <div style='background:#13132b;border-radius:12px;padding:12px'>
            <p style='color:#34d399;font-size:10px;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 6px'>🌸 Fragrance</p>
            <p style='color:#ddd;font-size:12px;margin:0'>{s["fragrance"]}</p>
        </div>
        <div style='background:#13132b;border-radius:12px;padding:12px'>
            <p style='color:#60a5fa;font-size:10px;letter-spacing:1.5px;
                text-transform:uppercase;margin:0 0 6px'>💡 Pro Tip</p>
            <p style='color:#ddd;font-size:12px;margin:0'>{s["tip"]}</p>
        </div>
    </div>
</div>"""
