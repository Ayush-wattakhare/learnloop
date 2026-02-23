"""
Generate PWA icons for LearnLoop
Run: python generate_icons.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a LearnLoop icon with gradient background"""
    # Create image with gradient
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background (blue to purple)
    for y in range(size):
        # Calculate color for this row
        ratio = y / size
        r = int(29 + (124 - 29) * ratio)  # 1D4ED8 to 7C3AED
        g = int(78 + (62 - 78) * ratio)
        b = int(216 + (237 - 216) * ratio)
        draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b))
    
    # Add emoji/text
    try:
        # Try to use a font
        font_size = int(size * 0.5)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw text (📚 emoji or "SM")
    text = "📚"
    
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw white text
    draw.text((x, y), text, fill='white', font=font)
    
    # Save
    img.save(output_path, 'PNG')
    print(f"✅ Created: {output_path}")

def main():
    """Generate all required icon sizes"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Create icons directory if it doesn't exist
    os.makedirs('static/icons', exist_ok=True)
    
    print("🎨 Generating PWA icons...")
    
    for size in sizes:
        output_path = f'static/icons/icon-{size}x{size}.png'
        create_icon(size, output_path)
    
    print("\n✅ All icons generated successfully!")
    print("📱 Your PWA is ready for mobile installation!")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ PIL/Pillow not installed")
        print("📦 Install with: pip install Pillow")
        print("\n💡 Alternative: Use online icon generator:")
        print("   - https://realfavicongenerator.net/")
        print("   - https://www.pwabuilder.com/")
