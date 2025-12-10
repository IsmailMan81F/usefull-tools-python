import os
from tkinter import Tk, Label, Button, Entry, Listbox, END, filedialog, messagebox, Scrollbar, RIGHT, Y, BOTH, Frame
from PIL import Image

# Select images
def select_images():
    paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    if paths:
        for path in paths:
            listbox.insert(END, path)
        lbl_status.config(text=f"{listbox.size()} image(s) selected.", fg="green")

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

# Convert images to PDFs
def convert_to_pdf():
    if listbox.size() == 0:
        messagebox.showerror("Error", "Please select images first.")
        return

    base_name = entry_name.get().strip()
    if not base_name:
        messagebox.showerror("Error", "Please enter a base name for the PDFs.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    images = list(listbox.get(0, END))

    for i, img_path in enumerate(images, start=1):
        try:
            img = Image.open(img_path).convert("RGB")
            pdf_name = f"{base_name}.pdf"
            pdf_path = os.path.join(desktop_path, pdf_name)
            img.save(pdf_path, "PDF", resolution=100.0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {os.path.basename(img_path)}: {e}")
            return

    messagebox.showinfo("Success", f"All PDFs saved to Desktop")
    clear_all()
    entry_name.delete(0, END)

# --- UI Setup ---
root = Tk()
root.title("Image to PDF Converter")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#f4f6f8")

Label(root, text="Image to PDF Converter", font=("Segoe UI", 16, "bold"), bg="#f4f6f8", fg="#333").pack(pady=20)
Label(root, text="Select multiple images to convert each into a PDF", bg="#f4f6f8", fg="#555").pack(pady=5)

# Listbox frame
frame = Frame(root, bg="#f4f6f8")
frame.pack(pady=10, fill=BOTH, expand=False, padx=40)

scrollbar = Scrollbar(frame, orient="vertical")
listbox = Listbox(frame, selectmode="extended", width=60, height=9, yscrollcommand=scrollbar.set, bg="white", fg="#333", relief="solid", borderwidth=0)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(fill=BOTH, expand=True)

# Buttons
btn_frame = Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=5)

Button(btn_frame, text="Browse Images", command=select_images, bg="#3b82f6", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Remove Selected", command=remove_selected, bg="#ef4444", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Clear All", command=clear_all, bg="#6b7280", fg="white", width=15, relief="flat", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)

lbl_status = Label(root, text="No images selected.", bg="#f4f6f8", fg="gray")
lbl_status.pack(pady=5)

# Base name input
Label(root, text="Enter base PDF name (e.g., pdf):", bg="#f4f6f8", fg="#333", font=("Segoe UI", 10)).pack(pady=(20, 5))
entry_name = Entry(root, width=30, font=("Segoe UI", 11), justify="center", relief="solid", borderwidth=1)
entry_name.pack(pady=5)

# Convert button
Button(root, text="Convert to PDFs", command=convert_to_pdf, bg="#22c55e", fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, relief="flat").pack(pady=20)

Label(root, text="Made with ❤️ by Ismail", bg="#f4f6f8", fg="#999", font=("Segoe UI", 9)).pack(side="bottom", pady=10)

root.mainloop()
