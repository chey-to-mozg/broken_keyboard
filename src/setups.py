import tkinter as tk
from tkinter import font, ttk
from src import common

ROOT = tk.Tk()

BackgroundColor = '#F0F2F8'
PanelBackgroundColor = '#FFFFFF'
BlueTextColor = 'blue'

ButtonsFont = font.Font(family='Courier', size=12, weight='bold')
MainInfoFont = font.Font(family='Courier', size=12)
MainInfoFontBig = font.Font(family='Courier', size=20)
MainInfoFontBigBold = font.Font(family='Courier', size=20, weight='bold')
AdditionalInfoFont = font.Font(family='Courier', size=9)
LettersFont = font.Font(family='Courier', size=28, weight='bold')
TimerFont = font.Font(family='Courier', size=40, weight='bold')

text_entity_image = tk.PhotoImage(file=common.get_image_path('text_entity'))
text_entity_style = ttk.Style()
text_entity_style.image = text_entity_image
text_entity_style.element_create("RoundedFrame", "image", text_entity_image, border=16, sticky="nsew")
text_entity_style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])

results_entity_image = tk.PhotoImage(file=common.get_image_path('results_body'))
results_entity_style = ttk.Style()
results_entity_style.image = results_entity_image
results_entity_style.element_create("ResultsBody", "image", results_entity_image, border=16, sticky="nsew")
results_entity_style.layout("ResultsBody", [("ResultsBody", {"sticky": "nsew"})])
