
import tkinter as tk
import json
import os

DATA_FILE = "data.json"

#----- Слой данных-------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("characters", [])
def save_data(characters):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"characters": characters}, f, ensure_ascii=False, indent=2)

#------ Данные и память ------
characters = load_data()

# ----- Логика ------
def refresh_list():
    listbox.delete(0, tk.END)
    for ch in characters:
        listbox.insert(tk.END, ch["name"])

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
    save_data(characters)

def del_character():
    selected = listbox.curselection()
    if not selected:
        return
    del characters[selected[0]]
    refresh_list()
    save_data(characters)

def del_all():
    listbox.delete(0, tk.END)
    refresh_list()
    save_data(characters)

def on_double_click(event):
    index = listbox.nearest(event.y)
    listbox.delete(index)
    refresh_list()
    save_data(characters)

def on_select(event):
    selected = listbox.curselection()
    if not selected:
        return
    ch = characters[selected[0]]
    entry_name.delete(0, tk.END)
    entry_name.insert(0, ch["name"])
    entry_character.delete(0, tk.END)
    entry_character.insert(0, ch["character"])
    entry_appearance.delete(0, tk.END)
    entry_appearance.insert(0, ch["appearance"])

# ------ Интерфейс ------ 
        
root = tk.Tk()
root.title("Моя программа")
root.geometry("700x500")

sidebar = tk.Frame(root, width=150, bg = "lightgray")
sidebar.pack(side="left", fill="y")

btn1 = tk.Button(sidebar, text="Персонажи")
btn1.pack(padx=5, pady=5, fill="x")

btn2 = tk.Button(sidebar, text="Главы")
btn2.pack(padx=5, pady=5, fill= "x")

btn3 = tk.Button(sidebar, text="Сюжет")
btn3.pack(padx=5, pady=5, fill="x")

content = tk.Frame(root)
content.pack(side="left", fill="both", expand=True)

characters_frame = tk.Frame(content)
characters_frame.pack(fill="both", expand=True)

listbox = tk.Listbox(characters_frame, width=30)
listbox.pack(side="left", fill="both", expand=True)
listbox.bind("<<ListboxSelect>>", on_select)


panel = tk.Frame(characters_frame)
panel.pack(side="right", fill="y", padx=10, pady=10)

tk.Label(panel, text="Имя").pack(anchor="w", pady=(10, 0))
entry_name = tk.Entry(panel, width=30)
entry_name.pack()

tk.Label(panel, text="Характер").pack(anchor="w", pady=(10, 0))
entry_character = tk.Entry(panel, width=30)
entry_character.pack()

tk.Label(panel, text="Внешность").pack(anchor="w", pady=(10, 0))
entry_appearance = tk.Entry(panel, width=30)
entry_appearance.pack()

add_button = tk.Button(panel, text = "Добавить", command=add_character)
add_button.pack()

del_button = tk.Button(panel, text= "Удалить", command=del_character)
del_button.pack()

del_all_button = tk.Button(panel, text= "Удалить все", command= del_all)
del_all_button.pack()

listbox.bind("<Double-Button-1>", on_double_click)



root.mainloop()
