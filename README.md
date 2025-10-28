# Endangered & Extinct Animals GUI

A Python tkinter application displaying 40 animals (20 Critically Endangered + 20 Extinct) with scrollable interface.

## Features
- **40 animals** with scientific names
- **Scrollable interface** with mousewheel support
- **Color-coded status**: Red for Extinct, Orange for Critically Endangered
- **Animal initials** displayed as placeholders

## Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
source venv/bin/activate
python main.py
```

## Adding Real Animal Images

To display actual animal photos instead of initials:

1. Create an `animal_images/` directory in the project root
2. Add images named exactly as the animal (replace spaces with underscores):
   - `Javan_Rhino.jpg`
   - `Vaquita.jpg`
   - `Dodo.jpg`
   - etc.
3. Images will be automatically loaded and resized to 80x80 pixels

### Where to Get Images

- **Wikimedia Commons**: https://commons.wikimedia.org (free, CC-licensed)
- **iNaturalist**: https://www.inaturalist.org (community photos)
- **Unsplash**: https://unsplash.com (free high-quality photos)

**Note**: Ensure you have rights to use any images you add.

## Project Structure

```
endangered-animals-app/
├── main.py              # Main application
├── animal_data.py       # 40 animals with scientific names
├── image_generator.py   # Image/placeholder generator
├── image_downloader.py  # Image loader with caching
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── animal_images/      # Image cache (gitignored)
```

## Technologies Used

- **Python 3.14**
- **tkinter** - GUI framework
- **Pillow** - Image processing
- **requests** - HTTP library for potential image downloading

## Animals Included

### Critically Endangered (20)
Javan Rhino, Vaquita, Amur Leopard, Black Rhino, Bornean Orangutan, Cross River Gorilla, Hawksbill Turtle, Saola, South China Tiger, Sumatran Elephant, Sumatran Orangutan, Sumatran Rhino, Sunda Tiger, Yangtze Finless Porpoise, Philippine Eagle, Kakapo, Addax, Chinese Pangolin, Mountain Gorilla, Siamese Crocodile

### Extinct (20)
Dodo, Tasmanian Tiger, Passenger Pigeon, Woolly Mammoth, Steller's Sea Cow, Great Auk, Caribbean Monk Seal, Quagga, West African Black Rhino, Baiji River Dolphin, Golden Toad, Pyrenean Ibex, Japanese Sea Lion, Toolache Wallaby, Atlas Bear, Caspian Tiger, Carolina Parakeet, Schomburgk's Deer, Falkland Islands Wolf, Moa

