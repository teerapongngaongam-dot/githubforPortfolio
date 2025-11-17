import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Constants

FILE = Path(“final_project/data.json”)
COLORS = {
    “bg”: “#f5f5f5”,
    “primary”: “#4CAF50”,
    “secondary”: “#2196F3”,
    “danger”: “#f44336”,
    “warning”: “#FF9800”,
    “text”: “#333333”
}

class TodoManager:
    “”“Handles all todo data operations”””

    def __init__(self, filepath: Path):
    self.filepath = filepath
    self.todos: List[Dict] = []
    self.load()
    
    def load(self) -> bool:
        try:
            if self.filepath.exists():
                data = json.loads(self.filepath.read_text(encoding="utf-8"))
            # Validate data structure
            if isinstance(data, list):
                self.todos = data
                return True
            else:
                print("Invalid data format, starting fresh")
                self.todos = []
                return False
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Error", f"Failed to load todos: {str(e)}")
            self.todos = []
            return False
            return True

    def save(self) -> bool:
    """Save todos to file with error handling"""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.filepath.write_text(
                json.dumps(self.todos, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            return True
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save todos: {str(e)}")
            return False

    def add(self, task: str, priority: str = "normal") -> bool:
        """Add a new todo"""
        if not task.strip():
            return False
    
        todo = {
            "task": task.strip(),
            "done": False,
            "created": datetime.now().isoformat(),
            "priority": priority
        }
        self.todos.append(todo)
        return self.save()

    def mark_done(self, index: int) -> bool:
        """Mark a todo as done"""
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = True
            self.todos[index]["completed"] = datetime.now().isoformat()
            return self.save()
        return False

    def toggle_done(self, index: int) -> bool:
        """Toggle done status"""
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = not self.todos[index]["done"]
            if self.todos[index]["done"]:
                self.todos[index]["completed"] = datetime.now().isoformat()
            else:
                self.todos[index].pop("completed", None)
            return self.save()
        return False

    def delete(self, index: int) -> bool:
        """Delete a todo"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            return self.save()
        return False

    def edit(self, index: int, new_task: str) -> bool:
        """Edit a todo's text"""
        if 0 <= index < len(self.todos) and new_task.strip():
            self.todos[index]["task"] = new_task.strip()
            self.todos[index]["edited"] = datetime.now().isoformat()
            return self.save()
        return False

    def get_filtered(self, filter_type: str = "all") -> List[tuple]:
        """Get filtered todos with their indices"""
        if filter_type == "active":
            return [(i, t) for i, t in enumerate(self.todos) if not t["done"]]
        elif filter_type == "completed":
            return [(i, t) for i, t in enumerate(self.todos) if t["done"]]
        else:
            return list(enumerate(self.todos))

    def clear_completed(self) -> bool:
        """Remove all completed todos"""
        self.todos = [t for t in self.todos if not t["done"]]
        return self.save()


class TodoApp:
“”“Main GUI application”””


    def __init__(self, root: tk.Tk):
        self.root = root
        self.manager = TodoManager(FILE)
        self.filter_var = tk.StringVar(value="all")
        self.search_var = tk.StringVar()
    
        self.setup_ui()
        self.bind_shortcuts()
        self.refresh()

    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("Todo Pro - Enhanced")
        self.root.geometry("600x550")
        self.root.configure(bg=COLORS["bg"])
    
        # Top frame - Entry and Add button
    top_frame = tk.Frame(self.root, bg=COLORS["bg"])
    top_frame.pack(pady=15, fill=tk.X, padx=20)
    
        self.entry = tk.Entry(
            top_frame,
            font=("Arial", 12),
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.entry.bind('<Return>', lambda e: self.add_task())
    
        tk.Button(
            top_frame,
            text="➕ Add",
            command=self.add_task,
            bg=COLORS["primary"],
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    # Search frame
    search_frame = tk.Frame(self.root, bg=COLORS["bg"])
    search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    tk.Label(
        search_frame,
        text="🔍",
        bg=COLORS["bg"],
        font=("Arial", 12)
    ).pack(side=tk.LEFT)
    
    search_entry = tk.Entry(
        search_frame,
        textvariable=self.search_var,
        font=("Arial", 10),
        relief=tk.SOLID,
        borderwidth=1
    )
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=3)
    self.search_var.trace('w', lambda *args: self.refresh())
    
    # Filter frame
    filter_frame = tk.Frame(self.root, bg=COLORS["bg"])
    filter_frame.pack(pady=(0, 10))
    
    for text, value in [("All", "all"), ("Active", "active"), ("Completed", "completed")]:
        tk.Radiobutton(
            filter_frame,
            text=text,
            variable=self.filter_var,
            value=value,
            command=self.refresh,
            bg=COLORS["bg"],
            font=("Arial", 9),
            selectcolor=COLORS["secondary"],
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
    
    # Action buttons frame
    btn_frame = tk.Frame(self.root, bg=COLORS["bg"])
    btn_frame.pack(pady=5)
    
    buttons = [
        ("✓ Toggle Done", self.toggle_task, COLORS["secondary"]),
        ("✏️ Edit", self.edit_task, COLORS["warning"]),
        ("🗑️ Delete", self.delete_task, COLORS["danger"]),
        ("🧹 Clear Done", self.clear_completed, "#9E9E9E")
    ]
    
    for text, cmd, color in buttons:
        tk.Button(
            btn_frame,
            text=text,
            command=cmd,
            bg=color,
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=3)
    
    # Listbox with scrollbar
    list_frame = tk.Frame(self.root)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    self.listbox = tk.Listbox(
        list_frame,
        font=("Arial", 11),
        selectmode=tk.SINGLE,
        relief=tk.SOLID,
        borderwidth=1,
        yscrollcommand=scrollbar.set,
        activestyle='none'
    )
    self.listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    scrollbar.config(command=self.listbox.yview)
    
    # Double-click to toggle done
    self.listbox.bind('<Double-Button-1>', lambda e: self.toggle_task())
    
    # Status bar
    self.status_label = tk.Label(
        self.root,
        text="",
        bg=COLORS["bg"],
        fg=COLORS["text"],
        font=("Arial", 9),
        anchor=tk.W
    )
    self.status_label.pack(fill=tk.X, padx=20, pady=(0, 10))

    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Delete>', lambda e: self.delete_task())
        self.root.bind('<Control-d>', lambda e: self.toggle_task())
        self.root.bind('<Control-e>', lambda e: self.edit_task())
        self.root.bind('<Control-n>', lambda e: self.entry.focus())
        self.root.bind('<Escape>', lambda e: self.entry.delete(0, tk.END))

    def refresh(self):
    """Refresh the listbox display"""
    self.listbox.delete(0, tk.END)
    
    # Get filtered todos
    filtered = self.manager.get_filtered(self.filter_var.get())
    
    # Apply search filter
    search_term = self.search_var.get().lower()
    if search_term:
        filtered = [(i, t) for i, t in filtered if search_term in t["task"].lower()]
    
    # Display todos
    for original_idx, todo in filtered:
        status = "✓" if todo["done"] else "○"
        priority = {"high": "🔴", "normal": "", "low": "🔵"}.get(todo.get("priority", "normal"), "")
        text = f"{status} {priority} {todo['task']}"
        
        self.listbox.insert(tk.END, text)
        # Store original index as item data
        self.listbox.itemconfig(tk.END, fg="#888888" if todo["done"] else COLORS["text"])
    
    # Store mapping of listbox index to original todo index
    self.index_map = {i: original_idx for i, (original_idx, _) in enumerate(filtered)}
    
    # Update status bar
    total = len(self.manager.todos)
    active = sum(1 for t in self.manager.todos if not t["done"])
    completed = total - active
    self.status_label.config(
        text=f"Total: {total} | Active: {active} | Completed: {completed}"
    )

    def get_selected_index(self) -> int:
        """Get the original index of selected item"""
        sel = self.listbox.curselection()
        if sel:
            listbox_idx = sel[0]
            return self.index_map.get(listbox_idx, -1)
        return -1

    def add_task(self):
        """Add a new task"""
        task = self.entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
    
        if self.manager.add(task):
            self.entry.delete(0, tk.END)
            self.refresh()
            self.entry.focus()

    def toggle_task(self):
        """Toggle done status of selected task"""
        idx = self.get_selected_index()
        if idx >= 0:
            self.manager.toggle_done(idx)
            self.refresh()

    def delete_task(self):
        """Delete selected task"""
        idx = self.get_selected_index()
        if idx >= 0:
            task = self.manager.todos[idx]["task"]
            if messagebox.askyesno("Confirm Delete", f"Delete task:\n'{task}'?"):
                self.manager.delete(idx)
                self.refresh()

    def edit_task(self):
        """Edit selected task"""
        idx = self.get_selected_index()
        if idx >= 0:
            old_task = self.manager.todos[idx]["task"]
            new_task = simpledialog.askstring(
                "Edit Task",
                "Edit task:",
                initialvalue=old_task
            )
            if new_task and new_task != old_task:
                self.manager.edit(idx, new_task)
                self.refresh()

    def clear_completed(self):
        """Clear all completed tasks"""
        completed_count = sum(1 for t in self.manager.todos if t["done"])
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
    
        if messagebox.askyesno(
            "Confirm Clear",
            f"Clear {completed_count} completed task(s)?"
        ):
            self.manager.clear_completed()
            self.refresh()


    def run():
    “”“Run the application”””
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

    if __name__ == "__main__":
    run()
