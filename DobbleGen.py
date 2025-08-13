import os
from tkinter import Tk, filedialog, Canvas, Scrollbar, Frame, Button, NW, BOTH, LEFT, RIGHT, Y
from PIL import Image, ImageTk
import svgwrite
import itertools
import math
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A3
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import io
from cairosvg import svg2png

# --- GUI per selezione immagini ---
def select_images():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Seleziona immagini PNG o JPG",
        filetypes=[("Immagini PNG e JPG", "*.png *.jpg *.jpeg")]
    )
    valid_images = []
    for path in file_paths:
        try:
            img = Image.open(path)
            if img.width < 50 or img.height < 50:
                print(f"Immagine troppo piccola: {path}")
                continue
            valid_images.append(path)
        except:
            print(f"Formato non valido: {path}")
    return valid_images

# --- Funzioni core Dobble ---
def polygon_vertices(sides, radius, center):
    cx, cy = center
    vertices = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def generate_svg_card(image_paths, output_path, card_size=400):
    n = len(image_paths)
    sides = n - 1
    dwg = svgwrite.Drawing(output_path, size=(card_size, card_size))
    center = (card_size/2, card_size/2)
    radius = card_size/2.5
    vertices = polygon_vertices(sides, radius, center)
    for i, vertex in enumerate(vertices):
        x, y = vertex
        img = image_paths[i]
        dwg.add(dwg.image(img, insert=(x-30, y-30), size=(60,60)))
    dwg.add(dwg.image(image_paths[-1], insert=(center[0]-40, center[1]-40), size=(80,80)))
    dwg.save()

def generate_deck_svg(images, output_dir="output_svg", card_size=400):
    os.makedirs(output_dir, exist_ok=True)
    idx = 1
    for combo in itertools.permutations(images):
        output_file = os.path.join(output_dir, f"carta_{idx}.svg")
        generate_svg_card(combo, output_file, card_size)
        idx += 1
    return sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".svg")])

# --- PDF ottimizzato ---
def optimal_layout(total_cards, page_size=A3):
    width, height = page_size
    best_rows, best_cols = 1, total_cards
    min_waste = width * height
    for rows in range(1, total_cards+1):
        cols = math.ceil(total_cards / rows)
        card_w = width / cols
        card_h = height / rows
        waste = (card_w * card_h * total_cards) - (width * height)
        if waste >= 0 and waste < min_waste:
            min_waste = waste
            best_rows, best_cols = rows, cols
    return best_rows, best_cols

def generate_pdf_optimized(svg_files, pdf_path="mazzo_dobble.pdf", page_size=A3):
    total_cards = len(svg_files)
    rows, cols = optimal_layout(total_cards, page_size)
    width, height = page_size
    card_width = width / cols
    card_height = height / rows
    c = pdfcanvas.Canvas(pdf_path, pagesize=page_size)
    x_offset, y_offset = 0, height - card_height
    for idx, svg_file in enumerate(svg_files):
        drawing = svg2rlg(svg_file)
        scale_x = card_width / drawing.width
        scale_y = card_height / drawing.height
        scale = min(scale_x, scale_y)
        drawing.width *= scale
        drawing.height *= scale
        for e in drawing.contents:
            e.scale(scale, scale)
        renderPDF.draw(drawing, c, x_offset, y_offset)
        x_offset += card_width
        if (idx + 1) % cols == 0:
            x_offset = 0
            y_offset -= card_height
            if (idx + 1) % (rows * cols) == 0:
                c.showPage()
                x_offset, y_offset = 0, height - card_height
    c.save()
    print(f"PDF ottimizzato generato: {pdf_path}")

# --- Preview dinamica ---
def preview_cards(svg_files):
    root = Tk()
    root.title("Preview carte Dobble")

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)
    canvas_widget = Canvas(frame)
    canvas_widget.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    inner_frame = Frame(canvas_widget)
    canvas_widget.create_window((0,0), window=inner_frame, anchor=NW)
    images_tk = []

    total_cards = len(svg_files)
    if total_cards <= 20:
        thumb_size = 200
    elif total_cards <= 50:
        thumb_size = 150
    elif total_cards <= 100:
        thumb_size = 100
    else:
        thumb_size = 80

    cols = 5 if thumb_size >= 150 else 8

    for idx, svg_file in enumerate(svg_files):
        png_data = io.BytesIO()
        svg2png(url=svg_file, write_to=png_data)
        png_data.seek(0)
        pil_img = Image.open(png_data)
        pil_img.thumbnail((thumb_size, thumb_size))
        tk_img = ImageTk.PhotoImage(pil_img)
        images_tk.append(tk_img)

        label = Canvas(inner_frame, width=thumb_size, height=thumb_size)
        label.create_image(0,0, anchor=NW, image=tk_img)
        label.grid(row=idx//cols, column=idx%cols, padx=5, pady=5)

    inner_frame.update_idletasks()
    canvas_widget.config(scrollregion=canvas_widget.bbox("all"))

    Button(root, text="Genera PDF Ottimizzato", command=lambda: generate_pdf_optimized(svg_files)).pack(pady=10)
    root.mainloop()

# --- Esempio d'uso completo ---
if __name__ == "__main__":
    images = select_images()
    if images:
        svg_files = generate_deck_svg(images)
        preview_cards(svg_files)
