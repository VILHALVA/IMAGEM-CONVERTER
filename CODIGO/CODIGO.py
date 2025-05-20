import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import io
from rembg import remove
import os

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("IMAGEM CONVERTER")
app.geometry("600x600")

image_path = ""

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="SELECIONE UMA IMAGEM", filetypes=[("Imagens", "*.*")])
    if image_path:
        image_label.configure(text="CAMINHO: " + image_path)
        image_label.pack()
        update_save_button_state()

def update_save_button_state():
    if format_var.get() == "PADRÃO" and remove_bg_var.get() == "NÃO":
        save_button.configure(state="disabled")
    else:
        save_button.configure(state="normal")

def remove_background_and_save():
    if image_path:
        with open(image_path, "rb") as f:
            image_data = f.read()

        try:
            if remove_bg_var.get() == "SIM":
                output = remove(image_data)
                img = Image.open(io.BytesIO(output))
            else:
                img = Image.open(image_path)

            format_mapping = {
                "PADRÃO": os.path.splitext(image_path)[1][1:].upper(),
                "ICO": "ICO",
                "PNG": "PNG",
                "JPG": "JPEG",
                "JPEG": "JPEG"
            }

            selected_format = format_var.get()
            if selected_format in format_mapping:
                if selected_format in ["JPG", "JPEG"] and img.mode in ["RGBA", "LA"]:
                    img = img.convert("RGB")

                file_extension = format_mapping[selected_format].lower()
                output_image_path = os.path.splitext(image_path)[0] + f"_CONVERTIDO.{file_extension}"
                img.save(output_image_path, format=format_mapping[selected_format])
                messagebox.showinfo("SUCESSO!", f"A imagem foi salva como {selected_format} com sucesso!")
            else:
                messagebox.showerror("ERRO", "Formato de imagem inválido.")
        except Exception as e:
            messagebox.showerror("ERRO", str(e))

        update_save_button_state()

select_button = ctk.CTkButton(app, text="SELECIONAR", command=select_image)
select_button.pack(pady=10)

image_label = ctk.CTkLabel(app, text="CAMINHO: ")
image_label.pack()

ctk.CTkLabel(app, text="CONVERTER PARA:").pack(pady=5)

format_var = ctk.StringVar(value="PADRÃO")

format_frame = ctk.CTkFrame(app)
format_frame.pack(pady=5)

options = ["PADRÃO", "ICO", "PNG", "JPG", "JPEG"]
for option in options:
    ctk.CTkRadioButton(format_frame, text=option, variable=format_var, value=option, command=update_save_button_state).pack(side="left", padx=5)

ctk.CTkLabel(app, text="REMOVER FUNDO:").pack(pady=5)

remove_bg_var = ctk.StringVar(value="NÃO")

remove_bg_frame = ctk.CTkFrame(app)
remove_bg_frame.pack(pady=5)

ctk.CTkRadioButton(remove_bg_frame, text="SIM", variable=remove_bg_var, value="SIM", command=update_save_button_state).pack(side="left", padx=10)
ctk.CTkRadioButton(remove_bg_frame, text="NÃO", variable=remove_bg_var, value="NÃO", command=update_save_button_state).pack(side="left", padx=10)

save_button = ctk.CTkButton(app, text="SALVAR", command=remove_background_and_save, state="disabled")
save_button.pack(pady=10)

footer_label = ctk.CTkLabel(app, text="APP CRIADO PELO VILHALVA\nGITHUB: @VILHALVA", fg_color="gray", text_color="white", height=30)
footer_label.pack(side="bottom", fill="x")

app.mainloop()
