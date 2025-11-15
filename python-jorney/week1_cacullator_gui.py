import tkinter as tk
from tkinter import font

class Calculator:
def __init__(self, root):
self.root = root
self.root.title(“Calculator”)
self.root.geometry(“400x550”)
self.root.resizable(False, False)
self.root.configure(bg=”#1e1e1e”)


    self.expression = ""
    self.result_var = tk.StringVar()
    self.result_var.set("0")
    
    self.create_widgets()

def create_widgets(self):
    # Display frame
    display_frame = tk.Frame(self.root, bg="#1e1e1e")
    display_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Result display
    display_font = font.Font(family="Arial", size=36, weight="bold")
    self.display = tk.Label(
        display_frame,
        textvariable=self.result_var,
        font=display_font,
        bg="#2d2d2d",
        fg="white",
        anchor="e",
        padx=20,
        pady=20
    )
    self.display.pack(expand=True, fill="both")
    
    # Buttons frame
    buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
    buttons_frame.pack(padx=20, pady=(0, 20))
    
    # Button layout
    buttons = [
        ['C', '←', '%', '/'],
        ['7', '8', '9', '*'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['0', '.', '=']
    ]
    
    button_font = font.Font(family="Arial", size=18)
    
    for i, row in enumerate(buttons):
        for j, btn_text in enumerate(row):
            # Determine button properties
            if btn_text == '=':
                bg_color = "#4CAF50"
                fg_color = "white"
                colspan = 2
            elif btn_text in ['C', '←']:
                bg_color = "#f44336"
                fg_color = "white"
                colspan = 1
            elif btn_text in ['/', '*', '-', '+', '%']:
                bg_color = "#FF9800"
                fg_color = "white"
                colspan = 1
            else:
                bg_color = "#424242"
                fg_color = "white"
                colspan = 1
            
            btn = tk.Button(
                buttons_frame,
                text=btn_text,
                font=button_font,
                bg=bg_color,
                fg=fg_color,
                activebackground=bg_color,
                activeforeground=fg_color,
                border=0,
                cursor="hand2",
                command=lambda x=btn_text: self.on_button_click(x)
            )
            
            btn.grid(
                row=i,
                column=j,
                columnspan=colspan,
                sticky="nsew",
                padx=5,
                pady=5
            )
    
    # Configure grid weights
    for i in range(5):
        buttons_frame.grid_rowconfigure(i, weight=1, minsize=70)
    for j in range(4):
        buttons_frame.grid_columnconfigure(j, weight=1, minsize=70)

def on_button_click(self, char):
    if char == 'C':
        self.expression = ""
        self.result_var.set("0")
    elif char == '←':
        self.expression = self.expression[:-1]
        self.result_var.set(self.expression if self.expression else "0")
    elif char == '=':
        try:
            result = str(eval(self.expression))
            self.result_var.set(result)
            self.expression = result
        except:
            self.result_var.set("Error")
            self.expression = ""
    else:
        if self.expression == "0":
            self.expression = ""
        self.expression += str(char)
        self.result_var.set(self.expression)


if __name__ == “__main__”:
root = tk.Tk()
calculator = Calculator(root)
root.mainloop() 
