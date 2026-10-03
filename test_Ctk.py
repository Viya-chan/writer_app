import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Тест CustomTkinter")
root.geometry("400x300")

label = ctk.CTkLabel(root, text="Привет, CustomTkinter!")
label.pack(pady=20)

button = ctk.CTkButton(root, text="Нажми меня", command=lambda: print("Работает!"))
button.pack(pady=10)

root.mainloop()