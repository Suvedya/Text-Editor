import tkinter as tk
from tkinter import filedialog, messagebox, font


class BasicTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Text Editor")
        self.text_area = tk.Text(root, undo=True, wrap="word")
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.file_path = None

        # Create menu bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Search", command=self.search_text)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Format menu
        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Bold", command=self.bold_text)
        format_menu.add_command(label="Italic", command=self.italic_text)
        format_menu.add_command(label="Underline", command=self.underline_text)
        menu_bar.add_cascade(label="Format", menu=format_menu)

        # Status bar
        self.status_bar = tk.Label(root, text="Line: 1 | Column: 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind("<KeyRelease>", self.update_status_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.file_path = file_path

    def save_file(self):
        if self.file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(self.file_path, 'w') as file:
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", ".txt"), ("All Files", ".*")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            self.file_path = file_path

    def search_text(self):
        search_popup = tk.Toplevel(self.root)
        search_popup.title("Search Text")
        search_popup.geometry("300x50")

        tk.Label(search_popup, text="Search:").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_popup, width=25)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_button = tk.Button(search_popup, text="Search", command=lambda: self.find_text(search_entry.get()))
        search_button.pack(side=tk.LEFT)

    def find_text(self, query):
        self.text_area.tag_remove('match', '1.0', tk.END)
        start_pos = '1.0'
        while True:
            start_pos = self.text_area.search(query, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(query)}c"
            self.text_area.tag_add('match', start_pos, end_pos)
            self.text_area.tag_config('match', background='yellow', foreground='black')
            start_pos = end_pos

    def bold_text(self):
        self.apply_format('bold', weight='bold')

    def italic_text(self):
        self.apply_format('italic', slant='italic')

    def underline_text(self):
        self.apply_format('underline', underline=1)

    def apply_format(self, tag_name, **font_options):
        start, end = self.text_area.index(tk.SEL_FIRST), self.text_area.index(tk.SEL_LAST)
        current_tags = self.text_area.tag_names(tk.SEL_FIRST)
        if tag_name in current_tags:
            self.text_area.tag_remove(tag_name, start, end)
        else:
            font_config = font.Font(self.text_area, self.text_area.cget("font")).actual()
            font_config.update(font_options)
            self.text_area.tag_configure(tag_name, font=font.Font(**font_config))
            self.text_area.tag_add(tag_name, start, end)

    def update_status_bar(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Line: {row} | Column: {col}")


if __name__ == "__main__":
    root = tk.Tk()
    editor = BasicTextEditor(root)
    root.mainloop()