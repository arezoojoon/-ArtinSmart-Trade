from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, path):
    img = Image.new('RGB', (size, size), color='#0f172a')
    d = ImageDraw.Draw(img)
    
    # Draw a simple gold "T" or shape
    # Gold color: #f59e0b
    
    # Draw a circle
    margin = size // 5
    d.ellipse([margin, margin, size-margin, size-margin], outline='#f59e0b', width=size//20)
    
    # Draw Text "TM"
    # rudimentary drawing since we might not have fonts
    # Vertical line of T
    center = size // 2
    width = size // 10
    top = size // 3
    bottom = size - top
    
    # T Crossbar
    d.rectangle([center - size//4, top, center + size//4, top + width], fill='#f59e0b')
    # T Stem
    d.rectangle([center - width//2, top, center + width//2, bottom], fill='#f59e0b')

    # Ensure dir exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"Created {path}")

create_icon(192, 'public/icons/icon-192x192.png')
create_icon(512, 'public/icons/icon-512x512.png')
