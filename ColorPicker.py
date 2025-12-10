import tkinter as tk
import pyautogui
from pynput import keyboard

class ScreenColorPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Color Picker")
        self.root.geometry("250x250")
        self.root.resizable(False, False)

        # UI setup
        self.preview = tk.Label(self.root, text="", width=20, height=5, bg="white", relief="solid")
        self.preview.pack(pady=10)

        self.rgb_label = tk.Label(self.root, text="RGB: (0, 0, 0)", font=("Consolas", 10))
        self.rgb_label.pack()

        self.hex_label = tk.Label(self.root, text="#FFFFFF", font=("Consolas", 12, "bold"))
        self.hex_label.pack(pady=5)

        self.info = tk.Label(self.root, text="Press SPACE to pick a color\nPress ESC to quit",
                             fg="gray", font=("Arial", 9))
        self.info.pack(pady=5)

        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_key)
        self.listener.start()

        self.update_preview()
        self.root.mainloop()

    def on_key(self, key):
        try:
            if key == keyboard.Key.esc:
                self.root.quit()
            elif key == keyboard.Key.space:
                x, y = pyautogui.position()
                r, g, b = pyautogui.pixel(x, y)
                self.show_color((r, g, b))
        except Exception as e:
            print(e)

    def show_color(self, rgb):
        r, g, b = rgb
        hex_code = '#%02x%02x%02x' % (r, g, b)
        self.preview.config(bg=hex_code)
        self.rgb_label.config(text=f"RGB: ({r}, {g}, {b})")
        self.hex_label.config(text=hex_code.upper())

        # Copy hex to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(hex_code.upper())

    def update_preview(self):
        try:
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            hex_code = '#%02x%02x%02x' % (r, g, b)
            self.preview.config(bg=hex_code)
        except Exception:
            pass
        self.root.after(50, self.update_preview)  # Refresh every 50ms


if __name__ == "__main__":
    ScreenColorPicker()
