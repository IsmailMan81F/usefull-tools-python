import os
from tkinter import Tk, Label, Button, Entry, Listbox, END, filedialog, messagebox, Scrollbar, RIGHT, Y, BOTH, Frame
from PIL import Image
import pytesseract

# Set path to tesseract.exe (Windows users: adjust if installed elsewhere)
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Functions ---
def select_images():
    paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    if paths:
        for path in paths:
            listbox.insert(END, path)
        lbl_status.config(text=f"{listbox.size()} image(s) selected.", fg="green")

def remove_selected():
    selected = listbox.curselection()
    for i in reversed(selected):
        listbox.delete(i)
    lbl_status.config(text=f"{listbox.size()} image(s) selected.", fg="gray" if listbox.size() == 0 else "green")

def clear_all():
    listbox.delete(0, END)
    lbl_status.config(text="No images selected.", fg="gray")

def convert_to_text():
    if listbox.size() == 0:
        messagebox.showerror("Error", "Please select images first.")
        return

    base_name = entry_name.get().strip()
    if not base_name:
        messagebox.showerror("Error", "Please enter a base name for the text files.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    images = list(listbox.get(0, END))

    for i, img_path in enumerate(images, start=1):
        try:
            img = Image.open(img_path)
            text = pytesseract.image_to_string(img, lang="eng")
            txt_name = f"{base_name}{i}.txt"
            txt_path = os.path.join(desktop_path, txt_name)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text from {os.path.basename(img_path)}:\n{e}")
            return

    messagebox.showinfo("Success", f"All text files saved to Desktop")
    clear_all()
    entry_name.delete(0, END)

# --- UI Setup ---
root = Tk()
root.title("Image to Text Converter")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#f4f6f8")

Label(root, text="Image to Text Converter", font=("Segoe UI", 16, "bold"), bg="#f4f6f8", fg="#333").pack(pady=20)
Label(root, text="Select multiple images to extract text from each", bg="#f4f6f8", fg="#555").pack(pady=5)

frame = Frame(root, bg="#f4f6f8")
frame.pack(pady=10, fill=BOTH, expand=False, padx=40)

scrollbar = Scrollbar(frame, orient="vertical")
listbox = Listbox(frame, selectmode="extended", width=60, height=9, yscrollcommand=scrollbar.set, bg="white", fg="#333", relief="solid", borderwidth=0)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(fill=BOTH, expand=True)

btn_frame = Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=5)

Button(btn_frame, text="Browse Images", command=select_images, bg="#3b82f6", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Remove Selected", command=remove_selected, bg="#ef4444", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Clear All", command=clear_all, bg="#6b7280", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)

lbl_status = Label(root, text="No images selected.", bg="#f4f6f8", fg="gray")
lbl_status.pack(pady=5)

Label(root, text="Enter base text name (e.g., text):", bg="#f4f6f8", fg="#333", font=("Segoe UI", 10)).pack(pady=(20, 5))
entry_name = Entry(root, width=30, font=("Segoe UI", 11), justify="center", relief="solid", borderwidth=1)
entry_name.pack(pady=5)

Button(root, text="Convert to Text Files", command=convert_to_text, bg="#22c55e", fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, relief="flat").pack(pady=20)

Label(root, text="Made with ❤️ by Ismail", bg="#f4f6f8", fg="#999", font=("Segoe UI", 9)).pack(side="bottom", pady=10)

root.mainloop()
