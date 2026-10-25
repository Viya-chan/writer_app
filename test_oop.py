import tkinter as tk
import customtkinter as ctk

class CharacterTab:
    def __init__(self, parent):
        #создаем фрейм(коробку) для этой вкладки 
        self.characters=[]
        self.frame=ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        self.listbox_frame = ctk.CTkScrollableFrame(self.frame)
        self.listbox_frame.pack(pady=20)

        #Создаем кнопку внутри класса 
        self.btn = ctk.CTkButton(self.frame, text = "Я кнопка из класса", command=self.add_character)
        self.btn.pack(pady=20)
        self.entry = ctk.CTkEntry(self.frame)
        self.entry.pack(pady=20)

    def refresh_list(self):
        for widget in self.listbox_frame.winfo_children():
            widget.destroy()
        for ch in self.characters:
            self.btn = ctk.CTkButton(self.listbox_frame, text=ch)
            self.btn.pack(pady=10)
    
    #Метод(фугкция внутри класса), который срабатывает при нажатии 
    def add_character(self):
        self.entry_name = self.entry.get().strip()
        if self.entry_name == "":
            print("Вы не ввелия имя")
            return
        self.characters.append(self.entry_name)
        self.entry.delete(0, tk.END)
        print("Добавлено", self.entry_name)
        self.refresh_list()

root = ctk.CTk()
root.geometry("400x300")
#Создаем объеккт(экземпляр) нашего класса 
tab = CharacterTab(root)

root.mainloop()