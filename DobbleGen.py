import os
import math
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, Frame, BOTH, RIGHT, Y
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ====== GENERAZIONE DOBBLE ======
def generate_dobble_deck(n):
    symbols = list(range(n**2 + n + 1))
    deck = []
    for i in range(n+1):
        deck.append([symbols[0]] + [symbols[(n * i + j + 1)] for j in range(n)])
    for a in range(1, n+1):
        for b in range(1, n+1):
            deck.append([symbols[a]] + [
                symbols[(n+1) + n*(j-1) + ((a-1)*(j-1) + (b-1)) % n] for j in range(1, n+1)
            ])
    return deck

# ====== DISEGNO CARTA ======
def draw_card(symbol_images, diameter_px=300):
    card = Image.new("RGBA", (diameter_px, diameter_px), (255, 255, 255, 0))
    center = diameter_px // 2
    radius = diameter_px // 2 - 40

    central_img = symbol_images[0].resize((60, 60), Image.LANCZOS)
    card.paste(central_img, (center-30, center-30), central_img)

    angle_step = 2 * math.pi / (len(symbol_images)-1)
    for idx, img in enumerate(symbol_images[1:], start=1):
        img_resized = img.resize((50, 50), Image.LANCZOS)
        angle = angle_step * (idx-1)
        x = int(center + radius * math.cos(angle) - 25)
        y = int(center + radius * math.sin(angle) - 25)
        card.paste(img_resized, (x, y), img_resized)

    return card

# ====== PREVIEW ======
def preview_cards(deck, images, on_confirm):
    root = tk.Tk()
    root.title("Preview Carte Dobble")

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas_tk = tk.Canvas(frame, yscrollcommand=scrollbar.set)
    canvas_tk.pack(fill=BOTH, expand=True)
    scrollbar.config(command=canvas_tk.yview)

    y_offset = 10
    for idx, card in enumerate(deck):
        card_img = draw_card([images[s] for s in card])
        tk_img = ImageTk.PhotoImage(card_img)
        canvas_tk.create_image(150, y_offset, anchor="n", image=tk_img)
        canvas_tk.image = tk_img  # prevenzione GC
        y_offset += card_img.height + 20

    def confirm():
        root.destroy()
        on_confirm()

    btn = tk.Button(root, text="Genera PDF", command=confirm)
    btn.pack(pady=5)

    root.mainloop()

# ====== PDF EXPORT ======
def export_pdf(deck, images, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4
    x, y = 50, page_height - 150

    for idx, card in enumerate(deck):
        card_img = draw_card([images[s] for s in card], diameter_px=250)
        tmp_path = os.path.join(tempfile.gettempdir(), f"_tmp_{idx}.png")
        card_img.save(tmp_path)
        c.drawImage(tmp_path, x, y, width=80*2.8, height=80*2.8)

        x += 250
        if x > page_width - 200:
            x = 50
            y -= 300
            if y < 100:
                c.showPage()
                x, y = 50, page_height - 150
        os.remove(tmp_path)
    c.save()

# ====== MAIN ======
if __name__ == "__main__":
    tk.Tk().withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Seleziona immagini",
        filetypes=[("Immagini PNG/JPG", "*.png;*.jpg;*.jpeg")]
    )

    if not file_paths:
        messagebox.showerror("Errore", "Nessuna immagine selezionata.")
        exit()

    # Carica e valida immagini
    images = []
    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext not in [".png", ".jpg", ".jpeg"]:
            messagebox.showerror("Errore", f"Formato non supportato: {path}")
            exit()
        img = Image.open(path).convert("RGBA")
        if img.width < 200 or img.height < 200:
            messagebox.showerror("Errore", f"Immagine troppo piccola (<200px): {path}")
            exit()
        images.append(img)

    num_symbols = len(images)
    n = int((math.sqrt(4*num_symbols - 3) - 1) // 2)
    required = n**2 + n + 1
    if num_symbols < required:
        messagebox.showerror("Errore", f"Servono almeno {required} immagini per n={n}")
        exit()

    deck = generate_dobble_deck(n)

    def on_confirm():
        pdf_name = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF file", "*.pdf")],
            title="Salva PDF come"
        )
        if pdf_name:
            export_pdf(deck, images, pdf_name)
            messagebox.showinfo("Fatto", f"PDF generato: {pdf_name}")

    preview_cards(deck, images, on_confirm)
