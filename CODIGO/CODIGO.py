import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import io
from rembg import remove
import os
import ctypes  
from threading import Thread
import glob

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def is_oculto_ou_sistema(path):
    if os.name == "nt":  
        try:
            atributos = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if atributos == -1:
                return False
            FILE_ATTRIBUTE_HIDDEN = 0x2
            FILE_ATTRIBUTE_SYSTEM = 0x4
            return bool(atributos & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM))
        except Exception:
            return False
    else: 
        return os.path.basename(path).startswith(".")

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IMAGEM CONVERTER")
        
        self.selected_directory = ""

        self.format_var = ctk.StringVar(value="PADRÃO")
        self.remove_bg_var = ctk.StringVar(value="NÃO")

        self.scrollable_frame = ctk.CTkScrollableFrame(root, width=700, height=700)
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.scrollable_frame, text="CONVERSOR DE IMAGENS", font=("Arial", 20)).pack(pady=10)

        self.format_container = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        self.format_container.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.format_container, text="CONVERTER PARA:").pack(pady=(10, 0))
        self.format_frame = ctk.CTkFrame(self.format_container)
        self.format_frame.pack(pady=10)

        options = ["PADRÃO", "JPEG", "JPG", "PNG", "ICO"]
        for option in options:
            ctk.CTkRadioButton(self.format_frame, text=option, variable=self.format_var, value=option, command=self.update_convert_button_state).pack(side="left", padx=5)

        self.remove_bg_container = ctk.CTkFrame(self.scrollable_frame, border_width=2, corner_radius=10)
        self.remove_bg_container.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.remove_bg_container, text="REMOVER FUNDO?").pack(pady=(10, 0))
        self.remove_bg_frame = ctk.CTkFrame(self.remove_bg_container)
        self.remove_bg_frame.pack(pady=10)

        ctk.CTkRadioButton(self.remove_bg_frame, text="SIM", variable=self.remove_bg_var, value="SIM", command=self.update_convert_button_state).pack(side="left", padx=10)
        ctk.CTkRadioButton(self.remove_bg_frame, text="NÃO", variable=self.remove_bg_var, value="NÃO", command=self.update_convert_button_state).pack(side="left", padx=10)

        self.button_frame = ctk.CTkFrame(self.scrollable_frame)
        self.button_frame.pack(pady=10)

        self.select_button = ctk.CTkButton(self.button_frame, text="DIRETÓRIO", command=self.select_directory)
        self.select_button.pack(side="left", padx=5)

        self.convert_button = ctk.CTkButton(self.button_frame, text="CONVERTER", command=self.start_conversion, state="disabled")
        self.convert_button.pack(side="left", padx=5)

        self.status_textbox = ctk.CTkTextbox(self.scrollable_frame, width=500, height=180)
        self.status_textbox.pack(pady=10)
        self.status_textbox.configure(state='disabled')

        self.progress_frame = ctk.CTkFrame(self.scrollable_frame)
        self.progress_frame.pack(pady=(0, 5), fill="x", padx=10)

        self.progress_count_label = ctk.CTkLabel(self.progress_frame, text="0/0", width=50, anchor="w")
        self.progress_count_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", expand=True, fill="x", padx=10)

        self.progress_percent_label = ctk.CTkLabel(self.progress_frame, text="0%", width=50, anchor="e")
        self.progress_percent_label.pack(side="right")

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.clear_status()
            self.append_status(f"Diretório selecionado: {directory}\n")
            self.update_convert_button_state()

    def update_convert_button_state(self):
        if self.selected_directory and (self.format_var.get() != "PADRÃO" or self.remove_bg_var.get() == "SIM"):
            self.convert_button.configure(state="normal")
        else:
            self.convert_button.configure(state="disabled")

    def start_conversion(self):
        self.clear_status(keep_directory=True)
        self.progress_bar.set(0)
        self.progress_count_label.configure(text="0/0")
        self.progress_percent_label.configure(text="0%")
        Thread(target=self.convert_images).start()

    def convert_images(self):
        input_dir = self.selected_directory
        selected_format = self.format_var.get()
        remove_bg = self.remove_bg_var.get() == "SIM"

        output_format = selected_format if selected_format != "PADRÃO" else None

        output_dir = os.path.join(input_dir, f"CONVERTIDOS_{output_format or 'PADRAO'}")
        os.makedirs(output_dir, exist_ok=True)

        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.ico', '*.bmp', '*.webp']
        image_files = []

        for ext in image_extensions:
            files = glob.glob(os.path.join(input_dir, ext))
            for file in files:
                basename = os.path.basename(file).lower()
                if (
                    is_oculto_ou_sistema(file) or
                    'folder' in basename or
                    'cover' in basename or
                    'albumart' in basename or
                    'thumb' in basename or
                    'artwork' in basename
                ):
                    continue
                image_files.append(file)

        if not image_files:
            self.append_status("Nenhuma imagem encontrada no diretório!\n")
            return

        total = len(image_files)
        for idx, image_path in enumerate(image_files):
            try:
                with open(image_path, "rb") as f:
                    image_data = f.read()
                
                if remove_bg:
                    output = remove(image_data)
                    img = Image.open(io.BytesIO(output))
                else:
                    img = Image.open(image_path)

                fmt_map = {"ICO": "ICO", "PNG": "PNG", "JPG": "JPEG", "JPEG": "JPEG"}
                fmt = fmt_map.get(selected_format, os.path.splitext(image_path)[1][1:].upper())

                if fmt in ["JPEG"] and img.mode in ["RGBA", "LA"]:
                    img = img.convert("RGB")

                filename = os.path.splitext(os.path.basename(image_path))[0]
                ext_map = {"ICO": ".ico", "PNG": ".png", "JPEG": ".jpg"}
                new_ext = ext_map.get(fmt, os.path.splitext(image_path)[1])
                new_filename = filename + new_ext

                output_file = os.path.join(output_dir, new_filename)
                img.save(output_file, format=fmt)
                self.append_status(f"Convertido: {new_filename} \n")
                
                progress_value = (idx + 1) / total
                self.progress_bar.set(progress_value)
                self.progress_count_label.configure(text=f"{idx + 1}/{total}")
                self.progress_percent_label.configure(text=f"{int(progress_value * 100)}%")

            except Exception as e:
                self.append_status(f"Erro ao converter {image_path}: {str(e)}\n")

        self.append_status(f"\nConversão concluída!\nArquivos salvos em: {output_dir}\n")
        messagebox.showinfo("Finalizado", f"Todas as imagens foram convertidas com sucesso!")

    def clear_status(self, keep_directory=False):
        text = self.status_textbox.get("1.0", "end")
        self.status_textbox.configure(state='normal')
        self.status_textbox.delete("1.0", "end")
        if keep_directory:
            for line in text.splitlines():
                if line.startswith("Diretório selecionado"):
                    self.status_textbox.insert("end", line + "\n")
        self.status_textbox.configure(state='disabled')

    def append_status(self, message):
        self.status_textbox.configure(state='normal')
        self.status_textbox.insert("end", message)
        self.status_textbox.see("end")
        self.status_textbox.configure(state='disabled')

if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageConverterApp(root)
    root.state("zoomed")
    root.resizable(True, True)
    root.mainloop()
