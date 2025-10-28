import logging
import os
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from PIL import Image

logger = logging.getLogger(__name__)

IMAGE_CACHE_DIR = Path("animal_images")
IMAGE_CACHE_DIR.mkdir(exist_ok=True)

ANIMAL_IMAGE_URLS = {
    "Javan Rhino": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rhinoceros_sondaicus_in_London_Zoo.jpg/320px-Rhinoceros_sondaicus_in_London_Zoo.jpg",
    "Vaquita": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Vaquita.jpg/320px-Vaquita.jpg",
    "Amur Leopard": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Amur_Leopard_%2815218490357%29.jpg/320px-Amur_Leopard_%2815218490357%29.jpg",
    "Black Rhino": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Black_rhino.jpg/320px-Black_rhino.jpg",
    "Bornean Orangutan": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Bornean_orangutan_%28Pongo_pygmaeus%29_in_tree.jpg/320px-Bornean_orangutan_%28Pongo_pygmaeus%29_in_tree.jpg",
    "Cross River Gorilla": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Male_gorilla_in_SF_zoo.jpg/320px-Male_gorilla_in_SF_zoo.jpg",
    "Hawksbill Turtle": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Hawksbill_turtle_doeppne-081.jpg/320px-Hawksbill_turtle_doeppne-081.jpg",
    "Saola": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Saola.jpg/320px-Saola.jpg",
    "South China Tiger": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Panthera_tigris_amoyensis_qtl1.jpg/320px-Panthera_tigris_amoyensis_qtl1.jpg",
    "Sumatran Elephant": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Elephas_maximus_sumatranus_-_Ragunan_Zoo.jpg/320px-Elephas_maximus_sumatranus_-_Ragunan_Zoo.jpg",
    "Sumatran Orangutan": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG/320px-Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG",
    "Sumatran Rhino": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Sumatran_Rhino_Way_Kambas_2008.jpg/320px-Sumatran_Rhino_Way_Kambas_2008.jpg",
    "Sunda Tiger": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Sumatran_tiger_%28Panthera_tigris_sumatrae%29.jpg/320px-Sumatran_tiger_%28Panthera_tigris_sumatrae%29.jpg",
    "Yangtze Finless Porpoise": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Yangtze_finless_porpoise.jpg/320px-Yangtze_finless_porpoise.jpg",
    "Philippine Eagle": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Philippine_Eagle.jpg/320px-Philippine_Eagle.jpg",
    "Kakapo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Sirocco_4.jpg/320px-Sirocco_4.jpg",
    "Addax": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Addax_%28Addax_nasomaculatus%29.jpg/320px-Addax_%28Addax_nasomaculatus%29.jpg",
    "Chinese Pangolin": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Pangolin_Borneo.jpg/320px-Pangolin_Borneo.jpg",
    "Mountain Gorilla": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Mountain_Gorilla_Silverback_2018.jpg/320px-Mountain_Gorilla_Silverback_2018.jpg",
    "Siamese Crocodile": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Siamese_Crocodile_Edit.jpg/320px-Siamese_Crocodile_Edit.jpg",
    "Dodo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Dodo_1.jpg/320px-Dodo_1.jpg",
    "Tasmanian Tiger": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Tasmanian_tiger_in_Hobart_Zoo.jpg/320px-Tasmanian_tiger_in_Hobart_Zoo.jpg",
    "Passenger Pigeon": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Ectopistes_migratoriusMCN2P28CA.jpg/320px-Ectopistes_migratoriusMCN2P28CA.jpg",
    "Woolly Mammoth": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Woolly_mammoth.jpg/320px-Woolly_mammoth.jpg",
    "Steller's Sea Cow": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Hydrodamalis_gigas_skeletal_reconstruction.jpg/320px-Hydrodamalis_gigas_skeletal_reconstruction.jpg",
    "Great Auk": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Keulemans-GreatAuk.jpg/240px-Keulemans-GreatAuk.jpg",
    "Caribbean Monk Seal": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Caribbean_Monk_Seal.jpg/320px-Caribbean_Monk_Seal.jpg",
    "Quagga": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Quagga_photo.jpg/320px-Quagga_photo.jpg",
    "West African Black Rhino": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Black_rhino.jpg/320px-Black_rhino.jpg",
    "Baiji River Dolphin": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Lipotes_vexillifer.png/320px-Lipotes_vexillifer.png",
    "Golden Toad": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Bufo_periglenes2.jpg/320px-Bufo_periglenes2.jpg",
    "Pyrenean Ibex": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Capra_pyrenaica_pyrenaica_%28Macho_de_bucardo_cazado_en_1898%29_-_Museo_de_Ciencias_Naturales_de_la_Universidad_de_Zaragoza.jpg/240px-Capra_pyrenaica_pyrenaica_%28Macho_de_bucardo_cazado_en_1898%29_-_Museo_de_Ciencias_Naturales_de_la_Universidad_de_Zaragoza.jpg",
    "Japanese Sea Lion": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Japanese_sea_lion_at_Ueno_Zoo_1950s.jpg/320px-Japanese_sea_lion_at_Ueno_Zoo_1950s.jpg",
    "Toolache Wallaby": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Toolache_Wallaby.jpg/240px-Toolache_Wallaby.jpg",
    "Atlas Bear": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Ursus_arctos_crowtheri.jpg/320px-Ursus_arctos_crowtheri.jpg",
    "Caspian Tiger": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Caspischetiger.jpg/320px-Caspischetiger.jpg",
    "Carolina Parakeet": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Carolina_Parakeet.jpg/320px-Carolina_Parakeet.jpg",
    "Schomburgk's Deer": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Rucervus_schomburgki.jpg/320px-Rucervus_schomburgki.jpg",
    "Falkland Islands Wolf": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Falkland_Islands_wolf.jpg/320px-Falkland_Islands_wolf.jpg",
    "Moa": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Giant_Moa_skeleton.jpg/240px-Giant_Moa_skeleton.jpg",
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
        response = requests.get(url, timeout=10)
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

