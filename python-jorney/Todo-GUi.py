import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

FILE = Path("final_project/data.json")

#load and save
def load():
    try:
        if FILE.exsist():
            return json.loads(FILE.read_text(encoding="UTF-8"))
        return []
    except:
        messagebox.showerror("Error", "Cannot load file")
    return []
def save(todos):
    try:
        FILE.parent.mkdir(exist_ok=True)
        FILE.write_text(json.dumps(todos, indent=2), encoding="UTF-8")
    except:
        messagebox.showerror("Error", "Cannot save file")

#main app
def run():
    todos = load()
    def refresh():
        listbox.delete(0, tk.END)
        for i, todo in enumerate(todos):
            status = "/" if todo["done"] else "0"
            text = f"{status} {todo['task']}"
            if todo["done"]:
                listbox.itemconfig(i, fg="gray")

    def add():
        task = entry.get().strip()
        if task:
            todos.append({"task": task, "done": False})
            save(todos)
            entry.delete(0, tk.END)
            refresh()
        else:
            messagebox.showwarning("Warning", "Please enter a task")

    def toggle():
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            todos[idx]["done"] = not todos[idx]["done"]
            save(todos)
            refresh()

    def delete():
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            if messagebox.askyesno("Delete", f"Delete '{todos[idx]['task']}'?"):
                todos.pop(idx)
                save()
                refresh()

                # Setup Window

    root = tk.Tk()
    root.title("Todo Pro")
    root.geometry("500x450")

    # Entry
    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=15, padx=20, fill=tk.X)
    entry.bind('<Return>', lambda e: add())

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Add", command=add, bg="#4CAF50", fg="white",
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Toggle", command=toggle, bg="#2196F3", fg="white",
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete, bg="#f44336", fg="white",
              width=10).pack(side=tk.LEFT, padx=5)

    # Listbox
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, font=("Arial", 11), yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    listbox.bind('<Double-Button-1>', lambda e: toggle())

    scrollbar.config(command=listbox.yview)


    refresh()
    root.mainloop()
if __name__ == "__main__":
    run()
