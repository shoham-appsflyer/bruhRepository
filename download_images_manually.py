"""
Helper script to download animal images from Unsplash.
Run this script separately to populate the animal_images/ directory.

Usage:
    python download_images_manually.py
"""
import logging
import time
from pathlib import Path

import requests
from animal_data import CRITICALLY_ENDANGERED_ANIMALS, EXTINCT_ANIMALS

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

IMAGE_CACHE_DIR = Path("animal_images")
IMAGE_CACHE_DIR.mkdir(exist_ok=True)

UNSPLASH_BASE = "https://source.unsplash.com/300x300/?"


def download_image(animal_name: str) -> bool:
    cache_path = IMAGE_CACHE_DIR / f"{animal_name.replace(' ', '_')}.jpg"
    
    if cache_path.exists():
        logger.info(f"✓ {animal_name} - Already downloaded")
        return True
    
    search_term = animal_name.replace(" ", "+")
    url = f"{UNSPLASH_BASE}{search_term},animal,wildlife"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        with open(cache_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"✓ {animal_name} - Downloaded successfully")
        time.sleep(1)
        return True
        
    except Exception as e:
        logger.error(f"✗ {animal_name} - Failed: {e}")
        return False


def main():
    all_animals = CRITICALLY_ENDANGERED_ANIMALS + EXTINCT_ANIMALS
    
    logger.info(f"Starting download of {len(all_animals)} animal images...")
    logger.info("This may take a few minutes...\n")
    
    successful = 0
    failed = 0
    
    for animal in all_animals:
        if download_image(animal['name']):
            successful += 1
        else:
            failed += 1
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Download complete!")
    logger.info(f"Successful: {successful}/{len(all_animals)}")
    logger.info(f"Failed: {failed}/{len(all_animals)}")
    logger.info(f"{'='*60}")
    
    if failed > 0:
        logger.warning("\nSome images failed to download. You can:")
        logger.warning("1. Run this script again")
        logger.warning("2. Manually download images from:")
        logger.warning("   - https://unsplash.com")
        logger.warning("   - https://pixabay.com")
        logger.warning("   - https://commons.wikimedia.org")
        logger.warning("\nSave images as: animal_images/<Animal_Name>.jpg")


if __name__ == "__main__":
    main()

