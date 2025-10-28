import logging
import warnings
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from PIL import Image
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings('ignore', category=InsecureRequestWarning)

logger = logging.getLogger(__name__)

IMAGE_CACHE_DIR = Path("animal_images")
IMAGE_CACHE_DIR.mkdir(exist_ok=True)

ANIMAL_IMAGE_URLS = {
    "Javan Rhino": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&q=80",
    "Vaquita": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&q=80",
    "Amur Leopard": "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=300&q=80",
    "Black Rhino": "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&q=80",
    "Bornean Orangutan": "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&q=80",
    "Cross River Gorilla": "https://images.unsplash.com/photo-1551135049-8a33b5883817?w=300&q=80",
    "Hawksbill Turtle": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=300&q=80",
    "Saola": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=300&q=80",
    "South China Tiger": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&q=80",
    "Sumatran Elephant": "https://images.unsplash.com/photo-1564760290292-23341e4df6ec?w=300&q=80",
    "Sumatran Orangutan": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=300&q=80",
    "Sumatran Rhino": "https://images.unsplash.com/photo-1553830591-d8632a99e6ff?w=300&q=80",
    "Sunda Tiger": "https://images.unsplash.com/photo-1602491453631-e2a5ad90a131?w=300&q=80",
    "Yangtze Finless Porpoise": "https://images.unsplash.com/photo-1568430462989-44163eb1752f?w=300&q=80",
    "Philippine Eagle": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&q=80",
    "Kakapo": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&q=80",
    "Addax": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=300&q=80",
    "Chinese Pangolin": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&q=80",
    "Mountain Gorilla": "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&q=80",
    "Siamese Crocodile": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&q=80",
    "Dodo": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=300&q=80",
    "Tasmanian Tiger": "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&q=80",
    "Passenger Pigeon": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=300&q=80",
    "Woolly Mammoth": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&q=80",
    "Steller's Sea Cow": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&q=80",
    "Great Auk": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&q=80",
    "Caribbean Monk Seal": "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=300&q=80",
    "Quagga": "https://images.unsplash.com/photo-1553830591-d8632a99e6ff?w=300&q=80",
    "West African Black Rhino": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&q=80",
    "Baiji River Dolphin": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&q=80",
    "Golden Toad": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&q=80",
    "Pyrenean Ibex": "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&q=80",
    "Japanese Sea Lion": "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=300&q=80",
    "Toolache Wallaby": "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&q=80",
    "Atlas Bear": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=300&q=80",
    "Caspian Tiger": "https://images.unsplash.com/photo-1602491453631-e2a5ad90a131?w=300&q=80",
    "Carolina Parakeet": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&q=80",
    "Schomburgk's Deer": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=300&q=80",
    "Falkland Islands Wolf": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=300&q=80",
    "Moa": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=300&q=80",
}


def download_animal_image(animal_name: str) -> Optional[Image.Image]:
    cache_path = IMAGE_CACHE_DIR / f"{animal_name.replace(' ', '_')}.jpg"
    
    if cache_path.exists():
        logger.debug(f"Loading cached image for {animal_name}")
        return Image.open(cache_path)
    
    url = ANIMAL_IMAGE_URLS.get(animal_name)
    if not url:
        logger.warning(f"No URL found for {animal_name}")
        return None
    
    try:
        logger.info(f"Downloading image for {animal_name}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.save(cache_path, "JPEG")
        logger.info(f"Successfully downloaded and cached image for {animal_name}")
        return img
        
    except Exception as e:
        logger.error(f"Failed to download image for {animal_name}: {e}")
        return None


def resize_image_for_display(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    return img
