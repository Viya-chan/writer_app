import customtkinter as ctk
import tkinter as tk
import data_meneger

class ChaptersTab:
    def __init__(self, parent):
        self.chapters = data_meneger.chapters
        self.selected_index = None

        