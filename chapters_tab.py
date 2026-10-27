import customtkinter as ctk
import tkinter as tk
import data_meneger

class ChaptersTab:
    def __init__(self, parent):
        self.chapters = data_meneger.chapters
        self.selected_index = None

        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row = 0, column = 0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight= 0)
        self.frame.grid_columnconfigure( 1, weight= 1)
        self.frame.grid_rowconfigure(0, weight=1)

# Список глав слева
        self.listbox = ctk.CTkScrollableFrame(self.frame, width=200)
        self.listbox.grid(row=0, column=0, sticky="nsew")

# Панель справа
        self.panel = ctk.CTkFrame(self.frame)
        self.panel.grid(row = 0, column = 1, sticky = "nsew", padx=10, pady=10)
        self.panel.grid_columnconfigure(0, weight = 1)
        self.panel.grid_rowconfigure(2, weight = 1)

        # Верхняя строка(название + статус)
        self.top_row = ctk.CTkFrame(self.panel)
        self.top_row.grid(row = 0, column = 0, sticky = "ew")
        self.top_row.grid_columnconfigure(0, weight = 0)
        self.top_row.grid_columnconfigure(1, weight = 0)

# Название 
        self.title_block = ctk.CTkFrame(self.top_row)
        self.title_block.grid(row = 0, column = 0, sticky = "w", padx=(0,10))
        ctk.CTkLabel(self.title_block, text="Название").grid(row = 0, column = 0, sticky = "w")
        self.entry_chapter_title = ctk.CTkEntry(self.title_block, width=300)
        #self.entry_chapter_title.bind("<KeyRelease>", mark_as_dirty)
        self.entry_chapter_title.grid(row=1, column=0)

# Статус 
        self.status_blok = ctk.CTkFrame(self.top_row)
        self.status_blok.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(self.status_blok, text="Статус").grid(row=0, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Черновик")
        self.status_menu = tk.OptionMenu(
            self.status_blok, self.status_var,
            "Черновик", "В работе", "Готово", "Выложено"
        )
        self.status_menu.grid(row=1, column=0)

# Главы
        ctk.CTkLabel(self.panel, text="Главы").grid(row=1, column=0, sticky="w", pady=(0,10))
        self.text_chapter = ctk.CTkTextbox(self.panel, height=15, width=50)
        #self.text_chapter.bind("<KeyRelease>", mark_as_dirty)
        self.text_chapter.grid(row=2, column=0, sticky="nsew")

# Кнопки 
        self.buttons_row = ctk.CTkFrame(self.panel)
        self.buttons_row.grid(row=3, column=0, sticky="ew", pady=(10,0))

        self.add_chapter_btn = ctk.CTkButton(self.buttons_row, text="Добавить главу", command=self.add_chapters)
        self.add_chapter_btn.grid(row=0, column=0, padx=1)

        self.dell_chapter_btn = ctk.CTkButton(self.buttons_row, text="Удалить главу", command=self.del_chapter)
        self.dell_chapter_btn.grid(row=0, column=1, padx=1)

        self.btn_clear_chapter = ctk.CTkButton(self.buttons_row, text="Очистить", command=self.clear_chapter)
        self.btn_clear_chapter.grid(row=1, column=0, pady=1)

        self.btn_save_changes_chapter = ctk.CTkButton(self.buttons_row, text="Сохранить изменения", command=self.save_changes_chapter)
        self.btn_save_changes_chapter.grid(row= 1, column=1, pady=1)

        self.refresh_chapters()

        self.frame.grid_remove()

    def refresh_chapters(self):
        for wiget in self.listbox.winfo_children():
            wiget.destroy()
        for index, ch in enumerate(self.chapters):
            btn = ctk.CTkButton(self.listbox, text=ch["title"], command = lambda i = index: self.on_select_chapter(i))
            btn.pack(fill = "x", pady = 2)

    def add_chapters(self):
        self.title = self.entry_chapter_title.get().strip()
        self.status = self.status_var.get().strip()
        self.text = self.text_chapter.get("1.0", tk.END).strip()

        if self.title == "":
            print("Вы не ввели название главы")
            return
        self.chapters.append({
            "title": self.title,
            "status": self.status,
            "text": self.text
        })
        self.entry_chapter_title.delete(0, tk.END)
        self.status_var.set("Черновик")
        self.text_chapter.delete("1.0", tk.END)

        self.refresh_chapters()
        data_meneger.save_all()

    def del_chapter(self):
        if self.selected_index is None:
            print("Вы не выбрали главу")
            return
        del self.chapters[self.selected_index]
        self.entry_chapter_title.delete(0, tk.END)
        self.status_var.set("Черновик")
        self.text_chapter.delete("1.0", tk.END)

        self.refresh_chapters()
        data_meneger.save_all()

    def on_select_chapter(self, index):
        self.selected_index = index
        ch = self.chapters[index]

        self.entry_chapter_title.delete(0, tk.END)
        self.entry_chapter_title.insert(0, ch["text"])

        self.status_var.set(ch["status"])

        self.text_chapter.delete("1.0", tk.END)
        self.text_chapter.insert("1.0", ch["text"])

    def save_changes_chapter(self):
        self.title = self.entry_chapter_title.get().strip()
        self.chapters[self.selected_index]["title"] = self.entry_chapter_title.get().strip()
        self.chapters[self.selected_index]["status"] = self.status_var.get()
        self.chapters[self.selected_index]["text"] = self.text_chapter.get("1.0", tk.END).strip()

        self.refresh_chapters()
        data_meneger.save_all()

    def clear_chapter(self):
        self.entry_chapter_title.delete(0, tk.END)
        self.text_chapter.delete("1.0", tk.END)
        self.status_var.set("Черновик")
    
