import customtkinter as ctk
import tkinter as tk
import data_meneger


class CharactersTab:
    def __init__(self, parent):
        #Данные
        self.characters = data_meneger.characters
        self.selected_index = None

        #Интерфейс
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.listbox_frame = ctk.CTkScrollableFrame(self.frame, width=200)
        self.listbox_frame.grid(row =0, column=0, rowspan=8, sticky="nsew")

        self.panel = ctk.CTkFrame(self.frame)
        #self.panel.grid_rowconfigure(0, weight=0)
        #self.panel.grid_rowconfigure(1, weight=0)     
        self.panel.grid(row = 0, column = 1, sticky = "nsew")
        self.panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.panel, text="Имя").grid(row = 0, column = 0, pady=(10, 0))
        self.entry_name = ctk.CTkEntry(self.panel, width=30)
        #self.entry_name.bind("<KeyRelease>", mark_as_dirty)
        self.entry_name.grid(row = 1, column = 0, sticky = "ew", padx = 10)

        ctk.CTkLabel(self.panel, text="Характер").grid(row = 2, column = 0, pady=(10, 0))
        self.entry_character = ctk.CTkEntry(self.panel, width=30)
        #self.entry_character.bind("<KeyRelease>", mark_as_dirty)
        self.entry_character.grid(row = 3, column = 0, sticky = "ew", padx = 10)

        ctk.CTkLabel(self.panel, text="Внешность").grid(row = 4, column = 0, pady=(10, 0))
        self.entry_appearance = ctk.CTkEntry(self.panel, width=30)
        #self.entry_appearance.bind("<KeyRelease>", mark_as_dirty)
        self.entry_appearance.grid(row = 5, column = 0, sticky = "ew", padx = 10)

        self.characters_buttons = ctk.CTkFrame(self.panel)
        self.characters_buttons.grid(row=6, column=0, sticky="ew")
        self.characters_buttons.grid_columnconfigure(0, weight=0)
        self.characters_buttons.grid_columnconfigure(1, weight=0)

        self.add_button = ctk.CTkButton(self.characters_buttons, text = "Добавить", command=self.add_character)
        self.add_button.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = 5)

        self.del_button = ctk.CTkButton(self.characters_buttons, text= "Удалить", command=self.dell_character)
        self.del_button.grid(row = 0, column = 1, sticky = "ew", padx = 10, pady = 5)

        self.btn_clear_character = ctk.CTkButton(self.characters_buttons, text="Очистить", command=self.clear_character)
        self.btn_clear_character.grid(row=1, column=0,  sticky = "ew", padx = 10, pady = 5)

        self.btn_save_changes_character = ctk.CTkButton(self.characters_buttons, text="Сохранить изменения", command=self.save_change)
        self.btn_save_changes_character.grid(row=1, column=1,  sticky = "ew", padx = 10, pady = 5)       

        self.refresh_list()


    def refresh_list(self):
        for widget in self.listbox_frame.winfo_children():
            widget.destroy()

        for index, ch in enumerate(self.characters):
            btn = ctk.CTkButton(
                self.listbox_frame, 
                text=ch["name"],
                command=lambda i=index: self.on_select(i)
            )
            btn.pack(fill="x", pady = 2)

    def on_select(self, index):
        self.selected_index = index
        ch = self.characters[index]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, ch["name"])
        self.entry_appearance.delete(0, tk.END)
        self.entry_appearance.insert(0, ch["appearance"])
        self.entry_character.delete(0, tk.END)
        self.entry_character.insert(0, ch["character"])

    def add_character(self):
        name = self.entry_name.get().strip()
        appearance = self.entry_appearance.get().strip()
        character = self.entry_character.get().strip()
        if name == "":
            print("Вы не ввели имя")
            return
        self.characters.append({
            "name": name,
            "appearance": appearance,
            "character": character
            })
        self.entry_name.delete(0, tk.END)
        self.entry_appearance.delete(0, tk.END)
        self.entry_character.delete(0, tk.END)
        self.refresh_list()
<<<<<<< HEAD
        data_meneger.save_all()
=======
>>>>>>> 345339fdf4bbe800f72af37023b544000e6af6e8

        

    def dell_character(self):
        if self.selected_index is None:
            print("Вы не выбрали персонажа")
            return
        del self.characters[self.selected_index]
        self.selected_index = None
        self.entry_name.delete(0, tk.END)
        self.entry_character.delete(0, tk.END)
        self.entry_appearance.delete(0, tk.END)
        
        self.refresh_list()
<<<<<<< HEAD
        data_meneger.save_all()
=======
>>>>>>> 345339fdf4bbe800f72af37023b544000e6af6e8
        



    def save_change(self):
        if self.selected_index is None:
            print("Вы не выбрали персонажа")
            return
        self.characters[self.selected_index]["name"] = self.entry_name.get().strip()
        self.characters[self.selected_index]["appearance"] = self.entry_appearance.get().strip()
        self.characters[self.selected_index]["character"] = self.entry_character.get().strip()
        self.refresh_list()
<<<<<<< HEAD
        data_meneger.save_all()
=======
>>>>>>> 345339fdf4bbe800f72af37023b544000e6af6e8

    

    def clear_character(self):
        self.selected_index = None
        self.entry_character.delete(0, tk.END)
        self.entry_appearance.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)


