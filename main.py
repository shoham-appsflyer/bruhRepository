import logging
import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from animal_data import CRITICALLY_ENDANGERED_ANIMALS, EXTINCT_ANIMALS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnimalCard(ttk.Frame):
    def __init__(self, parent: ttk.Frame, animal_data: Dict[str, str]):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.animal_data = animal_data
        self._create_widgets()
        
    def _create_widgets(self) -> None:
        name_label = ttk.Label(
            self,
            text=self.animal_data['name'],
            font=('Arial', 14, 'bold')
        )
        name_label.pack(pady=(10, 5), padx=10, anchor=tk.W)
        
        scientific_label = ttk.Label(
            self,
            text=f"Scientific: {self.animal_data['scientific_name']}",
            font=('Arial', 9, 'italic'),
            foreground='gray'
        )
        scientific_label.pack(pady=(0, 5), padx=10, anchor=tk.W)
        
        status_label = ttk.Label(
            self,
            text=f"Status: {self.animal_data['status']}",
            font=('Arial', 10),
            foreground='red' if self.animal_data['status'] == 'Extinct' else 'orange'
        )
        status_label.pack(pady=(0, 10), padx=10, anchor=tk.W)


class ScrollableAnimalFrame(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.animals: List[Dict[str, str]] = []
        self._create_widgets()
        
    def _create_widgets(self) -> None:
        self.canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        logger.info("Scrollable animal frame created successfully")
        
    def add_animal(self, animal_data: Dict[str, str]) -> None:
        self.animals.append(animal_data)
        card = AnimalCard(self.scrollable_frame, animal_data)
        card.pack(fill=tk.X, padx=10, pady=5)
        logger.info(f"Added animal: {animal_data['name']}")
        
    def clear_animals(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.animals.clear()
        logger.info("Cleared all animals from display")


class EndangeredAnimalsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Endangered & Extinct Animals")
        self.root.geometry("600x700")
        self._create_widgets()
        self._load_animals()
        logger.info("Application initialized successfully")
        
    def _create_widgets(self) -> None:
        title_label = ttk.Label(
            self.root,
            text="Endangered & Extinct Animals",
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=20)
        
        self.animal_frame = ScrollableAnimalFrame(self.root)
        self.animal_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        logger.info("Main widgets created successfully")
        
    def _load_animals(self) -> None:
        all_animals = CRITICALLY_ENDANGERED_ANIMALS + EXTINCT_ANIMALS
        for animal in all_animals:
            self.animal_frame.add_animal(animal)
        logger.info(f"Loaded {len(all_animals)} animals into display")


def main() -> None:
    logger.info("Starting Endangered Animals Application")
    root = tk.Tk()
    app = EndangeredAnimalsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

