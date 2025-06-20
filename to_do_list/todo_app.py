import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkcalendar import DateEntry
import json
import os
import datetime

DATA_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List")
        self.root.geometry("700x600")
        self.root.configure(bg="white")
        self.tasks = []
        self.dark_mode = False

        self.load_tasks()

        self.setup_ui()
        self.populate_listbox()

    def setup_ui(self):
        self.title_label = tk.Label(self.root, text="Advanced To-Do List", font=("Helvetica", 20, "bold"), bg="white")
        self.title_label.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.root, bg="white")
        input_frame.pack(pady=5, fill=tk.X, padx=10)

        self.task_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=25)
        self.task_entry.grid(row=0, column=0, padx=5)

        self.date_entry = DateEntry(input_frame, font=("Helvetica", 12), width=12)
        self.date_entry.grid(row=0, column=1, padx=5)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(input_frame, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.grid(row=0, column=2, padx=5)

        tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white").grid(row=0, column=3, padx=5)

        # Search and filter
        filter_frame = tk.Frame(self.root, bg="white")
        filter_frame.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(filter_frame, text="Search:", bg="white").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(filter_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Go", command=self.search_tasks).pack(side=tk.LEFT)
        tk.Button(filter_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=2)

        tk.Button(filter_frame, text="Sort by Date", command=self.sort_by_date).pack(side=tk.RIGHT, padx=2)
        tk.Button(filter_frame, text="Sort by Priority", command=self.sort_by_priority).pack(side=tk.RIGHT)

        # Listbox
        self.task_listbox = tk.Listbox(self.root, font=("Helvetica", 12), height=15)
        self.task_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Action buttons
        action_frame = tk.Frame(self.root, bg="white")
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="Mark Done", command=self.complete_task, bg="#2196F3", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Edit", command=self.edit_task, bg="#FFA500", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Delete", command=self.delete_task, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Clear All", command=self.clear_all, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(action_frame, text="Export", command=self.export_tasks, bg="#607D8B", fg="white").grid(row=0, column=4, padx=5)

        # Dark mode
        self.dark_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.dark_button.pack(pady=5)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        due_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        priority = self.priority_var.get()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False, "priority": priority, "due": due_date})
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.populate_listbox()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.populate_listbox()

    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            current_text = self.tasks[index]["text"]
            new_text = simpledialog.askstring("Edit Task", "Update task:", initialvalue=current_text)
            if new_text:
                self.tasks[index]["text"] = new_text.strip()
                self.save_tasks()
                self.populate_listbox()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this task?")
            if confirm:
                del self.tasks[index]
                self.save_tasks()
                self.populate_listbox()

    def clear_all(self):
        confirm = messagebox.askyesno("Clear All", "Delete all tasks?")
        if confirm:
            self.tasks.clear()
            self.save_tasks()
            self.populate_listbox()

    def populate_listbox(self):
        self.task_listbox.delete(0, tk.END)
        today = datetime.date.today()
        for task in self.tasks:
            status = "[✓]" if task["completed"] else "[ ]"
            overdue = datetime.datetime.strptime(task["due"], "%Y-%m-%d").date() < today
            color_tag = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }[task["priority"]]
            line = f"{status} {color_tag} {task['text']} (Due: {task['due']})"
            if overdue and not task["completed"]:
                line += " ❗"
            self.task_listbox.insert(tk.END, line)

    def search_tasks(self):
        keyword = self.search_entry.get().lower()
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if keyword in task["text"].lower() or keyword in task["priority"].lower():
                status = "[✓]" if task["completed"] else "[ ]"
                line = f"{status} {task['text']} (Due: {task['due']})"
                self.task_listbox.insert(tk.END, line)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.populate_listbox()

    def sort_by_date(self):
        self.tasks.sort(key=lambda x: x["due"])
        self.populate_listbox()

    def sort_by_priority(self):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        self.tasks.sort(key=lambda x: priority_order[x["priority"]])
        self.populate_listbox()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        color = "black" if self.dark_mode else "white"
        fg = "white" if self.dark_mode else "black"
        self.root.configure(bg=color)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=color, fg=fg)
            except:
                pass
        self.populate_listbox()

    def export_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for task in self.tasks:
                    f.write(f"{task['text']} | {task['priority']} | Due: {task['due']} | {'Done' if task['completed'] else 'Pending'}\n")
            messagebox.showinfo("Exported", "Tasks exported successfully.")

    def save_tasks(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.tasks = json.load(f)

# Launch app
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
