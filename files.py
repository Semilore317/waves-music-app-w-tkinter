import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        self.current_directory = os.path.expanduser("~")  # Start at the user's home directory

        # Directory Navigation Section
        self.nav_frame = tk.Frame(self.root, bg="#eeeeee", height=50)
        self.nav_frame.pack(side="top", fill="x")

        self.path_entry = ttk.Entry(self.nav_frame, width=80)
        self.path_entry.insert(0, self.current_directory)
        self.path_entry.pack(side="left", padx=10, pady=10)

        ttk.Button(self.nav_frame, text="Go", command=self.change_directory).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="Up", command=self.navigate_up).pack(side="left", padx=5)

        # Main Content Section
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Type", "Size"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.column("Name", width=400)
        self.tree.column("Type", width=100)
        self.tree.column("Size", width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=self.scrollbar.set)

        # Right-click Menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Open", command=self.open_item)
        self.menu.add_command(label="Rename", command=self.rename_item)
        self.menu.add_command(label="Delete", command=self.delete_item)
        self.menu.add_command(label="Create Folder", command=self.create_folder)

        self.tree.bind("<Button-3>", self.show_menu)  # Right-click menu
        self.tree.bind("<Double-1>", self.open_item)  # Double-click to open

        # Populate initial directory
        self.populate_tree(self.current_directory)

    def populate_tree(self, directory):
        self.tree.delete(*self.tree.get_children())
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    self.tree.insert("", "end", values=(item, "Folder", "-"))
                else:
                    size = os.path.getsize(item_path)
                    self.tree.insert("", "end", values=(item, "File", f"{size} bytes"))
        except PermissionError:
            messagebox.showerror("Error", "Permission denied!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_directory(self):
        new_dir = self.path_entry.get()
        if os.path.isdir(new_dir):
            self.current_directory = new_dir
            self.populate_tree(self.current_directory)
        else:
            messagebox.showerror("Error", "Invalid directory")

    def navigate_up(self):
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir:
            self.current_directory = parent_dir
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.current_directory)
            self.populate_tree(self.current_directory)

    def open_item(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_directory, item_name)
        if os.path.isdir(item_path):
            self.current_directory = item_path
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.current_directory)
            self.populate_tree(self.current_directory)
        else:
            os.system(f'xdg-open "{item_path}"')  # Use the system's default application to open the file

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_directory, item_name)
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{item_name}'?")
        if confirm:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            self.populate_tree(self.current_directory)

    def rename_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_name = self.tree.item(selected_item, "values")[0]
        item_path = os.path.join(self.current_directory, item_name)
        new_name = filedialog.asksaveasfilename(initialfile=item_name, title="Rename Item")
        if new_name:
            new_path = os.path.join(self.current_directory, os.path.basename(new_name))
            os.rename(item_path, new_path)
            self.populate_tree(self.current_directory)

    def create_folder(self):
        folder_name = filedialog.asksaveasfilename(title="Create Folder", defaultextension="")
        if folder_name:
            os.mkdir(folder_name)
            self.populate_tree(self.current_directory)

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
