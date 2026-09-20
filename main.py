
import tkinter as tk
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
    chapters_frame.pack_forget()
    characters_frame.pack(fill="both", expand=True)

def show_chapters():
    characters_frame.pack_forget()
    chapters_frame.pack(fill="both", expand=True)

def save_all():
    data.save_data(all_data)    

# ------ Интерфейс ------ 
# ------Главное окно --------       
root = tk.Tk()
root.title("Моя программа")
root.geometry("700x500")

#-------Боковое меню ---------

sidebar = tk.Frame(root, width=150, bg = "lightgray")
sidebar.pack(side="left", fill="y")

btn1 = tk.Button(sidebar, text="Персонажи", command=show_caracters)
btn1.pack(padx=5, pady=5, fill="x")

btn2 = tk.Button(sidebar, text="Главы", command=show_chapters)
btn2.pack(padx=5, pady=5, fill= "x")

btn3 = tk.Button(sidebar, text="Сюжет")
btn3.pack(padx=5, pady=5, fill="x")

#---------Средняя часть --------

content = tk.Frame(root)
content.pack(side="left", fill="both", expand=True)

#--------Персонажи----------------

characters_frame = tk.Frame(content)
characters_frame.pack(fill="both", expand=True)

listbox_characters = tk.Listbox(characters_frame, width=30)
listbox_characters.pack(side="left", fill="y")
listbox_characters.bind("<<ListboxSelect>>", on_select)

panel = tk.Frame(characters_frame)
panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(panel, text="Имя").pack(anchor="w", pady=(10, 0))
entry_name = tk.Entry(panel, width=30)
entry_name.pack(fill="x")

tk.Label(panel, text="Характер").pack(anchor="w", pady=(10, 0))
entry_character = tk.Entry(panel, width=30)
entry_character.pack(fill="x")

tk.Label(panel, text="Внешность").pack(anchor="w", pady=(10, 0))
entry_appearance = tk.Entry(panel, width=30)
entry_appearance.pack(fill="x")

add_button = tk.Button(panel, text = "Добавить", command=add_character)
add_button.pack()

del_button = tk.Button(panel, text= "Удалить", command=del_character)
del_button.pack()

del_all_button = tk.Button(panel, text= "Удалить все", command= del_all)
del_all_button.pack()

listbox_characters.bind("<Double-Button-1>", on_double_click)

#----------Главы----------

chapters_frame = tk.Frame(content)
chapters_frame.pack(fill="both", expand=True)

# Список глав слева
listbox_chapters = tk.Listbox(chapters_frame, width=30)
listbox_chapters.pack(side="left", fill="y")
listbox_chapters.bind("<<ListboxSelect>>", on_select_chapter)

# Панель справа
panel_chapters = tk.Frame(chapters_frame)
panel_chapters.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Верхняя строка(название + статус)
top_row = tk.Frame(panel_chapters)
top_row.pack(fill="x")

# Название 
title_block = tk.Frame(top_row)
title_block.pack(side="left", padx=(0, 10))
tk.Label(title_block, text="Название").pack(anchor="w")
entry_chapter_title = tk.Entry(title_block, width=30)
entry_chapter_title.pack()

# Статус 
status_blok = tk.Frame(top_row)
status_blok.pack(side="left")
tk.Label(status_blok, text="Статус").pack(anchor="w")
status_var = tk.StringVar(value="Черновик")
status_menu = tk.OptionMenu(
    status_blok, status_var,
    "Черновик", "В работе", "Готово", "Выложено"
)
status_menu.pack()

# Главы
tk.Label(panel_chapters, text="Главы").pack(anchor="w", pady=(0, 10))
text_chapter = tk.Text(panel_chapters, height=15, width=50)
text_chapter.pack(fill="both", expand=True)

# Кнопки 
buttons_row = tk.Frame(panel_chapters)
buttons_row.pack(fill="x", pady=(10, 0))

add_chapter_btn = tk.Button(buttons_row, text="Добавить главу", command=add_chapters)
add_chapter_btn.pack(side="left")

dell_chapter_btn = tk.Button(buttons_row, text="Удалить главу", command=del_chapter)
dell_chapter_btn.pack(side="left")

chapters_frame.pack_forget()






refresh_list()
refresh_chapters()
root.mainloop()
