# No API needed - smart local style translation using templates

STYLE_TEMPLATES = {
    "dark academia aesthetic outfit": {
        "colors": ["dark brown", "charcoal grey", "forest green", "cream"],
        "clothing": "oversized brown tweed blazer, high waisted plaid trousers, white oxford shirt, knit turtleneck sweater",
        "shoes": "worn leather oxford shoes",
        "accessories": "vintage leather satchel, round glasses",
        "lighting": "warm candlelight, moody shadows",
        "background": "old library with wooden shelves",
        "keywords": ["dark academia", "intellectual", "vintage", "layered", "moody"]
    },
    "cottagecore aesthetic outfit": {
        "colors": ["sage green", "dusty rose", "cream", "warm beige"],
        "clothing": "flowy floral midi dress, white puff sleeve blouse, linen pinafore",
        "shoes": "brown leather mary janes",
        "accessories": "woven straw basket, delicate gold necklace",
        "lighting": "soft golden hour sunlight",
        "background": "wildflower meadow, wooden cottage",
        "keywords": ["cottagecore", "romantic", "nature", "feminine", "whimsical"]
    },
    "Y2K fashion aesthetic": {
        "colors": ["hot pink", "electric blue", "silver", "white"],
        "clothing": "low rise flared jeans, cropped metallic jacket, butterfly print top",
        "shoes": "platform chunky sneakers",
        "accessories": "tinted sunglasses, mini shoulder bag",
        "lighting": "bright vibrant lighting",
        "background": "urban city street, neon signs",
        "keywords": ["Y2K", "retro", "bold", "playful", "nostalgic"]
    },
    "minimalist clean aesthetic outfit": {
        "colors": ["white", "beige", "light grey", "camel"],
        "clothing": "tailored beige trench coat, straight leg white trousers, fitted ribbed top",
        "shoes": "white leather loafers",
        "accessories": "simple gold jewelry, structured tote bag",
        "lighting": "clean bright natural light",
        "background": "minimal white studio",
        "keywords": ["minimalist", "clean", "elegant", "simple", "modern"]
    },
    "streetwear urban fashion": {
        "colors": ["black", "grey", "white", "orange"],
        "clothing": "oversized graphic hoodie, baggy cargo pants, cropped puffer jacket",
        "shoes": "chunky high top sneakers",
        "accessories": "baseball cap, crossbody bag",
        "lighting": "urban street lighting",
        "background": "city street, brick wall graffiti",
        "keywords": ["streetwear", "urban", "casual", "bold", "modern"]
    },
    "bohemian boho fashion": {
        "colors": ["rust orange", "turquoise", "warm brown", "gold"],
        "clothing": "flowy maxi skirt, embroidered peasant blouse, fringe suede vest",
        "shoes": "tan leather sandals",
        "accessories": "layered beaded necklaces, wide brim hat",
        "lighting": "warm sunset golden light",
        "background": "desert landscape, festival",
        "keywords": ["bohemian", "free spirited", "earthy", "layered", "artistic"]
    },
    "coastal grandmother aesthetic": {
        "colors": ["navy blue", "white", "sand beige", "soft blue"],
        "clothing": "linen wide leg trousers, striped navy top, oversized linen blazer",
        "shoes": "white canvas espadrilles",
        "accessories": "pearl necklace, canvas tote",
        "lighting": "bright coastal sunlight",
        "background": "beach house, ocean view",
        "keywords": ["coastal", "relaxed", "classic", "breezy", "elegant"]
    },
    "romantic feminine fashion": {
        "colors": ["blush pink", "ivory", "lavender", "soft red"],
        "clothing": "satin slip dress, lace trim blouse, chiffon wrap skirt",
        "shoes": "strappy heeled sandals",
        "accessories": "dainty pearl earrings, small evening bag",
        "lighting": "soft diffused golden light",
        "background": "blooming garden, cafe terrace",
        "keywords": ["romantic", "feminine", "delicate", "soft", "elegant"]
    },
    "edgy grunge fashion": {
        "colors": ["black", "dark red", "grey", "silver"],
        "clothing": "ripped black skinny jeans, oversized band tee, leather moto jacket",
        "shoes": "chunky black combat boots",
        "accessories": "silver chain necklace, studded belt",
        "lighting": "moody dark dramatic lighting",
        "background": "dark urban alley, concert venue",
        "keywords": ["grunge", "edgy", "dark", "rebellious", "rock"]
    },
    "preppy classic fashion": {
        "colors": ["navy", "forest green", "white", "red"],
        "clothing": "pleated plaid skirt, crisp white button down shirt, cable knit sweater",
        "shoes": "brown leather loafers",
        "accessories": "headband, structured handbag",
        "lighting": "bright clean natural daylight",
        "background": "college campus, green lawn",
        "keywords": ["preppy", "classic", "polished", "collegiate", "clean"]
    },
    "vintage retro 70s fashion": {
        "colors": ["mustard yellow", "burnt orange", "brown", "cream"],
        "clothing": "high waisted flared trousers, printed wrap blouse, suede fringe jacket",
        "shoes": "platform heeled boots",
        "accessories": "oversized tinted sunglasses, hobo bag",
        "lighting": "warm vintage film tone",
        "background": "retro diner, vintage car",
        "keywords": ["vintage", "retro", "70s", "groovy", "nostalgic"]
    },
    "athleisure sporty fashion": {
        "colors": ["black", "white", "neon green", "grey"],
        "clothing": "high waist leggings, sports bra, zip up windbreaker jacket",
        "shoes": "sleek running sneakers",
        "accessories": "sports cap, gym bag",
        "lighting": "bright energetic lighting",
        "background": "modern gym, city park",
        "keywords": ["sporty", "athletic", "modern", "functional", "dynamic"]
    },
    "artsy eclectic fashion": {
        "colors": ["cobalt blue", "emerald green", "mustard", "purple"],
        "clothing": "painted denim jacket, mixed print wide leg trousers, artistic graphic top",
        "shoes": "colorful block heel mules",
        "accessories": "statement earrings, handmade tote",
        "lighting": "creative studio lighting",
        "background": "art gallery, colorful murals",
        "keywords": ["artistic", "eclectic", "creative", "bold", "expressive"]
    },
    "soft girl pastel aesthetic": {
        "colors": ["baby pink", "lilac", "sky blue", "mint"],
        "clothing": "pastel pink mini skirt, white ruffle blouse, baby blue cardigan",
        "shoes": "white platform mary janes",
        "accessories": "hair clips, small backpack",
        "lighting": "soft dreamy light",
        "background": "pastel bedroom, cherry blossom park",
        "keywords": ["soft", "cute", "pastel", "dreamy", "youthful"]
    },
    "old money elegant fashion": {
        "colors": ["camel", "ivory", "navy", "dark green"],
        "clothing": "tailored camel wool coat, silk blouse, straight leg trousers",
        "shoes": "classic leather pumps",
        "accessories": "leather gloves, structured handbag",
        "lighting": "soft indoor warm lighting",
        "background": "grand estate, luxury hotel lobby",
        "keywords": ["elegant", "refined", "classic", "luxurious", "timeless"]
    }
}

def get_client():
    # No API needed for local mode
    print("Using local style templates (no API needed)")
    return None

def translate_mood_to_style(mood_text, matched_styles, client=None):
    # Get the top matched style
    top_style = matched_styles[0]["style"]
    
    # Look up the template for this style
    # If not found exactly, use the closest one
    template = STYLE_TEMPLATES.get(top_style)
    if not template:
        # fallback to first available
        template = list(STYLE_TEMPLATES.values())[0]
    
    # Build the Stable Diffusion prompt
    outfit_prompt = (
        f"fashion photography, professional model, full body shot, "
        f"woman wearing {template['clothing']}, {template['shoes']}, "
        f"{template['accessories']}, {template['lighting']}, "
        f"{template['background']}, high quality, detailed, realistic, "
        f"8k resolution"
    )
    
    return {
        "outfit_prompt": outfit_prompt,
        "color_palette": template["colors"],
        "style_keywords": template["keywords"],
        "occasion": f"Perfect for a casual {top_style.replace(' aesthetic outfit','').replace(' fashion','')} inspired day",
        "season": "All season"
    }

def build_negative_prompt():
    return (
        "low quality, blurry, distorted, deformed, ugly, bad anatomy, "
        "watermark, text, cartoon, anime, illustration, painting, "
        "extra limbs, missing limbs, bad hands"
    )
