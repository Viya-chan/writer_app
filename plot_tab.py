import customtkinter as ctk
import tkinter as tk
import data_meneger

class PlotTab:
    def __init__(self, parent):
        self.plot = data_meneger.plot
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row = 0, column = 0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0)

        self.top_panel = ctk.CTkFrame(self.frame)
        self.top_panel.grid(row=0, column=0, sticky="ew", pady=2)
        self.top_panel.grid_columnconfigure(0, weight=0)
        self.top_panel.grid_columnconfigure(1, weight=0)
        self.top_panel.grid_rowconfigure(0, weight=0)

        self.btn_idea = ctk.CTkButton(self.top_panel, text= "Идея", command=self.show_idea)
        self.btn_idea.grid(row=0, column=0, padx=1)
        self.btn_scenes = ctk.CTkButton(self.top_panel, text= "Сцены", command=self.show_scenes)
        self.btn_scenes.grid(row=0, column=1, padx=1)

        self.idea_frame = ctk.CTkFrame(self.frame)
        self.idea_frame.grid(row = 1, column=0, sticky="nsew", pady=5)
        self.idea_frame.grid_columnconfigure(0, weight=1)
        self.idea_frame.grid_rowconfigure(0, weight=1)

        self.idea_text = ctk.CTkTextbox(self.idea_frame)
        #self.idea_text.bind("<KeyRelease>", mark_as_dirty)
        self.idea_text.grid(row=0, column=0, sticky="nsew")

        self.btn_idea_save = ctk.CTkButton(self.idea_frame, text = "Сохранить идею", command=self.save_idea)
        self.btn_idea_save.grid(row=2, column=0)

        self.idea_text.insert("1.0", self.plot.get("idea", ""))

    def show_idea(self):
        self.idea_frame.grid()

    def show_scenes(self):
        self.idea_frame.grid_remove()

    def save_idea(self):
        data_meneger.plot["idea"] = self.idea_text.get("1.0", tk.END).strip()
        data_meneger.save_all()