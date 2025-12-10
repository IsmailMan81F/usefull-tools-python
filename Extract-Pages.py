# pdf_page_extractor.pyw
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os
import sys

# --- Hide console on Windows ---
if os.name == "nt":
    try:
        import ctypes
        wh = ctypes.windll.kernel32.GetConsoleWindow()
        if wh:
            ctypes.windll.user32.ShowWindow(wh, 0)
    except Exception:
        pass


class PDFPageExtractor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Page Extractor")
        self.geometry("500x460")
        self.configure(bg="#f7f9fb")
        self.resizable(False, False)

        self.pdf_path = None

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="PDF Page Extractor", font=("Segoe UI", 18, "bold"), bg="#f7f9fb", fg="#222")
        title.pack(pady=(20, 5))

        info = tk.Label(self, text="Select a PDF and type the pages you want to extract (e.g., 1 2 5 7)", bg="#f7f9fb", fg="#555")
        info.pack()

        # File display
        self.file_label = tk.Label(self, text="No file selected", bg="#f7f9fb", fg="#888", wraplength=460)
        self.file_label.pack(pady=10)

        browse_btn = self._create_button("Browse PDF", self.browse_file, "#4a90e2")
        browse_btn.pack(pady=5)

        # Entry for pages
        pages_label = tk.Label(self, text="Enter pages to extract (space-separated):", bg="#f7f9fb", fg="#333")
        pages_label.pack(pady=(20, 5))

        self.pages_entry = tk.Entry(self, width=40, font=("Segoe UI", 12), justify="center")
        self.pages_entry.pack(pady=5)

        # 🔹 Entry for output file name
        name_label = tk.Label(self, text="Enter new file name (without .pdf):", bg="#f7f9fb", fg="#333")
        name_label.pack(pady=(15, 5))

        self.name_entry = tk.Entry(self, width=40, font=("Segoe UI", 12), justify="center")
        self.name_entry.insert(0, "extracted_pages")  # default
        self.name_entry.pack(pady=5)

        # Extract button
        extract_btn = self._create_button("Extract Pages", self.extract_pages, "#28a745", width=20, height=2)
        extract_btn.pack(pady=20)

        # Status
        self.status_label = tk.Label(self, text="Ready", bg="#f7f9fb", fg="#555")
        self.status_label.pack(pady=5)

    def _create_button(self, text, command, color, width=16, height=1):
        btn = tk.Button(
            self, text=text, command=command, width=width, height=height,
            bg=color, fg="white", activebackground=color, activeforeground="white",
            bd=0, relief="flat", font=("Segoe UI", 10, "bold")
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self._brighten(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def _brighten(self, hex_color, factor=1.2):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        bright = tuple(min(int(c * factor), 255) for c in rgb)
        return f"#{bright[0]:02x}{bright[1]:02x}{bright[2]:02x}"

    def browse_file(self):
        path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path = path
            self.file_label.config(text=f"Selected: {os.path.basename(path)}", fg="#222")

    def extract_pages(self):
        if not self.pdf_path:
            messagebox.showwarning("No file", "Please select a PDF file first.")
            return

        pages_text = self.pages_entry.get().strip()
        if not pages_text:
            messagebox.showwarning("No pages", "Please enter the pages to extract (e.g. 1 2 5 7).")
            return

        file_name = self.name_entry.get().strip()
        if not file_name:
            messagebox.showwarning("No name", "Please enter a name for the new file.")
            return

        try:
            pages = [int(x) - 1 for x in pages_text.split() if x.isdigit()]  # convert to 0-based
            if not pages:
                messagebox.showwarning("Invalid input", "Please enter valid page numbers separated by spaces.")
                return

            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()

            for p in pages:
                if 0 <= p < len(reader.pages):
                    writer.add_page(reader.pages[p])
                else:
                    messagebox.showwarning("Invalid page", f"Page {p + 1} is out of range.")
                    return

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop, f"{file_name}.pdf")

            with open(output_path, "wb") as out:
                writer.write(out)

            self.status_label.config(text="File saved successfully ✅")
            messagebox.showinfo("Success", f"Extracted pages saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    app = PDFPageExtractor()
    app.mainloop()
