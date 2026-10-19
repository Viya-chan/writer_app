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
if "plot" not in all_data:
    all_data["plot"] = {"idea":"", "parts":[]}
characters = all_data["characters"]
chapters = all_data["chapters"]
plot = all_data["plot"]
parts = plot["parts"]
scene_fields = []


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

#------Функции сюжет--------
def show_idea():
    scenes_frame.grid_remove()
    idea_frame.grid()

def show_scenes():
    idea_frame.grid_remove()
    scenes_frame.grid()

def save_idea():
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    save_all()

def refresh_scines_list():
    scenes_list.delete(0, tk.END)
    for pa in parts:
        scenes_list.insert(tk.END, pa["part_name"])

def add_scenes():
    part_name = entry_part_name.get().strip()
    part_scenes = get_scenes()
    if part_name == "":
        print("Вы не ввели имя")
        return
    parts.append({
        "part_name": part_name,
        "scenes": part_scenes
    })
    entry_part_name.delete(0, tk.END)
    refresh_scines_list()
    save_all()

def dell_scenes():
    selected = scenes_list.curselection()
    if not selected:
        return
    del parts [selected[0]]
    entry_part_name.delete(0, tk.END)
    refresh_scines_list()
    save_all()

def on_select_scenes(event):
    selected = scenes_list.curselection()
    if not selected:
        return
    pa = parts[selected[0]]
    entry_part_name.delete(0, tk.END)
    entry_part_name.insert(0, pa["part_name"])
    clear_scene_fields()
    for scene_text in pa.get("scenes", []):
        field = ctk.CTkEntry(scenes_dynamic_container, width=30)
        field.grid(row=len(scene_fields), column=0, sticky="ew", pady=2)
        field.insert(0, scene_text)
        scene_fields.append(field)


#-------Функции сцен--------
def add_scene_field():
    field = ctk.CTkEntry(scenes_dynamic_container, width=30)
    field.grid(row=len(scene_fields), column=0, sticky="ew", pady=2)
    scene_fields.append(field)

def get_scenes():
    scenes = []
    for field in scene_fields:
        text = field.get().strip()
        scenes.append(text)
    return scenes

def clear_scene_fields():
    for field in scene_fields:
        field.destroy()
    scene_fields.clear()


#------Фунции в боковом меню--------
def show_caracters ():
    chapters_frame.grid_remove()
    plot_frame.grid_remove()
    characters_frame.grid()

def show_chapters():
    characters_frame.grid_remove()
    plot_frame.grid_remove()
    chapters_frame.grid()

def show_plot():
    chapters_frame.grid_remove()
    characters_frame.grid_remove()
    plot_frame.grid()


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


btn1 = ctk.CTkButton(sidebar, text="Персонажи", command=show_caracters)
btn1.grid(row = 0, column = 0, pady=1)

btn2 = ctk.CTkButton(sidebar, text="Главы", command=show_chapters)
btn2.grid(row = 1, column = 0, pady=1)

btn3 = ctk.CTkButton(sidebar, text="Сюжет", command=show_plot)
btn3.grid(row = 2, column = 0, pady=1)

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
chapters_frame.grid(row = 0, column = 0, sticky="nsew")
chapters_frame.grid_columnconfigure(0, weight= 0)
chapters_frame.grid_columnconfigure( 1, weight= 1)
chapters_frame.grid_rowconfigure(0, weight=1)

# Список глав слева
listbox_chapters = tk.Listbox(chapters_frame, width=30)
listbox_chapters.grid(row = 0, column= 0, sticky="nsew")
listbox_chapters.bind("<<ListboxSelect>>", on_select_chapter)

# Панель справа
panel_chapters = ctk.CTkFrame(chapters_frame)
panel_chapters.grid(row = 0, column = 1, sticky = "nsew", padx=10, pady=10)
panel_chapters.grid_columnconfigure(0, weight = 1)
panel_chapters.grid_rowconfigure(2, weight = 1)

# Верхняя строка(название + статус)
top_row = ctk.CTkFrame(panel_chapters)
top_row.grid(row = 0, column = 0, sticky = "ew")
top_row.grid_columnconfigure(0, weight = 0)
top_row.grid_columnconfigure(1, weight = 0)

# Название 
title_block = ctk.CTkFrame(top_row)
title_block.grid(row = 0, column = 0, sticky = "w", padx=(0,10))
ctk.CTkLabel(title_block, text="Название").grid(row = 0, column = 0, sticky = "w")
entry_chapter_title = ctk.CTkEntry(title_block, width=300)
entry_chapter_title.grid(row=1, column=0)

# Статус 
status_blok = ctk.CTkFrame(top_row)
status_blok.grid(row=0, column=1, sticky="w")
ctk.CTkLabel(status_blok, text="Статус").grid(row=0, column=0, sticky="w")
status_var = tk.StringVar(value="Черновик")
status_menu = tk.OptionMenu(
    status_blok, status_var,
    "Черновик", "В работе", "Готово", "Выложено"
)
status_menu.grid(row=1, column=0)

# Главы
ctk.CTkLabel(panel_chapters, text="Главы").grid(row=1, column=0, sticky="w", pady=(0,10))
text_chapter = ctk.CTkTextbox(panel_chapters, height=15, width=50)
text_chapter.grid(row=2, column=0, sticky="nsew")

# Кнопки 
buttons_row = ctk.CTkFrame(panel_chapters)
buttons_row.grid(row=3, column=0, sticky="ew", pady=(10,0))

add_chapter_btn = ctk.CTkButton(buttons_row, text="Добавить главу", command=add_chapters)
add_chapter_btn.grid(row=0, column=0, padx=1)

dell_chapter_btn = ctk.CTkButton(buttons_row, text="Удалить главу", command=del_chapter)
dell_chapter_btn.grid(row=0, column=1, padx=1)

chapters_frame.grid_remove()


#------Cюжет-------
plot_frame = ctk.CTkFrame(content)
plot_frame.grid(row = 0, column = 0, sticky="nsew")
plot_frame.grid_columnconfigure(0, weight=1)
plot_frame.grid_rowconfigure(0, weight=0)
plot_frame.grid_rowconfigure(1, weight=1)
plot_frame.grid_rowconfigure(2, weight=0)

plot_top_panel = ctk.CTkFrame(plot_frame)
plot_top_panel.grid(row=0, column=0, sticky="ew", pady=2)
plot_top_panel.grid_columnconfigure(0, weight=0)
plot_top_panel.grid_columnconfigure(1, weight=0)
plot_top_panel.grid_rowconfigure(0, weight=0)

btn_idea = ctk.CTkButton(plot_top_panel, text= "Идея", command=show_idea)
btn_idea.grid(row=0, column=0, padx=1)
btn_scenes = ctk.CTkButton(plot_top_panel, text= "Сцены", command=show_scenes)
btn_scenes.grid(row=0, column=1, padx=1)

idea_frame = ctk.CTkFrame(plot_frame)
idea_frame.grid(row = 1, column=0, sticky="nsew", pady=5)
idea_frame.grid_columnconfigure(0, weight=1)
idea_frame.grid_rowconfigure(0, weight=1)

idea_text = ctk.CTkTextbox(idea_frame)
idea_text.grid(row=0, column=0, sticky="nsew")

btn_idea_save = ctk.CTkButton(idea_frame, text = "Сохранить идею", command=save_idea)
btn_idea_save.grid(row=2, column=0)

idea_text.insert("1.0", plot.get("idea", ""))

idea_frame.grid_remove()
#------Раздел с идеями-----------
scenes_frame = ctk.CTkFrame(plot_frame)
scenes_frame.grid(row = 1, column=0, sticky="nsew")
scenes_frame.grid_columnconfigure(0, weight=0)
scenes_frame.grid_columnconfigure(1, weight=1)
scenes_frame.grid_rowconfigure(0, weight=1)

scenes_list = tk.Listbox(scenes_frame, width=30)
scenes_list.grid(row=0, column=0, sticky="ns")
scenes_list.bind("<<ListboxSelect>>", on_select_scenes)

scenes_text_frame = ctk.CTkFrame(scenes_frame)
scenes_text_frame.grid(row=0, column=1, sticky="nsew")
scenes_text_frame.grid_rowconfigure(0, weight=0)
scenes_text_frame.grid_rowconfigure(1, weight=0)
scenes_text_frame.grid_rowconfigure(2, weight=0)
scenes_text_frame.grid_rowconfigure(3, weight=1)
scenes_text_frame.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(scenes_text_frame, text="Название части").grid(row=0, column=0, sticky="ew", pady=1)
entry_part_name = ctk.CTkEntry(scenes_text_frame, width=30)
entry_part_name.grid(row=1, column=0, sticky="ew", pady=2)
ctk.CTkLabel(scenes_text_frame, text="Список сцен").grid(row=2, column=0, sticky="ew", pady=1)
#scenes_text = ctk.CTkTextbox(scenes_text_frame)
#scenes_text.grid(row=3, column=0, sticky="nsew")

scenes_dynamic_container = ctk.CTkFrame(scenes_text_frame)
scenes_dynamic_container.grid(row=2, column=0, sticky="nsew")
scenes_dynamic_container.grid_columnconfigure(0, weight=1)

btn_add_scene = ctk.CTkButton(scenes_text_frame, text="Добавить сцену", command=add_scene_field)
btn_add_scene.grid(row=5, column=0 )
btn_add_part = ctk.CTkButton(scenes_text_frame, text="Созадть часть", command=add_scenes)
btn_add_part.grid(row=6, column=0, pady = 2)
btn_dell_part = ctk.CTkButton(scenes_text_frame, text="Удалить часть", command=dell_scenes)
btn_dell_part.grid(row=7, column=0, pady = 2)


scenes_frame.grid_remove()
plot_frame.grid_remove()

refresh_list()
refresh_chapters()
refresh_scines_list()

def on_close():
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    save_all()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
