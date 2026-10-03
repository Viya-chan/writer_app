import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
import json
import os
import data
#------ Данные и память ------
all_data = data.load_data()
if "characters" not in all_data:
    all_data["characters"] = []
if "chapters" not in all_data:
    all_data["chapters"] = []
characters = all_data["characters"]
chapters = all_data["chapters"]


# ----- Логика ------
def refresh_list():
    listbox_characters.delete(0, tk.END)
    for ch in characters:
        listbox_characters.insert(tk.END, ch["name"])

def add_character():
    name = entry_name.get().strip()
    character = entry_character.get().strip()
    appearance = entry_appearance.get().strip()
    if name == "":
        print("Вы не ввели имя")
        return
    characters.append({
        "name": name,
        "character": character,
        "appearance": appearance,
    })
    entry_name.delete(0, tk.END)
    entry_character.delete(0, tk.END)
    entry_appearance.delete(0, tk.END)
    refresh_list()
    save_all()

def del_character():
    selected = listbox_characters.curselection()
    if not selected:
        return
    del characters[selected[0]]
    entry_name.delete(0, tk.END)
    entry_appearance.delete(0, tk.END)
    entry_character.delete(0, tk.END)

    refresh_list()
    save_all()

def del_all():
    listbox_characters.delete(0, tk.END)
    refresh_list()
    save_all()

def on_double_click(event):
    index = listbox_characters.nearest(event.y)
    listbox_characters.delete(index)
    refresh_list()
    save_all()

def on_select(event):
    selected = listbox_characters.curselection()
    if not selected:
        return
    ch = characters[selected[0]]
    entry_name.delete(0, tk.END)
    entry_name.insert(0, ch["name"])
    entry_character.delete(0, tk.END)
    entry_character.insert(0, ch["character"])
    entry_appearance.delete(0, tk.END)
    entry_appearance.insert(0, ch["appearance"])

# Фунции глав
def refresh_chapters():
    listbox_chapters.delete(0, tk.END)
    for ch in chapters:
        listbox_chapters.insert(tk.END, ch["title"])

def add_chapters():
    title = entry_chapter_title.get().strip()
    status = status_var.get()
    text = text_chapter.get("1.0", tk.END).strip()

    if title == "":
        print("Вы не ввели название главы")
        return
    chapters.append({
        "title": title,
        "status": status,
        "text": text,
    })

    entry_chapter_title.delete(0, tk.END)
    status_var.set("Черновик")
    text_chapter.delete("1.0",tk.END)
    refresh_chapters()
    save_all()

def del_chapter():
    selected = listbox_chapters.curselection()
    if not selected:
        return
    del chapters[selected[0]]

    entry_chapter_title.delete(0, tk.END)
    status_var.set("Черновик")
    text_chapter.delete("1.0", tk.END)

    refresh_chapters()
    save_all()

def on_select_chapter(event):
    selected = listbox_chapters.curselection()
    if not selected:
        return
    ch = chapters[selected[0]]

    entry_chapter_title.delete(0, tk.END)
    entry_chapter_title.insert(0, ch["title"])

    status_var.set(ch["status"])

    text_chapter.delete("1.0", tk.END)
    text_chapter.insert("1.0", ch["text"])


def show_caracters ():
    #chapters_frame.pack_forget()
    characters_frame.pack(fill="both", expand=True)

def show_chapters():
    characters_frame.pack_forget()
    #chapters_frame.pack(fill="both", expand=True)

def save_all():
    data.save_data(all_data)    

# ------ Интерфейс ------ 
# ------Главное окно --------       
root = ctk.CTk()
root.title("Моя программа")
root.geometry("700x500")
root.grid_columnconfigure(0, weight=0) #первый столбик не рстягивается
root.grid_columnconfigure(1, weight=1) #второй столбик рястягивается
root.grid_rowconfigure(0, weight=1) #строка растягивается

#-------Боковое меню ---------

sidebar = ctk.CTkFrame(root, width=150, corner_radius=0)
sidebar.grid(row = 0, column = 0, sticky = "ns")
sidebar.grid_propagate(False)
sidebar.configure(width = 150)

btn1 = ctk.CTkButton(sidebar, text="Персонажи", command=show_caracters)
btn1.grid(row = 0, column = 0)

btn2 = ctk.CTkButton(sidebar, text="Главы", command=show_chapters)
btn2.grid(row = 1, column = 0)

btn3 = ctk.CTkButton(sidebar, text="Сюжет")
btn3.grid(row = 2, column = 0)

#---------Средняя часть --------

content = ctk.CTkFrame(root, fg_color="transparent")
content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(0, weight=1)
content.grid(row = 0, column = 1, sticky = "nsew")

#--------Персонажи----------------

characters_frame = ctk.CTkFrame(content)
characters_frame.grid(row = 0, column = 0, sticky = "nsew")
characters_frame.grid_columnconfigure(0, weight=0)
characters_frame.grid_columnconfigure(1, weight=1)
characters_frame.grid_rowconfigure(0, weight=1)

listbox_characters = tk.Listbox(characters_frame, width=30)
listbox_characters.grid(row = 0, column= 0, rowspan = 8, sticky="nsew")
listbox_characters.bind("<<ListboxSelect>>", on_select)

panel = ctk.CTkFrame(characters_frame)
panel.grid_columnconfigure(0, weight=1)     
panel.grid(row = 0, column = 1, sticky = "nsew")

ctk.CTkLabel(panel, text="Имя").grid(row = 0, column = 0, pady=(10, 0))
entry_name = ctk.CTkEntry(panel, width=30)
entry_name.grid(row = 1, column = 0, sticky = "ew", padx = 10)

ctk.CTkLabel(panel, text="Характер").grid(row = 2, column = 0, pady=(10, 0))
entry_character = ctk.CTkEntry(panel, width=30)
entry_character.grid(row = 3, column = 0, sticky = "ew", padx = 10)

ctk.CTkLabel(panel, text="Внешность").grid(row = 4, column = 0, pady=(10, 0))
entry_appearance = ctk.CTkEntry(panel, width=30)
entry_appearance.grid(row = 5, column = 0, sticky = "ew", padx = 10)

add_button = ctk.CTkButton(panel, text = "Добавить", command=add_character)
add_button.grid(row = 6, column = 0, sticky = "ew", padx = 10, pady = 5)

del_button = ctk.CTkButton(panel, text= "Удалить", command=del_character)
del_button.grid(row = 7, column = 0, sticky = "ew", padx = 10, pady = 5)

del_all_button = ctk.CTkButton(panel, text= "Удалить все", command= del_all)
del_all_button.grid(row = 8, column = 0, sticky = "ew", padx = 10, pady = 5)

listbox_characters.bind("<Double-Button-1>", on_double_click)

#----------Главы----------


chapters_frame = ctk.CTkFrame(content)
chapters_frame.grid(row = 0, column = 0)
chapters_frame.grid_columnconfigure(0, weight= 0)
chapters_frame.grid_columnconfigure( 1, weight= 1)
chapters_frame.grid_rowconfigure(0, weight=1)

# Список глав слева
listbox_chapters = tk.Listbox(chapters_frame, width=30)
listbox_chapters.grid(row = 0, column= 0, sticky="nsew", rowspan= )
listbox_chapters.bind("<<ListboxSelect>>", on_select_chapter)

# Панель справа
panel_chapters = ctk.CTkFrame(chapters_frame)
panel_chapters.grid(row = 0, column = 1, sticky = "nsew", padx=10, pady=10)

# Верхняя строка(название + статус)
top_row = ctk.CTkFrame(panel_chapters)
top_row.grid(row = 0, column = 0, sticky = "ew")

# Название 
title_block = ctk.CTkFrame(top_row)
title_block.pack(side="left", padx=(0, 10))
ctk.CTkLabel(title_block, text="Название").pack(anchor="w")
entry_chapter_title = ctk.CTkEntry(title_block, width=300)
entry_chapter_title.pack()

# Статус 
status_blok = ctk.CTkFrame(top_row)
status_blok.pack(side="left")
ctk.CTkLabel(status_blok, text="Статус").pack(anchor="w")
status_var = tk.StringVar(value="Черновик")
status_menu = tk.OptionMenu(
    status_blok, status_var,
    "Черновик", "В работе", "Готово", "Выложено"
)
status_menu.pack()

# Главы
ctk.CTkLabel(panel_chapters, text="Главы").pack(anchor="w", pady=(0, 10))
text_chapter = ctk.CTkTextbox(panel_chapters, height=15, width=50)
text_chapter.pack(fill="both", expand=True)

# Кнопки 
buttons_row = ctk.CTkFrame(panel_chapters)
buttons_row.pack(fill="x", pady=(10, 0))

add_chapter_btn = ctk.CTkButton(buttons_row, text="Добавить главу", command=add_chapters)
add_chapter_btn.pack(side="left")

dell_chapter_btn = ctk.CTkButton(buttons_row, text="Удалить главу", command=del_chapter)
dell_chapter_btn.pack(side="left")

chapters_frame.pack_forget()




refresh_list()
#refresh_chapters()
root.mainloop()
