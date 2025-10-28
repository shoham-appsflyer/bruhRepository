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

The app currently displays animal initials (e.g., "JR" for Javan Rhino) as placeholders. To show actual photos:

### Option 1: Automatic Download (Recommended)

Run the helper script to download images from Unsplash:

```bash
source venv/bin/activate
python download_images_manually.py
```

This will automatically download images for all 40 animals into the `animal_images/` directory.

### Option 2: Manual Download

1. Create an `animal_images/` directory in the project root
2. Download images from free sources:
   - **Unsplash**: https://unsplash.com (free high-quality photos)
   - **Pixabay**: https://pixabay.com (free stock photos)
   - **Wikimedia Commons**: https://commons.wikimedia.org (free, CC-licensed)
   - **Public Domain Review**: https://publicdomainreview.org/collection/extinct-animals
3. Save images with exact animal names (replace spaces with underscores):
   - `Javan_Rhino.jpg`
   - `Vaquita.jpg`
   - `Dodo.jpg`
   - etc.
4. Images will be automatically loaded and resized to 80x80 pixels

**Note**: Automated downloading may fail due to SSL issues or rate limiting. If the helper script doesn't work, manually download images from the sources above.

### Troubleshooting Image Downloads

If images aren't showing:
1. Check that files are in `animal_images/` directory
2. Verify filenames match exactly (e.g., `Javan_Rhino.jpg` not `javan-rhino.jpg`)
3. Ensure images are valid JPEG format
4. Restart the application after adding images

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

