import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Global variable untuk menyimpan citra grayscale
image_gray_global = None

# Fungsi untuk memilih gambar dan mengonversi ke grayscale
def open_image():
    global image_gray_global

    file_path = filedialog.askopenfilename()
    if file_path:
        # Buka gambar RGB
        image_rgb = Image.open(file_path)
        image_gray = image_rgb.convert("L")  # Konversi ke grayscale
        image_gray_global = image_gray       # Simpan untuk keperluan penyimpanan

        # Resize tampilan agar lebih besar
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
        label_gray_text.config(text="Gambar Grayscale")

# Fungsi untuk menyimpan gambar grayscale
def save_grayscale():
    global image_gray_global
    if image_gray_global:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            image_gray_global.save(file_path)

# GUI utama
root = tk.Tk()
root.title("Konversi RGB ke Grayscale")
root.geometry("600x600")

btn_open = tk.Button(root, text="📂 Pilih Gambar", command=open_image)
btn_open.pack(pady=10)

btn_save = tk.Button(root, text="💾 Simpan Grayscale", command=save_grayscale)
btn_save.pack(pady=5)

# Label untuk gambar RGB
label_rgb_text = tk.Label(root, text="")
label_rgb_text.pack()
label_rgb = tk.Label(root)
label_rgb.pack()

# Label untuk gambar Grayscale
label_gray_text = tk.Label(root, text="")
label_gray_text.pack()
label_gray = tk.Label(root)
label_gray.pack()

root.mainloop()
