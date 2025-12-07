#!/usr/bin/env python3
"""
Neko Sonic Music Festival Poster
Based on the Neko Sonic design philosophy
4:3 ratio, anime-inspired, featuring kawaii cats
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# Canvas setup - 4:3 ratio
WIDTH = 1600
HEIGHT = 1200
DPI = 300

# Color palette - vibrant anime-inspired colors
PINK = (255, 105, 180)
ELECTRIC_BLUE = (0, 191, 255)
SUNSHINE_YELLOW = (255, 223, 0)
DEEP_PURPLE = (138, 43, 226)
SOFT_PINK = (255, 182, 193)
MINT = (152, 255, 152)
PEACH = (255, 218, 185)
LAVENDER = (230, 190, 255)
WHITE = (255, 255, 255)
CREAM = (255, 253, 240)
DARK_PINK = (199, 21, 133)

def create_gradient_background(width, height):
    """Create a vibrant gradient background"""
    img = Image.new('RGB', (width, height), CREAM)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Create soft gradient zones
    for y in range(height):
        progress = y / height
        # Blend from pink-purple to blue-yellow
        r = int(LAVENDER[0] * (1 - progress) + SOFT_PINK[0] * progress)
        g = int(LAVENDER[1] * (1 - progress) + SOFT_PINK[1] * progress)
        b = int(LAVENDER[2] * (1 - progress) + SOFT_PINK[2] * progress)
        draw.rectangle([(0, y), (width, y + 2)], fill=(r, g, b, 180))

    return img

def draw_cat_face(draw, x, y, size, rotation=0, color=PINK, outline_color=WHITE):
    """Draw a kawaii anime-style cat face"""
    # Main face circle
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=color, outline=outline_color, width=8)

    # Ears
    ear_size = size * 0.4
    # Left ear
    ear_points = [
        (x - size * 0.7, y - size * 0.5),
        (x - size * 0.9, y - size * 1.2),
        (x - size * 0.3, y - size * 0.8)
    ]
    draw.polygon(ear_points, fill=color, outline=outline_color)
    draw.ellipse([x - size * 0.75 - 15, y - size * 0.85 - 15,
                  x - size * 0.75 + 15, y - size * 0.85 + 15],
                 fill=DARK_PINK)

    # Right ear
    ear_points = [
        (x + size * 0.7, y - size * 0.5),
        (x + size * 0.9, y - size * 1.2),
        (x + size * 0.3, y - size * 0.8)
    ]
    draw.polygon(ear_points, fill=color, outline=outline_color)
    draw.ellipse([x + size * 0.75 - 15, y - size * 0.85 - 15,
                  x + size * 0.75 + 15, y - size * 0.85 + 15],
                 fill=DARK_PINK)

    # Eyes - big anime style
    eye_y = y - size * 0.2
    # Left eye
    draw.ellipse([x - size * 0.4 - 25, eye_y - 35,
                  x - size * 0.4 + 25, eye_y + 35],
                 fill=(40, 40, 60))
    draw.ellipse([x - size * 0.4 - 18, eye_y - 28,
                  x - size * 0.4 + 18, eye_y + 28],
                 fill=ELECTRIC_BLUE)
    # Highlight
    draw.ellipse([x - size * 0.4 - 10, eye_y - 20,
                  x - size * 0.4 + 5, eye_y - 5],
                 fill=WHITE)
    draw.ellipse([x - size * 0.4 + 8, eye_y + 10,
                  x - size * 0.4 + 15, eye_y + 17],
                 fill=(200, 230, 255))

    # Right eye
    draw.ellipse([x + size * 0.4 - 25, eye_y - 35,
                  x + size * 0.4 + 25, eye_y + 35],
                 fill=(40, 40, 60))
    draw.ellipse([x + size * 0.4 - 18, eye_y - 28,
                  x + size * 0.4 + 18, eye_y + 28],
                 fill=ELECTRIC_BLUE)
    # Highlight
    draw.ellipse([x + size * 0.4 - 10, eye_y - 20,
                  x + size * 0.4 + 5, eye_y - 5],
                 fill=WHITE)
    draw.ellipse([x + size * 0.4 + 8, eye_y + 10,
                  x + size * 0.4 + 15, eye_y + 17],
                 fill=(200, 230, 255))

    # Nose - small triangle
    nose_points = [
        (x, y + size * 0.1),
        (x - 12, y + size * 0.25),
        (x + 12, y + size * 0.25)
    ]
    draw.polygon(nose_points, fill=DARK_PINK)

    # Mouth - kawaii smile
    draw.arc([x - 30, y + size * 0.1, x + 30, y + size * 0.5],
             0, 180, fill=(40, 40, 60), width=6)

    # Whiskers
    whisker_color = (255, 255, 255, 200)
    # Left whiskers
    draw.line([x - size * 0.8, y, x - size * 1.3, y - 20], fill=whisker_color, width=4)
    draw.line([x - size * 0.8, y + 20, x - size * 1.3, y + 20], fill=whisker_color, width=4)
    draw.line([x - size * 0.8, y + 40, x - size * 1.3, y + 60], fill=whisker_color, width=4)

    # Right whiskers
    draw.line([x + size * 0.8, y, x + size * 1.3, y - 20], fill=whisker_color, width=4)
    draw.line([x + size * 0.8, y + 20, x + size * 1.3, y + 20], fill=whisker_color, width=4)
    draw.line([x + size * 0.8, y + 40, x + size * 1.3, y + 60], fill=whisker_color, width=4)

    # Cheek blush
    draw.ellipse([x - size * 0.85 - 20, y + size * 0.3 - 15,
                  x - size * 0.85 + 20, y + size * 0.3 + 15],
                 fill=(255, 150, 180, 100))
    draw.ellipse([x + size * 0.85 - 20, y + size * 0.3 - 15,
                  x + size * 0.85 + 20, y + size * 0.3 + 15],
                 fill=(255, 150, 180, 100))

def draw_music_note(draw, x, y, size, color, rotation=0):
    """Draw a music note"""
    # Note head
    draw.ellipse([x - size/2, y + size, x + size/2, y + size*2],
                 fill=color, outline=WHITE, width=3)
    # Stem
    draw.rectangle([x + size/2 - 6, y - size*2, x + size/2 + 6, y + size],
                   fill=color, outline=WHITE, width=3)
    # Flag
    flag_points = [
        (x + size/2, y - size*2),
        (x + size*1.5, y - size),
        (x + size/2, y - size*0.5)
    ]
    draw.polygon(flag_points, fill=color, outline=WHITE)

def draw_star(draw, x, y, size, color, points=5):
    """Draw a star shape"""
    coords = []
    for i in range(points * 2):
        angle = math.pi * 2 * i / (points * 2) - math.pi / 2
        r = size if i % 2 == 0 else size * 0.4
        coords.append((
            x + r * math.cos(angle),
            y + r * math.sin(angle)
        ))
    draw.polygon(coords, fill=color, outline=WHITE, width=3)

def draw_headphones(draw, x, y, size, color):
    """Draw kawaii headphones"""
    # Headband
    draw.arc([x - size, y - size*0.3, x + size, y + size*1.5],
             180, 360, fill=color, width=15)

    # Left ear cup
    draw.ellipse([x - size - 30, y + size*0.5 - 30,
                  x - size + 30, y + size*0.5 + 30],
                 fill=color, outline=WHITE, width=6)
    draw.ellipse([x - size - 20, y + size*0.5 - 20,
                  x - size + 20, y + size*0.5 + 20],
                 fill=DARK_PINK)

    # Right ear cup
    draw.ellipse([x + size - 30, y + size*0.5 - 30,
                  x + size + 30, y + size*0.5 + 30],
                 fill=color, outline=WHITE, width=6)
    draw.ellipse([x + size - 20, y + size*0.5 - 20,
                  x + size + 20, y + size*0.5 + 20],
                 fill=DARK_PINK)

# Create main image
print("Creating Neko Sonic Music Festival Poster...")
img = create_gradient_background(WIDTH, HEIGHT)
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay, 'RGBA')

# Add decorative circles in background
for _ in range(15):
    x = random.randint(100, WIDTH - 100)
    y = random.randint(100, HEIGHT - 100)
    size = random.randint(40, 120)
    colors = [PINK, ELECTRIC_BLUE, SUNSHINE_YELLOW, LAVENDER, MINT]
    color = random.choice(colors)
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(*color, 60), outline=(*WHITE, 100), width=4)

# Main cat character - center, large
main_cat_x = WIDTH // 2
main_cat_y = HEIGHT // 2 + 50
draw_cat_face(draw, main_cat_x, main_cat_y, 220, color=PINK)

# Add headphones to main cat
draw_headphones(draw, main_cat_x, main_cat_y - 50, 180, ELECTRIC_BLUE)

# Smaller cats - friends
draw_cat_face(draw, 300, 350, 110, color=SUNSHINE_YELLOW)
draw_cat_face(draw, WIDTH - 300, 380, 100, color=MINT)
draw_cat_face(draw, 250, HEIGHT - 250, 90, color=LAVENDER)
draw_cat_face(draw, WIDTH - 280, HEIGHT - 280, 95, color=PEACH)

# Music notes scattered around
note_positions = [
    (450, 200, 40, ELECTRIC_BLUE),
    (1150, 220, 35, PINK),
    (200, 600, 38, SUNSHINE_YELLOW),
    (1350, 650, 42, DEEP_PURPLE),
    (600, 950, 36, MINT),
    (1000, 980, 39, PINK),
]

for x, y, size, color in note_positions:
    draw_music_note(draw, x, y, size, color)

# Stars scattered
star_positions = [
    (150, 150, 30, SUNSHINE_YELLOW),
    (1450, 180, 28, PINK),
    (100, HEIGHT - 150, 32, ELECTRIC_BLUE),
    (1500, HEIGHT - 120, 27, LAVENDER),
    (800, 100, 35, MINT),
    (700, 1050, 29, DEEP_PURPLE),
    (1200, 1080, 31, SUNSHINE_YELLOW),
]

for x, y, size, color in star_positions:
    draw_star(draw, x, y, size, color)

# Composite overlay onto background
img = Image.alpha_composite(img.convert('RGBA'), overlay)

# Add text - minimal, as visual accent
text_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
text_draw = ImageDraw.Draw(text_layer)

# Try to load a fun font, fall back to default
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
    small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Title - top, bold and playful
title = "NEKO FEST"
bbox = text_draw.textbbox((0, 0), title, font=title_font)
title_width = bbox[2] - bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 80

# Add shadow/outline effect for title
for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
    text_draw.text((title_x + offset[0], title_y + offset[1]),
                   title, font=title_font, fill=DEEP_PURPLE)
text_draw.text((title_x, title_y), title, font=title_font, fill=WHITE)

# Subtitle
subtitle = "Summer Sonic"
bbox = text_draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = bbox[2] - bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = 220
text_draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font,
               fill=ELECTRIC_BLUE, stroke_width=2, stroke_fill=WHITE)

# Small details at bottom
detail = "2025"
bbox = text_draw.textbbox((0, 0), detail, font=small_font)
detail_width = bbox[2] - bbox[0]
detail_x = (WIDTH - detail_width) // 2
detail_y = HEIGHT - 80
text_draw.text((detail_x, detail_y), detail, font=small_font,
               fill=PINK, stroke_width=1, stroke_fill=WHITE)

# Composite text
img = Image.alpha_composite(img, text_layer)

# Convert back to RGB and save
img = img.convert('RGB')

# Apply slight texture for handmade feel
noise = Image.effect_noise((WIDTH, HEIGHT), 15)
img = Image.blend(img, noise.convert('RGB'), 0.03)

# Save final poster
output_path = '/Users/littlefatz/workspace/FE-DEMO/neko-sonic-poster.png'
img.save(output_path, 'PNG', dpi=(DPI, DPI), optimize=True)
print(f"✓ Poster saved: {output_path}")
print(f"  Dimensions: {WIDTH}x{HEIGHT} (4:3 ratio)")
print(f"  Style: Neko Sonic - Anime kawaii with music festival energy")
