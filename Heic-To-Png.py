import os
from tkinter import (
    Tk, Label, Button, Entry, Listbox, END,
    filedialog, messagebox, Scrollbar,
    RIGHT, Y, BOTH, Frame
)
from PIL import Image
import pillow_heif

# Register HEIC support
pillow_heif.register_heif_opener()

# Select HEIC images
def select_images():
    paths = filedialog.askopenfilenames(
        title="Select HEIC images",
        filetypes=[("HEIC files", "*.heic")]
    )
    if paths:
        for path in paths:
            listbox.insert(END, path)
        lbl_status.config(
            text=f"{listbox.size()} image(s) selected.",
            fg="green"
        )

# Remove selected images
def remove_selected():
    selected = listbox.curselection()
    for i in reversed(selected):
        listbox.delete(i)
    lbl_status.config(text=f"{listbox.size()} image(s) selected.")

# Clear all images
def clear_all():
    listbox.delete(0, END)
    lbl_status.config(text="No images selected.", fg="gray")

# Convert HEIC to PNG
def convert_to_png():
    if listbox.size() == 0:
        messagebox.showerror("Error", "Please select HEIC images first.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    images = list(listbox.get(0, END))

    for img_path in images:
        try:
            img = Image.open(img_path).convert("RGB")
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            png_path = os.path.join(desktop_path, base_name + ".png")
            img.save(png_path, "PNG")
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to convert {os.path.basename(img_path)}:\n{e}"
            )
            return

    messagebox.showinfo("Success", "All PNG files saved to Desktop")
    clear_all()

# --- UI Setup ---
root = Tk()
root.title("HEIC to PNG Converter")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#f4f6f8")

Label(
    root,
    text="HEIC to PNG Converter",
    font=("Segoe UI", 16, "bold"),
    bg="#f4f6f8",
    fg="#333"
).pack(pady=20)

Label(
    root,
    text="Select HEIC images and convert them to PNG",
    bg="#f4f6f8",
    fg="#555"
).pack(pady=5)

# Listbox frame
frame = Frame(root, bg="#f4f6f8")
frame.pack(pady=10, fill=BOTH, expand=False, padx=40)

scrollbar = Scrollbar(frame, orient="vertical")
listbox = Listbox(
    frame,
    selectmode="extended",
    width=60,
    height=9,
    yscrollcommand=scrollbar.set,
    bg="white",
    fg="#333",
    relief="solid",
    borderwidth=0
)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(fill=BOTH, expand=True)

# Buttons
btn_frame = Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=5)

Button(
    btn_frame,
    text="Browse HEIC Images",
    command=select_images,
    bg="#3b82f6",
    fg="white",
    width=18,
    relief="flat",
    font=("Segoe UI", 10, "bold")
).grid(row=0, column=0, padx=5)

Button(
    btn_frame,
    text="Remove Selected",
    command=remove_selected,
    bg="#ef4444",
    fg="white",
    width=15,
    relief="flat",
    font=("Segoe UI", 10, "bold")
).grid(row=0, column=1, padx=5)

Button(
    btn_frame,
    text="Clear All",
    command=clear_all,
    bg="#6b7280",
    fg="white",
    width=15,
    relief="flat",
    font=("Segoe UI", 10, "bold")
).grid(row=0, column=2, padx=5)

lbl_status = Label(
    root,
    text="No images selected.",
    bg="#f4f6f8",
    fg="gray"
)
lbl_status.pack(pady=5)

# Convert button
Button(
    root,
    text="Convert to PNG",
    command=convert_to_png,
    bg="#22c55e",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=25,
    height=2,
    relief="flat"
).pack(pady=25)

Label(
    root,
    text="Made with ❤️ by Ismail",
    bg="#f4f6f8",
    fg="#999",
    font=("Segoe UI", 9)
).pack(side="bottom", pady=10)

root.mainloop()
