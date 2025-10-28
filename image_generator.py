import logging
import random
import tkinter as tk

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


def create_placeholder_image(parent: tk.Widget, width: int, height: int) -> tk.Canvas:
    color = random.choice(COLORS)
    canvas = tk.Canvas(parent, width=width, height=height, bg=color, highlightthickness=0)
    
    canvas.create_text(
        width // 2,
        height // 2,
        text="🦁",
        font=('Arial', 40),
        fill='white'
    )
    
    logger.debug(f"Created placeholder image with color {color}")
    return canvas

