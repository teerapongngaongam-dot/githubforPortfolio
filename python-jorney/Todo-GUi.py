import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json

# กำหนด Path ไฟล์ให้เสถียร
CURRENT_DIR = Path(FILE).parent
FILE = CURRENT_DIR / "final_project" / "data.json"

# Load and Save
def load():
    #"""โหลดรายการสิ่งที่ต้องทำจากไฟล์ JSON อย่างปลอดภัย"""
    try:
        if FILE.exists():
            return json.loads(FILE.read_text(encoding="utf-8"))
    except Exception as e:
        # หากไฟล์เสียหรือมีปัญหาการโหลด ให้เริ่มด้วยรายการว่างเปล่า
        print(f"Load Error: {e}")
    return []

def save(todos):
    #"""บันทึกรายการสิ่งที่ต้องทำลงในไฟล์ JSON"""
    try:
        # สร้างโฟลเดอร์ถ้าไม่มี
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text(json.dumps(todos, indent=2), encoding="utf-8")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot save file: {e}")

# Main App
def run():
    todos = load()

    # Setup Window
    root = tk.Tk()
    root.title("Todo Pro")
    root.geometry("500x450")
    
    # --- ฟังก์ชันหลัก ---
    def refresh():
        #"""อัปเดต Listbox ให้แสดงข้อมูลล่าสุด"""
        listbox.delete(0, tk.END)
        for i, todo in enumerate(todos):
            # ตรวจสอบ key เพื่อป้องกัน Error จากข้อมูลที่ผิดพลาด
            is_done = todo.get("done", False)
            task_text = todo.get("task", "Unknown Task")

            status = "✓" if is_done else "○"
            display_text = f"{status} {task_text}"
            
            listbox.insert(tk.END, display_text)
            
            # แก้ไขปัญหาเรื่องสี: บังคับให้แสดงสีดำถ้ายังไม่เสร็จ
            if is_done:
                listbox.itemconfig(i, {'fg': "green"}) 
            else:
                listbox.itemconfig(i, {'fg': "red"}) # บังคับสีดำ

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
            task_name = todos[idx].get('task', 'Item')
            if messagebox.askyesno("Delete", f"Delete '{task_name}'?"):
                todos.pop(idx)
                save(todos)
                refresh()

    # --- Setup UI ---
    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=15, padx=20, fill=tk.X)
    entry.bind('<Return>', lambda e: add())

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Add", command=add, bg="#4CAF50", fg="white", 
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Toggle", command=toggle, bg="#2196F3", fg="white", 
              width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete, bg="#f44336", fg="white", 
              width=10).pack(side=tk.LEFT, padx=5)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # กำหนดค่าเริ่มต้น fg="black" เพื่อป้องกันปัญหา White-on-White
    listbox = tk.Listbox(frame, font=("Arial", 11), yscrollcommand=scrollbar.set, fg="black") 
    listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    listbox.bind('<Double-Button-1>', lambda e: toggle())

    scrollbar.config(command=listbox.yview)

    refresh()
    root.mainloop()

if __name__ == "__main__":
    run()