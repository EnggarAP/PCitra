import tkinter as tk
from tkinter import filedialog, Canvas
from PIL import Image

class IndexedImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Citra Terindeks")

        tk.Button(root, text="Pilih Gambar", command=self.load_image).pack()
        tk.Button(root, text="4 Warna", command=lambda: self.quantize_image(4)).pack()
        tk.Button(root, text="16 Warna", command=lambda: self.quantize_image(16)).pack()
        tk.Button(root, text="256 Warna", command=lambda: self.quantize_image(256)).pack()
        tk.Button(root, text="Simpan Gambar Terindeks", command=self.save_indexed_image).pack()

        self.canvas = Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.original_image = None
        self.indexed_image = None
        self.original_pixels = []
        self.indexed_pixels = []
        self.width = 0
        self.height = 0

    def load_image(self):
        path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.ppm")])
        if not path:
            return
        img = Image.open(path).convert("RGB")
        self.original_image = img
        self.width, self.height = img.size
        self.original_pixels = list(img.getdata())
        self.indexed_pixels = []
        self.show_comparison()

    def euclidean(self, a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2) ** 0.5

    def simple_random_sample(self, data, k):
        result = []
        used = set()
        count = 0
        i = 0
        while count < k and i < len(data):
            idx = (i * 11 + 17) % len(data)
            if idx not in used:
                used.add(idx)
                result.append(data[idx])
                count += 1
            i += 1
        return result

    def quantize_image(self, k):
        if not self.original_pixels:
            return

        centroids = self.simple_random_sample(self.original_pixels, k)
        for _ in range(5):
            clusters = [[] for _ in range(k)]
            for p in self.original_pixels:
                dists = [self.euclidean(p, c) for c in centroids]
                idx = dists.index(min(dists))
                clusters[idx].append(p)

            new_centroids = []
            for cluster in clusters:
                if cluster:
                    r = sum(p[0] for p in cluster) // len(cluster)
                    g = sum(p[1] for p in cluster) // len(cluster)
                    b = sum(p[2] for p in cluster) // len(cluster)
                    new_centroids.append((r, g, b))
                else:
                    new_centroids.append((0, 0, 0))
            centroids = new_centroids

        result = []
        for p in self.original_pixels:
            dists = [self.euclidean(p, c) for c in centroids]
            idx = dists.index(min(dists))
            result.append(centroids[idx])

        self.indexed_pixels = result
        self.indexed_image = Image.new("RGB", (self.width, self.height))
        self.indexed_image.putdata(self.indexed_pixels)
        self.show_comparison(title=f"{k} Warna")

    def show_comparison(self, title="Original"):
        self.canvas.delete("all")
        if not self.original_pixels:
            return

        scale = 1 if self.width > 200 else 2
        total_width = self.width * scale * 2
        self.canvas.config(width=total_width, height=self.height * scale)

        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x
                r, g, b = self.original_pixels[i]
                color = f'#{r:02x}{g:02x}{b:02x}'
                self.canvas.create_rectangle(
                    x*scale, y*scale, (x+1)*scale, (y+1)*scale,
                    fill=color, outline=color
                )

        if self.indexed_pixels:
            for y in range(self.height):
                for x in range(self.width):
                    i = y * self.width + x
                    r, g, b = self.indexed_pixels[i]
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    offset = self.width * scale
                    self.canvas.create_rectangle(
                        (x*scale + offset), y*scale,
                        (x+1)*scale + offset, (y+1)*scale,
                        fill=color, outline=color
                    )

        self.root.title(f"Citra Terindeks - {title}")

    def save_indexed_image(self):
        if not self.indexed_image:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")],
                                            title="Simpan Gambar Terindeks")
        if path:
            self.indexed_image.save(path)
            print(f"Gambar disimpan ke: {path}")

# Jalankan Aplikasi
root = tk.Tk()
app = IndexedImageApp(root)
root.mainloop()
