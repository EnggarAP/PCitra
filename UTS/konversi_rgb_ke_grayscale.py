import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

image_gray_global = None

def open_image():
    global image_gray_global

    file_path = filedialog.askopenfilename()
    if file_path:
        # Buka gambar RGB
        image_rgb = Image.open(file_path).convert("RGB")
        width, height = image_rgb.size

        # Buat citra kosong untuk grayscale
        image_gray = Image.new("L", (width, height))

        # Konversi manual RGB ke Grayscale per piksel
        for y in range(height):
            for x in range(width):
                r, g, b = image_rgb.getpixel((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # rumus luminance
                image_gray.putpixel((x, y), gray)

        image_gray_global = image_gray

        # Resize agar tampilan lebih besar
        image_rgb_resized = image_rgb.resize((300, 300))
        image_gray_resized = image_gray.resize((300, 300))

        # Konversi ke format Tkinter
        img_rgb_tk = ImageTk.PhotoImage(image_rgb_resized)
        img_gray_tk = ImageTk.PhotoImage(image_gray_resized)

        # Tampilkan gambar RGB
        label_rgb.config(image=img_rgb_tk)
        label_rgb.image = img_rgb_tk
        label_rgb_text.config(text="Gambar RGB")

        # Tampilkan gambar Grayscale
        label_gray.config(image=img_gray_tk)
        label_gray.image = img_gray_tk
        label_gray_text.config(text="Gambar Grayscale (Manual)")

def save_grayscale():
    global image_gray_global
    if image_gray_global:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            image_gray_global.save(file_path)

# GUI utama
root = tk.Tk()
root.title("Konversi Manual RGB ke Grayscale")
root.geometry("700x700")

btn_open = tk.Button(root, text="📂 Pilih Gambar", command=open_image)
btn_open.pack(pady=10)

btn_save = tk.Button(root, text="💾 Simpan Grayscale", command=save_grayscale)
btn_save.pack(pady=5)

label_rgb_text = tk.Label(root, text="")
label_rgb_text.pack()
label_rgb = tk.Label(root)
label_rgb.pack()

label_gray_text = tk.Label(root, text="")
label_gray_text.pack()
label_gray = tk.Label(root)
label_gray.pack()

root.mainloop()
