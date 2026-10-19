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

def save_all():
    data.save_data(all_data)

root = ctk.CTk()
root.title("Моя программа")
root.geometry("700x500")
root.grid_columnconfigure(0, weight=0) #первый столбик не рстягивается
root.grid_columnconfigure(1, weight=1) #второй столбик рястягивается
root.grid_rowconfigure(0, weight=1) #строка растягивается

content = ctk.CTkFrame(root, fg_color="transparent")
content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(0, weight=1)
content.grid(row = 0, column = 1, sticky = "nsew")

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
#ctk.CTkLabel(scenes_text_frame, text="Список сцен").grid(row=2, column=0, sticky="ew", pady=1)
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
#plot_frame.grid_remove()



refresh_scines_list()

def on_close():
    plot["idea"] = idea_text.get("1.0", tk.END).strip()
    save_all()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()