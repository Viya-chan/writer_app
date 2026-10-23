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
btn_x = []
is_dirty = False
selected_character_index = None
selected_chapter_index = None


# ----- Логика ------
#------Персонажи -------
def refresh_list():
    for widget in listbox_characters.winfo_children():
        widget.destroy()
    for index, ch in enumerate(characters):
        btn = ctk.CTkButton(listbox_characters, text = ch["name"], command = lambda i = index : on_select_character(i))
        btn.pack(fill="x", pady=2)

def on_select_character(index):
        global selected_character_index
        selected_character_index = index
        ch = characters[index]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, ch["name"])
        entry_appearance.delete(0, tk.END)
        entry_appearance.insert(0, ch["appearance"])
        entry_character.delete(0, tk.END)
        entry_character.insert(0, ch["character"])

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
    global selected_character_index
    if selected_character_index is None:
        win = ctk.CTkToplevel(root)
        win.geometry("350x150")
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="Вы не выбрали персонажа").pack(pady=20)
        def ok():
            win.destroy()
        btn_ok = ctk.CTkButton(win, text="Ok", command=ok).pack(padx=20)
        return
    del characters[selected_character_index]
    selected_character_index = None
    entry_name.delete(0, tk.END)
    entry_character.delete(0, tk.END)
    entry_appearance.delete(0, tk.END)

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

def clear_character():
    global selected_character_index
    selected_character_index = None
    entry_name.delete(0, tk.END)
    entry_character.delete(0, tk.END)
    entry_appearance.delete(0, tk.END)

def save_changes_charakter():
    global selected_character_index
    if selected_character_index is None:
        win = ctk.CTkToplevel(root)
        win.geometry("350x150")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="Вы не выбрали персонажа").pack(pady=20)
        def ok():
            win.destroy()
        btn_ok = ctk.CTkButton(win, text="Ok", command=ok).pack(padx=20)
        return
    characters[selected_character_index]["name"] = entry_name.get().strip()
    characters[selected_character_index]["appearance"] = entry_appearance.get().strip()
    characters[selected_character_index]["character"] = entry_character.get().strip()
    refresh_list()
    save_all()
#-------- Фунции глав
def refresh_chapters():
    for widget in listbox_chapters.winfo_children():
        widget.destroy()
    for index, ch in enumerate(chapters):
        btn = ctk.CTkButton(listbox_chapters, text=ch["title"], command = lambda i = index: on_select_chapter(i))
        btn.pack(fill="x", pady=2)

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
    global selected_chapter_index
    if selected_chapter_index is None:
        win = ctk.CTkToplevel(root)
        win.geometry("350x150")
        win.attributes("-topmost", True)
    
        ctk.CTkLabel(win, text="Вы не выбрали главу").pack(pady=20)
        def ok():
            win.destroy()
        btn_ok = ctk.CTkButton(win, text="Ok", command=ok).pack(padx=20)
        return    
    del chapters[selected_chapter_index]

    entry_chapter_title.delete(0, tk.END)
    status_var.set("Черновик")
    text_chapter.delete("1.0", tk.END)

    refresh_chapters()
    save_all()

def on_select_chapter(index):
    global selected_chapter_index
    selected_chapter_index = index

    ch = chapters[index]

    entry_chapter_title.delete(0, tk.END)
    entry_chapter_title.insert(0, ch["title"])

    status_var.set(ch["status"])

    text_chapter.delete("1.0", tk.END)
    text_chapter.insert("1.0", ch["text"])

def clear_chapter():
    entry_chapter_title.delete(0, tk.END)
    text_chapter.delete("1.0", tk.END)
    status_var.set("Черновик")

def save_changes_chapter():
    global selected_chapter_index
    if selected_chapter_index is None:
        win = ctk.CTkToplevel(root)
        win.geometry("350x150")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="Вы не выбрали персонажа").pack(pady=20)
        def ok():
            win.destroy()
        btn_ok = ctk.CTkButton(win, text="Ok", command=ok).pack(padx=20)
        return
    chapters[selected_chapter_index]["title"]= entry_chapter_title.get().strip()
    chapters[selected_chapter_index]["status"]=status_var.get()
    chapters[selected_chapter_index]["text"]=text_chapter.get("1.0", tk.END).strip()
    refresh_chapters()
    save_all()



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
    clear_scene_fields()
    refresh_scines_list()
    save_all()

def dell_scenes():
    selected = scenes_list.curselection()
    if not selected:
        return
    del parts [selected[0]]
    entry_part_name.delete(0, tk.END)
    refresh_scines_list()
    clear_scene_fields()
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
        curent_row=len(scene_fields)
        
        field = ctk.CTkEntry(scenes_dynamic_container, width=30)
        field.grid(row=curent_row, column=0, sticky="ew", pady=2)
        field.insert(0, scene_text)
        field.bind('<KeyRelease>', mark_as_dirty)
        scene_fields.append(field)

        btn_delete = ctk.CTkButton (
            scenes_dynamic_container, 
            text="X", width=30, fg_color="red", hover_color="darkred") 
        btn_delete.configure(command=lambda f = field, b = btn_delete: delete_field(f,b))
        btn_delete.grid(row=curent_row, column=1, padx=5, pady=2)
        btn_x.append(btn_delete)


#-------Функции сцен--------
def add_scene_field():
    field = ctk.CTkEntry(scenes_dynamic_container, width=250)
    field.grid(row=len(scene_fields), column=0, sticky="ew", pady=2)
    btn_delete = ctk.CTkButton(scenes_dynamic_container, text="X", width=30, fg_color="red", hover_color="darkred", command=lambda: delete_field(field, btn_delete))
    btn_delete.grid(row=len(scene_fields), column=1, padx=5, pady=2)
    scene_fields.append(field)
    btn_x.append(btn_delete)
    field.bind('<KeyRelease>', mark_as_dirty)


def delete_field(field_to_delete, btn_to_delet):
    field_to_delete.destroy()
    btn_to_delet.destroy()
    if field_to_delete in scene_fields:
        scene_fields.remove(field_to_delete)
    if btn_to_delet in btn_x:
        btn_x.remove(btn_to_delet)

def save_current_part():
    selected = scenes_list.curselection()
    if selected:
        pa = parts[selected[0]]
        pa["part_name"] = entry_part_name.get().strip()
        pa["scenes"] = get_scenes()


def get_scenes():
    scenes = []
    for field in scene_fields:
        text = field.get().strip()
        scenes.append(text)
    return scenes

def clear_scene_fields():
    for field in scene_fields:
        field.destroy()
    for btn_delete in btn_x:
        btn_delete.destroy()
    scene_fields.clear()
    btn_x.clear()

def clear_scene():
    clear_scene_fields()
    entry_part_name.delete(0, tk.END)
    scenes_list.selection_clear(0, tk.END)

def save_changes():
    selected = scenes_list.curselection()
    if not selected:
        print("Выберите часть из списка")
        return
    pa = parts[selected[0]]
    pa["part_name"] = entry_part_name.get().strip()
    pa["scenes"] = get_scenes()

    refresh_scines_list()
    save_all()

    global is_dirty
    is_dirty = False
    print("Изменения сохранены")

def mark_as_dirty(event):
    global is_dirty
    is_dirty = True

def ask_save_changes(action_callback):
    global is_dirty
    if not is_dirty:
        action_callback()
        return
    win = ctk.CTkToplevel(root)
    win.title("Внимание")
    win.geometry("350x150")
    win.attributes("-topmost", True)
    ctk.CTkLabel(win, text="Вы не сохранили изменения!\nВсе равно продолжить?").pack(pady=20)
    #кнопака да(продоложить)
    def confirm():
        global is_dirty
        is_dirty = False
        win.deiconify()
        action_callback()# Выполняем то что хотели 

    def cancel():
        win.destroy()

    ctk.CTkButton(win, text="Да", command=confirm, fg_color="red").pack(side= "left", padx=20)
    ctk.CTkButton(win, text="Отмена", command=cancel).pack(side="right", padx=20)
    win.grab_set()


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

#-----------Список персонажей-------
listbox_characters = ctk.CTkScrollableFrame(characters_frame, width=200)
listbox_characters.grid(row =0, column=0, rowspan=8, sticky="nsew")

panel = ctk.CTkFrame(characters_frame)
panel.grid_columnconfigure(0, weight=1)
panel.grid_rowconfigure(0, weight=0)
panel.grid_rowconfigure(1, weight=0)     
panel.grid(row = 0, column = 1, sticky = "nsew")

#--------Средняя часть у персонажей

ctk.CTkLabel(panel, text="Имя").grid(row = 0, column = 0, pady=(10, 0))
entry_name = ctk.CTkEntry(panel, width=30)
entry_name.grid(row = 1, column = 0, sticky = "ew", padx = 10)

ctk.CTkLabel(panel, text="Характер").grid(row = 2, column = 0, pady=(10, 0))
entry_character = ctk.CTkEntry(panel, width=30)
entry_character.grid(row = 3, column = 0, sticky = "ew", padx = 10)

ctk.CTkLabel(panel, text="Внешность").grid(row = 4, column = 0, pady=(10, 0))
entry_appearance = ctk.CTkEntry(panel, width=30)
entry_appearance.grid(row = 5, column = 0, sticky = "ew", padx = 10)

characters_buttons = ctk.CTkFrame(panel)
characters_buttons.grid(row=6, column=0, sticky="ew")
characters_buttons.grid_columnconfigure(0, weight=0)
characters_buttons.grid_columnconfigure(1, weight=0)

add_button = ctk.CTkButton(characters_buttons, text = "Добавить", command=add_character)
add_button.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = 5)

del_button = ctk.CTkButton(characters_buttons, text= "Удалить", command=del_character)
del_button.grid(row = 0, column = 1, sticky = "ew", padx = 10, pady = 5)

btn_clear_character = ctk.CTkButton(characters_buttons, text="Очистить", command=clear_character)
btn_clear_character.grid(row=1, column=0,  sticky = "ew", padx = 10, pady = 5)

btn_save_changes_character = ctk.CTkButton(characters_buttons, text="Сохранить изменения", command=save_changes_charakter)
btn_save_changes_character.grid(row=1, column=1,  sticky = "ew", padx = 10, pady = 5)
#----------Главы----------


chapters_frame = ctk.CTkFrame(content)
chapters_frame.grid(row = 0, column = 0, sticky="nsew")
chapters_frame.grid_columnconfigure(0, weight= 0)
chapters_frame.grid_columnconfigure( 1, weight= 1)
chapters_frame.grid_rowconfigure(0, weight=1)

# Список глав слева
listbox_chapters = ctk.CTkScrollableFrame(chapters_frame, width=200)
listbox_chapters.grid(row=0, column=0, sticky="nsew")

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

btn_clear_chapter = ctk.CTkButton(buttons_row, text="Очистить", command=clear_chapter)
btn_clear_chapter.grid(row=1, column=0, pady=1)

btn_save_changes_chapter = ctk.CTkButton(buttons_row, text="Сохранить изменения", command=save_changes_chapter)
btn_save_changes_chapter.grid(row= 1, column=1, pady=1)

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
entry_part_name.bind('<KeyRelease>', mark_as_dirty)
entry_part_name.grid(row=1, column=0, sticky="ew", pady=2)
ctk.CTkLabel(scenes_text_frame, text="Список сцен").grid(row=2, column=0, sticky="ew", pady=1)


scenes_dynamic_container = ctk.CTkFrame(scenes_text_frame)
scenes_dynamic_container.grid(row=3, column=0, sticky="nsew")
scenes_dynamic_container.grid_columnconfigure(0, weight=1)
scenes_dynamic_container.grid_columnconfigure(1, weight=0)

buttons_container = ctk.CTkFrame(scenes_text_frame)
buttons_container.grid(row=4, column=0)
buttons_container.grid_columnconfigure(0, weight=0)
buttons_container.grid_columnconfigure(1,weight=0)
buttons_container.grid_rowconfigure(0, weight=0)

btn_add_scene = ctk.CTkButton(buttons_container, text="Добавить сцену", command=add_scene_field)
btn_add_scene.grid(row=0, column=0 )
btn_add_part = ctk.CTkButton(buttons_container, text="Созадть часть", command=lambda: ask_save_changes(add_scenes))
btn_add_part.grid(row=1, column=0, pady = 2)

btn_save_changes = ctk.CTkButton(buttons_container, text="Сохранить изменения", command=save_changes)
btn_save_changes.grid(row=2, column=0, pady=2)

btn_dell_part = ctk.CTkButton(buttons_container, text="Удалить часть", command=dell_scenes)
btn_dell_part.grid(row=1, column=1, pady = 2)
btn_clear_scene = ctk.CTkButton(buttons_container, text="Очистить", command = clear_scene)
btn_clear_scene.grid(row =0, column=1, pady=2)


scenes_frame.grid_remove()
plot_frame.grid_remove()

refresh_list()
refresh_chapters()
refresh_scines_list()

def really_close():
    save_current_part()
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    save_all()
    root.destroy()

def on_close():
    ask_save_changes(really_close)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
