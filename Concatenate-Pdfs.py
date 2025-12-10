# pdf_merger.pyw
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os
import sys

# --- Hide terminal on Windows ---
if os.name == "nt":
    try:
        import ctypes
        wh = ctypes.windll.kernel32.GetConsoleWindow()
        if wh:
            ctypes.windll.user32.ShowWindow(wh, 0)  # Hide console window
    except Exception:
        pass


# --- Main App ---
class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("500x500")
        self.configure(bg="#f5f7fa")
        self.resizable(False, False)

        self.pdf_files = []

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="PDF Merger", font=("Segoe UI", 18, "bold"), bg="#f5f7fa", fg="#333")
        title.pack(pady=(15, 5))

        info = tk.Label(self, text="Select multiple PDF files to merge into one file", bg="#f5f7fa", fg="#666")
        info.pack()

        self.listbox = tk.Listbox(self, width=60, height=12, bd=0, highlightthickness=0, font=("Segoe UI", 10))
        self.listbox.pack(pady=15)

        # Buttons frame
        btn_frame = tk.Frame(self, bg="#f5f7fa")
        btn_frame.pack()

        self._add_button(btn_frame, "Browse PDFs", self.browse_pdfs, "#4a90e2").pack(side="left", padx=5)
        self._add_button(btn_frame, "Remove Selected", self.remove_selected, "#dc3545").pack(side="left", padx=5)
        self._add_button(btn_frame, "Clear All", self.clear_all, "#6c757d").pack(side="left", padx=5)

        # 🔹 Label + Entry for output file name
        name_label = tk.Label(self, text="Enter merged file name (without .pdf):", bg="#f5f7fa", fg="#333")
        name_label.pack(pady=(20, 5))

        self.name_entry = tk.Entry(self, width=40, font=("Segoe UI", 12), justify="center")
        self.name_entry.insert(0, "merged_output")  # Default name
        self.name_entry.pack(pady=5)

        # Merge button
        self._add_button(self, "Merge PDFs", self.merge_pdfs, "#28a745", width=20, height=2).pack(pady=20)

    def _add_button(self, parent, text, command, color, width=14, height=1):
        btn = tk.Button(
            parent, text=text, command=command, width=width, height=height,
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

    def browse_pdfs(self):
        files = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF files", "*.pdf")])
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.listbox.insert(tk.END, os.path.basename(file))

    def remove_selected(self):
        selected = list(self.listbox.curselection())
        for idx in reversed(selected):
            self.pdf_files.pop(idx)
            self.listbox.delete(idx)

    def clear_all(self):
        self.pdf_files.clear()
        self.listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("No files", "Please select PDF files first.")
            return

        file_name = self.name_entry.get().strip()
        if not file_name:
            messagebox.showwarning("No name", "Please enter a name for the merged file.")
            return

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = os.path.join(desktop, f"{file_name}.pdf")

        try:
            merger = PdfMerger()
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Success", f"Merged successfully!\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")


# --- Run app ---
if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
