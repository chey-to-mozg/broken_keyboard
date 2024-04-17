import tkinter as tk
from tkinter import font, ttk

from src import common

ROOT = tk.Tk()

BackgroundColor = '#F0F2F8'
PanelBackgroundColor = '#FFFFFF'
BlueTextColor = '#1E21AA'
GreenTextColor = '#00B27F'
RedTextColor = '#D60020'
GrayTextColor = '#808080'

ButtonsFont = font.Font(family='Proxima Nova', size=12, weight='bold')
MainInfoFont = font.Font(family='Proxima Nova', size=12)
MainInfoFontBold = font.Font(family='Proxima Nova', size=12, weight='bold')
MainInfoFontBig = font.Font(family='Proxima Nova', size=20)
MainInfoFontBigBold = font.Font(family='Proxima Nova', size=28, weight='bold')
AdditionalInfoFont = font.Font(family='Proxima Nova', size=10)
LettersFont = font.Font(family='Proxima Nova', size=28, weight='bold')
TimerFont = font.Font(family='Proxima Nova', size=40, weight='bold')
ResultHeaderFont = font.Font(family='Proxima Nova', size=20, weight='bold')
ResultWordFont = font.Font(family='Proxima Nova', size=16)
StatsFont = font.Font(family='Proxima Nova', size=14)
StatsFontBold = font.Font(family='Proxima Nova', size=14, weight='bold')

text_entity_image = tk.PhotoImage(file=common.get_image_path('text_entity'))
text_entity_style = ttk.Style()
text_entity_style.image = text_entity_image
text_entity_style.element_create("RoundedFrame", "image", text_entity_image, border=16, sticky="nsew")
text_entity_style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
