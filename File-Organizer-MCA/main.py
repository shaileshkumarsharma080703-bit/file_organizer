import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from organizer.service import FileOrganizer

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("900x650")
        self.folder = tk.StringVar()
        self.recursive = tk.BooleanVar()
        self.preview_only = tk.BooleanVar(value=True)
        self.organizer = FileOrganizer()
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="File Organizer", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Organize files by type without overwriting existing files.").pack(anchor="w", pady=(3,18))

        path = ttk.Frame(frame); path.pack(fill="x")
        ttk.Entry(path, textvariable=self.folder).pack(side="left", fill="x", expand=True)
        ttk.Button(path, text="Browse", command=self.select_folder).pack(side="left", padx=8)

        options = ttk.LabelFrame(frame, text="Options", padding=10); options.pack(fill="x", pady=15)
        ttk.Checkbutton(options, text="Scan subfolders", variable=self.recursive).pack(anchor="w")
        ttk.Checkbutton(options, text="Preview only (recommended)", variable=self.preview_only).pack(anchor="w", pady=6)

        actions = ttk.Frame(frame); actions.pack(fill="x")
        ttk.Button(actions, text="Preview", command=self.preview).pack(side="left")
        ttk.Button(actions, text="Organize", command=self.organize).pack(side="left", padx=8)
        ttk.Button(actions, text="Undo Last Operation", command=self.undo).pack(side="left")

        self.progress = ttk.Progressbar(frame, mode="determinate"); self.progress.pack(fill="x", pady=12)
        self.status = tk.StringVar(value="Ready"); ttk.Label(frame, textvariable=self.status).pack(anchor="w")

        box = ttk.LabelFrame(frame, text="Activity", padding=8); box.pack(fill="both", expand=True, pady=10)
        self.log = tk.Text(box, wrap="word", state="disabled", font=("Consolas", 10))
        self.log.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(box, orient="vertical", command=self.log.yview); scroll.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scroll.set)

    def write(self, text):
        self.log.configure(state="normal"); self.log.insert("end", text + "\n")
        self.log.see("end"); self.log.configure(state="disabled")

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            self.folder.set(folder); self.write(f"Selected: {folder}")

    def get_folder(self):
        folder = Path(self.folder.get()).expanduser()
        if not folder.is_dir():
            messagebox.showerror("Invalid Folder", "Please select a valid folder.")
            return None
        return folder

    def preview(self):
        folder = self.get_folder()
        if not folder: return
        result = self.organizer.preview(folder, self.recursive.get())
        self.progress["value"] = 100
        self.status.set(f"{len(result.operations)} file(s) planned, {result.skipped} skipped.")
        self.write("\n--- PREVIEW ---")
        for op in result.operations:
            self.write(f"[PLAN] {op.source.name} -> {op.destination.parent.name}/{op.destination.name}")
        if not result.operations: self.write("Nothing needs to be organized.")

    def organize(self):
        folder = self.get_folder()
        if not folder: return
        if self.preview_only.get():
            self.preview()
            self.write("Preview mode is enabled. Uncheck it to move files.")
            return
        if not messagebox.askyesno("Confirm", "Move files into category folders?"):
            return
        self.status.set("Organizing..."); self.progress["value"] = 20
        try:
            result = self.organizer.organize(folder, self.recursive.get())
        except Exception as exc:
            messagebox.showerror("Error", str(exc)); return
        self.progress["value"] = 100
        self.status.set(f"Completed: {result.moved} moved, {result.skipped} skipped, {result.failed} failed.")
        self.write("\n--- ORGANIZATION ---")
        for msg in result.messages: self.write(msg)
        messagebox.showinfo("Complete", f"Moved: {result.moved}\nSkipped: {result.skipped}\nFailed: {result.failed}")

    def undo(self):
        try:
            count = self.organizer.undo_last()
            self.write(f"[UNDO] Restored {count} file(s).")
            self.status.set(f"Undo completed: {count} file(s) restored.")
        except Exception as exc:
            messagebox.showerror("Undo", str(exc))

if __name__ == "__main__":
    root = tk.Tk()
    FileOrganizerApp(root)
    root.mainloop()
