import logging
import random
import tkinter as tk
from typing import Optional

from PIL import Image, ImageTk

from image_downloader import download_animal_image, resize_image_for_display

logger = logging.getLogger(__name__)


COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788',
    '#E63946', '#A8DADC', '#457B9D', '#F1FAEE', '#1D3557',
    '#D4A5A5', '#9381FF', '#FFD6A5', '#CAFFBF', '#FDFFB6',
    '#FFD6FF', '#E7C6FF', '#C8B6FF', '#B8C0FF', '#BBD0FF',
    '#AED9E0', '#FAF3DD', '#C8D5B9', '#8FC0A9', '#68B0AB',
    '#4A7C7E', '#D4939D', '#FFAFCC', '#BDE0FE', '#A2D2FF',
    '#CDB4DB', '#FFC8DD', '#FFAFCC', '#BDE0FE', '#A2D2FF'
]


def create_animal_image(parent: tk.Widget, animal_name: str, width: int, height: int) -> tk.Label:
    img = download_animal_image(animal_name)
    
    if img:
        img = resize_image_for_display(img, width, height)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(parent, image=photo, width=width, height=height)
        label.image = photo
        logger.debug(f"Created real image for {animal_name}")
        return label
    else:
        return create_placeholder_image(parent, width, height)


def create_placeholder_image(parent: tk.Widget, width: int, height: int) -> tk.Canvas:
    color = random.choice(COLORS)
    canvas = tk.Canvas(
        parent, 
        width=width, 
        height=height, 
        bg=color, 
        highlightthickness=2, 
        highlightbackground='#999999'
    )
    
    center_x = width // 2
    center_y = height // 2
    
    canvas.create_oval(
        10, 10, width - 10, height - 10,
        fill='white', 
        outline='#666666',
        width=2
    )
    
    canvas.create_oval(
        center_x - 8, center_y - 15, center_x + 8, center_y - 2,
        fill='#333333',
        outline=''
    )
    
    canvas.create_oval(
        center_x - 5, center_y - 12, center_x - 2, center_y - 8,
        fill='white',
        outline=''
    )
    canvas.create_oval(
        center_x + 2, center_y - 12, center_x + 5, center_y - 8,
        fill='white',
        outline=''
    )
    
    canvas.create_arc(
        center_x - 8, center_y - 5, center_x + 8, center_y + 10,
        start=180, extent=180,
        fill='#333333',
        outline=''
    )
    
    canvas.create_text(
        center_x, 
        height - 15,
        text="ANIMAL",
        font=('Arial', 8, 'bold'),
        fill='#666666'
    )
    
    logger.debug(f"Created placeholder image with color {color}")
    return canvas

