"""
generate_extension_icons.py - Generate extension icons for Blogger AI Studio Booster
"""
from PIL import Image, ImageDraw, ImageFont
import os

sizes = [16, 48, 128]
ext_dir = os.path.join(os.path.dirname(__file__), "chrome_extension")
os.makedirs(ext_dir, exist_ok=True)

for size in sizes:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded background with indigo-violet gradient feel
    corner_radius = int(size * 0.22)
    bg_color = (99, 102, 241, 255) # Modern Indigo #6366f1
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=corner_radius, fill=bg_color)
    
    # Inner border / glow
    border_color = (168, 85, 247, 255) # Purple #a855f7
    draw.rounded_rectangle([(1, 1), (size - 2, size - 2)], radius=corner_radius, outline=border_color, width=max(1, int(size * 0.05)))
    
    # White "B" letter in center
    try:
        font_size = int(size * 0.6)
        font = ImageFont.truetype("Roboto-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
        
    text = "B"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = (size - th) // 2 - int(size * 0.06)
    
    draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    
    out_path = os.path.join(ext_dir, f"icon{size}.png")
    img.save(out_path, "PNG")
    print(f"Generated {out_path} ({size}x{size})")
