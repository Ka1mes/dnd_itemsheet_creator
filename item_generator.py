import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap

class ItemCardGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Gegenstandszettel Generator")
        self.root.geometry("680x850") # Höhe für das neue AC-Feld angepasst
        self.root.configure(padx=20, pady=20)

        self.image_path = None

        self.create_ui()

    def create_ui(self):
        # 1. Titel (Oben)
        tk.Label(self.root, text="Gegenstandsname:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(self.root, font=("Arial", 14), width=42)
        self.entry_name.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="we")
        self.entry_name.insert(0, "Zweihandaxt der Alten Ahnen")

        # 2. Mittlerer Bereich (Bild links, Stats rechts)
        mid_frame = tk.Frame(self.root)
        mid_frame.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 15))

        # 2a. Bild-Auswahl (Links)
        img_frame = tk.Frame(mid_frame, bd=2, relief="groove", width=160, height=240)
        img_frame.grid(row=0, column=0, padx=(0, 20), sticky="n")
        img_frame.pack_propagate(False) 
        
        self.lbl_image_preview = tk.Label(img_frame, text="Kein Bild\nausgewählt")
        self.lbl_image_preview.pack(expand=True)
        
        tk.Button(mid_frame, text="Bild laden...", command=self.load_image).grid(row=1, column=0, pady=5, sticky="n")

        # 2b. Rechter Bereich für Typ und Stats
        right_frame = tk.Frame(mid_frame)
        right_frame.grid(row=0, column=1, rowspan=2, sticky="nw")

        # Typ
        tk.Label(right_frame, text="Typ:").grid(row=0, column=0, sticky="nw", pady=(0, 10))
        self.entry_type = tk.Entry(right_frame, font=("Arial", 12), width=18)
        self.entry_type.grid(row=0, column=1, columnspan=2, sticky="nw", pady=(0, 10))
        self.entry_type.insert(0, "GREATAXE +1")

        # Variablen für die Checkboxen
        self.show_gp = tk.BooleanVar(value=True)
        self.show_range = tk.BooleanVar(value=False)
        self.show_hit = tk.BooleanVar(value=True)
        self.show_ac = tk.BooleanVar(value=False) # AC standardmäßig aus (da es primär eine Waffe ist)
        self.show_atm = tk.BooleanVar(value=True)
        self.show_dmg = tk.BooleanVar(value=True)

        tk.Label(right_frame, text="Angezeigte Werte:", font=("Arial", 9, "italic")).grid(row=1, column=0, columnspan=3, sticky="w", pady=(5,5))

        # GP
        tk.Checkbutton(right_frame, text="GP", variable=self.show_gp).grid(row=2, column=0, sticky="w")
        self.entry_gp = tk.Entry(right_frame, font=("Arial", 10), width=12)
        self.entry_gp.grid(row=2, column=1, sticky="w")
        self.entry_gp.insert(0, "50")

        # Range
        tk.Checkbutton(right_frame, text="Range", variable=self.show_range).grid(row=3, column=0, sticky="w")
        self.entry_range = tk.Entry(right_frame, font=("Arial", 10), width=12)
        self.entry_range.grid(row=3, column=1, sticky="w")
        self.entry_range.insert(0, "Melee")

        # Hit
        tk.Checkbutton(right_frame, text="Hit", variable=self.show_hit).grid(row=4, column=0, sticky="w")
        self.entry_hit = tk.Entry(right_frame, font=("Arial", 10), width=12)
        self.entry_hit.grid(row=4, column=1, sticky="w")
        self.entry_hit.insert(0, "+1")

        # AC (Armor Class) - NEU
        tk.Checkbutton(right_frame, text="AC", variable=self.show_ac).grid(row=5, column=0, sticky="w")
        self.entry_ac = tk.Entry(right_frame, font=("Arial", 10), width=12)
        self.entry_ac.grid(row=5, column=1, sticky="w")
        self.entry_ac.insert(0, "18")

        # ATM (Attunement)
        tk.Checkbutton(right_frame, text="ATM", variable=self.show_atm).grid(row=6, column=0, sticky="w")
        self.val_atm = tk.StringVar(value="JA")
        atm_dropdown = ttk.Combobox(right_frame, textvariable=self.val_atm, values=["JA", "NEIN"], width=9, state="readonly")
        atm_dropdown.grid(row=6, column=1, sticky="w")

        # Damage (Breites Feld)
        tk.Checkbutton(right_frame, text="Dmg", variable=self.show_dmg).grid(row=7, column=0, sticky="w", pady=(10,0))
        self.entry_dmg = tk.Entry(right_frame, font=("Arial", 10), width=18)
        self.entry_dmg.grid(row=7, column=1, sticky="w", pady=(10,0))
        self.entry_dmg.insert(0, "1d12+1 + 1W4")

        # Schadenstyp (Dropdown)
        tk.Label(right_frame, text="Dmg Typ:", font=("Arial", 9)).grid(row=8, column=0, sticky="w")
        self.val_dmg_type = tk.StringVar(value="Hiebschaden")
        dmg_classes = [
            "Hiebschaden", "Stichschaden", "Wuchtschaden", 
            "Feuerschaden", "Kälteschaden", "Blitzschaden", 
            "Säureschaden", "Giftschaden", "Nekrotisch", 
            "Gleißend", "Psychisch", "Energie", "Donner"
        ]
        ttk.Combobox(right_frame, textvariable=self.val_dmg_type, values=dmg_classes, width=15, state="readonly").grid(row=8, column=1, sticky="w", pady=(2,0))

        # 3. Textbereich (Unten)
        tk.Label(self.root, text="Beschreibung & Effekte:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w")
        self.text_desc = tk.Text(self.root, wrap="word", height=10, font=("Arial", 11))
        self.text_desc.grid(row=4, column=0, columnspan=2, pady=5, sticky="we")
        
        default_text = (
            "Eine massive, aus dunklem Gebirgsstahl geschmiedete Axt.\n"
            "Effekt: Wenn ein Dämon oder Kultist des Schwarzen Rings im Umkreis "
            "von 30 Fuß ist, wird das Metall heiß und die Waffe leuchtet. "
            "Angriffe fügen diesen Feinden 1W4 zusätzlichen Feuerschaden zu."
        )
        self.text_desc.insert(tk.END, default_text)

        # 4. Generieren Button
        tk.Button(self.root, text="Gegenstandszettel generieren", font=("Arial", 12, "bold"), 
                  bg="#4CAF50", fg="white", command=self.generate_card).grid(row=5, column=0, columnspan=2, pady=20, sticky="we")

    def load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.image_path = filepath
            img = Image.open(filepath)
            img.thumbnail((150, 230))
            self.photo = ImageTk.PhotoImage(img)
            self.lbl_image_preview.config(image=self.photo, text="")

    def generate_card(self):
        card_width = 400
        card_height = 650 # Karte etwas verlängert, damit alle Boxen Platz haben
        img = Image.new('RGB', (card_width, card_height), color='white')
        draw = ImageDraw.Draw(img)

        # Schriftarten
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 16)
            font_text = ImageFont.truetype("arial.ttf", 14)
            font_small = ImageFont.truetype("arial.ttf", 11)
            font_box_val = ImageFont.truetype("arialbd.ttf", 13)
        except IOError:
            font_title = font_text = font_small = font_box_val = ImageFont.load_default()

        # Rahmen & Trennlinie
        draw.rectangle([10, 10, card_width-10, card_height-10], outline="black", width=2)
        draw.line([10, 350, card_width-10, 350], fill="black", width=2) # Trennlinie nach unten gerückt

        # Titel
        title_bg = [20, 20, card_width-20, 50]
        draw.rectangle(title_bg, fill="#EEEEEE")
        draw.text((30, 25), self.entry_name.get().upper(), font=font_title, fill="black")

        # Item-Bild
        box_x, box_y = 25, 65
        box_w, box_h = 160, 240 
        draw.rectangle([box_x, box_y, box_x+box_w, box_y+box_h], outline="black", width=2) 

        if self.image_path:
            try:
                item_img = Image.open(self.image_path).convert("RGBA")
                item_img.thumbnail((box_w - 4, box_h - 4)) 
                offset_x = box_x + 2 + (box_w - 4 - item_img.width) // 2
                offset_y = box_y + 2 + (box_h - 4 - item_img.height) // 2
                img.paste(item_img, (offset_x, offset_y), item_img if item_img.mode == 'RGBA' else None)
            except Exception as e:
                print(f"Fehler beim Laden des Bildes: {e}")

        # Typ (Rechts oben)
        start_x = 200
        draw.text((start_x, 70), "TYPE:", font=font_small, fill="black")
        draw.rectangle([start_x, 85, card_width-20, 110], fill="#EEEEEE")
        draw.text((start_x + 5, 90), self.entry_type.get(), font=font_title, fill="black")

        # --- DYNAMISCHES STAT-RASTER ---
        # 1. Sammeln der kleinen Standard-Werte
        active_std_stats = []
        if self.show_gp.get(): active_std_stats.append((self.entry_gp.get(), "GP"))
        if self.show_range.get(): active_std_stats.append((self.entry_range.get(), "RNG"))
        if self.show_hit.get(): active_std_stats.append((self.entry_hit.get(), "HIT"))
        if self.show_ac.get(): active_std_stats.append((self.entry_ac.get(), "AC")) # NEU: AC hinzugefügt
        if self.show_atm.get(): active_std_stats.append((self.val_atm.get(), "ATM"))

        box_width = 80
        box_height = 40
        gap = 10
        start_y = 130
        
        # 2. Zeichnen der kleinen Boxen (2 Spalten)
        for i, (val, label) in enumerate(active_std_stats):
            col = i % 2
            row = i // 2
            
            gx = start_x + col * (box_width + gap)
            gy = start_y + row * (box_height + gap)
            
            draw.rectangle([gx, gy, gx + box_width, gy + box_height], outline="black", width=2)
            
            # Label links, Wert rechts daneben
            draw.text((gx + 5, gy + 14), label, font=font_small, fill="dimgray")
            draw.text((gx + 35, gy + 12), val, font=font_box_val, fill="black")

        # 3. Zeichnen der breiten DMG Box
        if self.show_dmg.get():
            num_std = len(active_std_stats)
            dmg_row = 0 if num_std == 0 else ((num_std - 1) // 2 + 1)
            
            gx = start_x
            gy = start_y + dmg_row * (box_height + gap)
            dmg_width = (box_width * 2) + gap 
            
            draw.rectangle([gx, gy, gx + dmg_width, gy + box_height], outline="black", width=2)
            
            # DMG Label links, Wert rechts daneben
            draw.text((gx + 5, gy + 14), "DMG", font=font_small, fill="dimgray")
            draw.text((gx + 40, gy + 12), self.entry_dmg.get(), font=font_box_val, fill="black")

            # Schadenstyp unter der DMG Box
            dmg_type_text = f"Schadenstyp: {self.val_dmg_type.get()}"
            draw.text((gx + 5, gy + box_height + 4), dmg_type_text, font=font_small, fill="dimgray")

        # Beschreibungstext
        raw_text = self.text_desc.get("1.0", tk.END)
        y_text = 365 # Startpunkt für Text nach unten gerückt
        
        paragraphs = raw_text.split('\n')
        for para in paragraphs:
            wrapped_lines = textwrap.wrap(para, width=45)
            for line in wrapped_lines:
                draw.text((20, y_text), line, font=font_text, fill="black")
                y_text += 20
            y_text += 10

        # Speichern
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            initialfile=f"{self.entry_name.get().replace(' ', '_')}.png",
            filetypes=[("PNG Image", "*.png")]
        )
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Erfolg!", f"Gegenstandszettel gespeichert unter:\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemCardGenerator(root)
    root.mainloop()