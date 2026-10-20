import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Моя программа")
root.geometry("700x500")
root.grid_columnconfigure(0, weight=1)



root.mainloop()


