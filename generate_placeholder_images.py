"""
Generate colorful placeholder images for all animals.
This creates nice-looking images with gradients and animal initials.
"""
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from animal_data import CRITICALLY_ENDANGERED_ANIMALS, EXTINCT_ANIMALS

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

IMAGE_CACHE_DIR = Path("animal_images")
IMAGE_CACHE_DIR.mkdir(exist_ok=True)

COLORS = [
    ('#FF6B6B', '#C44569'), ('#4ECDC4', '#44A08D'), ('#45B7D1', '#2980B9'),
    ('#FFA07A', '#FA8BFF'), ('#98D8C8', '#52B788'), ('#F7DC6F', '#F39C12'),
    ('#BB8FCE', '#9B59B6'), ('#85C1E2', '#5DADE2'), ('#F8B739', '#F39C12'),
    ('#52B788', '#27AE60'), ('#E63946', '#C0392B'), ('#A8DADC', '#7FB3D5'),
    ('#457B9D', '#2E86AB'), ('#F1FAEE', '#E8F8F5'), ('#1D3557', '#2C3E50'),
    ('#D4A5A5', '#C39BD3'), ('#9381FF', '#7B68EE'), ('#FFD6A5', '#FBBF77'),
    ('#CAFFBF', '#A8E6CF'), ('#FDFFB6', '#F9E79F'), ('#FFD6FF', '#F8B4D9'),
    ('#E7C6FF', '#D7BDE2'), ('#C8B6FF', '#BB8FCE'), ('#B8C0FF', '#A9B9EA'),
    ('#BBD0FF', '#7FB3D5'), ('#AED9E0', '#85C1E2'), ('#FAF3DD', '#F9E79F'),
    ('#C8D5B9', '#A3C894'), ('#8FC0A9', '#6FA285'), ('#68B0AB', '#4A7C7E'),
    ('#4A7C7E', '#2C5F63'), ('#D4939D', '#C39BD3'), ('#FFAFCC', '#F8B4D9'),
    ('#BDE0FE', '#7FB3D5'), ('#A2D2FF', '#85C1E2'), ('#CDB4DB', '#BB8FCE'),
    ('#FFC8DD', '#F8B4D9'), ('#FFAFCC', '#F8B4D9'), ('#BDE0FE', '#7FB3D5'),
    ('#A2D2FF', '#85C1E2'),
]


def create_gradient_image(width: int, height: int, color1: str, color2: str) -> Image.Image:
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    
    for y in range(height):
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def generate_image(animal_name: str, index: int) -> bool:
    cache_path = IMAGE_CACHE_DIR / f"{animal_name.replace(' ', '_')}.jpg"
    
    if cache_path.exists():
        logger.info(f"✓ {animal_name} - Already exists")
        return True
    
    try:
        color1, color2 = COLORS[index % len(COLORS)]
        img = create_gradient_image(300, 300, color1, color2)
        draw = ImageDraw.Draw(img)
        
        initials = ''.join([word[0] for word in animal_name.split()[:2]]).upper()
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (300 - text_width) // 2
        y = (300 - text_height) // 2 - 20
        
        draw.text((x+3, y+3), initials, fill='rgba(0,0,0,50)', font=font)
        draw.text((x, y), initials, fill='white', font=font)
        
        draw.ellipse([10, 10, 290, 290], outline='white', width=8)
        
        img.save(cache_path, "JPEG", quality=95)
        logger.info(f"✓ {animal_name} - Generated successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ {animal_name} - Failed: {e}")
        return False


def main():
    all_animals = CRITICALLY_ENDANGERED_ANIMALS + EXTINCT_ANIMALS
    
    logger.info(f"Generating {len(all_animals)} animal placeholder images...")
    logger.info("This will take a few seconds...\n")
    
    successful = 0
    failed = 0
    
    for index, animal in enumerate(all_animals):
        if generate_image(animal['name'], index):
            successful += 1
        else:
            failed += 1
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Generation complete!")
    logger.info(f"Successful: {successful}/{len(all_animals)}")
    logger.info(f"Failed: {failed}/{len(all_animals)}")
    logger.info(f"{'='*60}")
    logger.info(f"\nImages saved to: {IMAGE_CACHE_DIR.absolute()}")
    logger.info("Run 'python main.py' to see the animals with images!")


if __name__ == "__main__":
    main()

