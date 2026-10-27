import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

import data_meneger
from data_meneger import characters, chapters, plot, parts, save_all, scene_fields, btn_x, selected_chapter_index, selected_character_index, selected_scenes_index
import characters_tab
import chapters_tab

#------Проверка на дубликаты 
def is_duplicate(data_list, key_to_chek, new_value, current_index=None):
    for index, item in enumerate(data_list):
        if item[key_to_chek] == new_value and index != current_index:
            return True
    return False

#------Сообщение с ошибкой
def show_error(message):
    win = ctk.CTkToplevel(root)
    win.geometry("300x150")
    win.attributes("-topmost", True)
    ctk.CTkLabel(win, text=message).pack()
    ctk.CTkButton(win, text="Ok", command=win.destroy).pack()
# -------Предупреждение об удалении 
def ask_confirm(message, action_callback):
    win = ctk.CTkToplevel(root)
    win.title("Подтверждение")
    win.geometry("350x150")
    win.attributes("-topmost", True)

    ctk.CTkLabel(win, text=message).pack(pady=20)

    def confirm():
        win.destroy()
        action_callback()
    def cancel():
        win.destroy()
    ctk.CTkButton(win, text="Да, удалить", command=confirm, fg_color="red").pack(side="left", padx=20)
    ctk.CTkButton(win, text="Отмена", command=cancel).pack(side="right", padx=20)
#------Персонажи -------


#-------- Фунции глав

#------Функции сюжет--------
def show_idea():
    scenes_frame.grid_remove()
    idea_frame.grid()

def show_scenes():
    idea_frame.grid_remove()
    scenes_frame.grid()

def save_idea():
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    data_meneger.is_dirty = False
    save_all()

def refresh_scenes_list():
    for widget in scenes_list.winfo_children():
        widget.destroy()
    for index, pa in enumerate(parts):
        btn = ctk.CTkButton(scenes_list, text=pa["part_name"], command=lambda i = index: on_select_scenes(i))
        btn.pack(fill="x", pady=2)

def add_scenes():
    part_name = entry_part_name.get().strip()
    part_scenes = get_scenes()
    if part_name == "":
        show_error("Вы не ввели название")
        return
    if is_duplicate(parts, "part_name", part_name):
        show_error("Такое название уже есть")
        return
    parts.append({
        "part_name": part_name,
        "scenes": part_scenes
    })
    entry_part_name.delete(0, tk.END)
    clear_scene_fields()
    refresh_scenes_list()
    save_all()

def dell_scenes():
    if data_meneger.selected_scenes_index is None:
        show_error("Вы не выбрали часть")
        return
    def do_delete():
        del parts [data_meneger.selected_scenes_index]
        selected_scenes_index = None
        entry_part_name.delete(0, tk.END)
        refresh_scenes_list()
        clear_scene_fields()
        save_all()
    ask_confirm("Вы точно хотите удалить часть?", do_delete)

def on_select_scenes(index):
    data_meneger.selected_scenes_index = index
    pa = parts[index]
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
    if data_meneger.selected_scenes_index is None:
        return
    pa = parts[data_meneger.selected_scenes_index]
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
    data_meneger.selected_scenes_index = None

def save_changes():
    if data_meneger.selected_scenes_index is None:
        return
    pa = parts[data_meneger.selected_scenes_index]
    pa["part_name"] = entry_part_name.get().strip()
    pa["scenes"] = get_scenes()

    refresh_scenes_list()
    save_all()

    data_meneger.is_dirty = False
    print("Изменения сохранены")

def mark_as_dirty(event):
    data_meneger.is_dirty = True

def ask_save_changes(action_callback):
    if not data_meneger.is_dirty:
        action_callback()
        return
    win = ctk.CTkToplevel(root)
    win.title("Внимание")
    win.geometry("350x150")
    win.attributes("-topmost", True)
    ctk.CTkLabel(win, text="Вы не сохранили изменения!\nВсе равно продолжить?").pack(pady=20)
    #кнопака да(продоложить)
    def confirm():
        data_meneger.is_dirty = False
        win.deiconify()
        action_callback()# Выполняем то что хотели 

    def cancel():
        win.destroy()

    ctk.CTkButton(win, text="Да", command=confirm, fg_color="red").pack(side= "left", padx=20)
    ctk.CTkButton(win, text="Отмена", command=cancel).pack(side="right", padx=20)
    win.grab_set()


#------Фунции в боковом меню--------
def show_caracters ():
    chapters_frame.frame.grid_remove()
    plot_frame.grid_remove()
    character_frame.frame.grid()

def show_chapters():
    character_frame.frame.grid_remove()
    plot_frame.grid_remove()
    chapters_frame.frame.grid()

def show_plot():
    chapters_frame.frame.grid_remove()
    character_frame.frame.grid_remove()
    plot_frame.grid()
    

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
content.grid(row = 0, column = 1, sticky = "nsew")

#--------Персонажи----------------

character_frame = characters_tab.CharactersTab(content)
chapters_frame = chapters_tab.ChaptersTab(content)
#----------Главы----------

content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(0, weight=1)



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
idea_text.bind("<KeyRelease>", mark_as_dirty)
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

scenes_list = ctk.CTkScrollableFrame(scenes_frame, width=200)
scenes_list.grid(row=0, column=0, sticky="ns")


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
btn_add_part = ctk.CTkButton(buttons_container, text="Созадть часть", command=add_scenes)
btn_add_part.grid(row=1, column=0, pady = 2)

btn_save_changes = ctk.CTkButton(buttons_container, text="Сохранить изменения", command=save_changes)
btn_save_changes.grid(row=2, column=0, pady=2)

btn_dell_part = ctk.CTkButton(buttons_container, text="Удалить часть", command=dell_scenes)
btn_dell_part.grid(row=1, column=1, pady = 2)
btn_clear_scene = ctk.CTkButton(buttons_container, text="Очистить", command = clear_scene)
btn_clear_scene.grid(row =0, column=1, pady=2)


scenes_frame.grid_remove()
plot_frame.grid_remove()


refresh_scenes_list()

def really_close():
    save_current_part()
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    save_all()
    root.destroy()

def on_close():
    ask_save_changes(really_close)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
