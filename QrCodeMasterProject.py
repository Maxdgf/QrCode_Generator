import customtkinter as ctk
import segno
import os
import sys
import time
from random import randint
import platform
import subprocess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from PIL import Image
         
ctk.set_default_color_theme("green") 

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = ""

#Window setup----------------------------------------------------------------------------------
        self.title("Генератор QR-кодов")    
        self.geometry("800x600")
        self.icon_path = os.path.join(os.path.dirname(__file__), 'qrCodeLogo.ico')
        self.iconbitmap(self.icon_path)
        self.resizable(0, 0)

#Window setup----------------------------------------------------------------------------------

#UI area-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.widgetFrame = ctk.CTkFrame(self, border_color="#1E90FF", border_width=5)
        #self.widgetFrame.pack_propagate(True)
        self.theme = "dark"
        ctk.set_appearance_mode(self.theme)

        self.labelNameFrame = ctk.CTkFrame(self, border_color="#1E90FF", border_width=5)
        self.labelName = ctk.CTkLabel(self.labelNameFrame, text="Генератор QR-кодов", text_color="#00BFFF", font=("Arial", 40))
        self.labelName.pack(side="left", padx=5)
        self.labelIcon = ctk.CTkImage(light_image=Image.open(self.resource_path("basic_qrcode.png")), dark_image=Image.open(self.resource_path("basic_qrcode.png")), size=(50, 50))
        self.labelImg = ctk.CTkLabel(self.labelNameFrame, image=self.labelIcon, text="")
        self.labelImg.pack(side="left", padx=5, pady=5)
        self.labelNameFrame.pack(anchor="ne", padx=5, pady=10)

        self.switchVar = ctk.StringVar(value="off")
        self.switchTheme = ctk.CTkSwitch(self, text="темная/светлая тема", fg_color="#1E90FF", command=self.switch_theme, variable=self.switchVar, onvalue="on", offvalue="off")
        self.switchTheme.place(x=0, y=0)

        self.urlFrame = ctk.CTkFrame(self.widgetFrame)
        self.NameString = ctk.CTkEntry(self.urlFrame, placeholder_text="введите ссылку", border_color="#00BBFB", border_width=3)
        self.NameString.pack(side="left", fill="x", expand=True)   
        self.btnPaste = ctk.CTkButton(self.urlFrame, text="вставить", fg_color="#1E90FF", hover_color="#00BFFF", command=self.paste_text)
        self.btnPaste.pack(side="right", fill="x", padx=2)
        self.urlFrame.pack(pady=10, fill="x", padx=10)

        self.filenameString = ctk.CTkEntry(self.widgetFrame, width=500, placeholder_text="введите имя сохраняемого файла", border_color="#00BBFB", border_width=3)
        self.filenameString.pack(fill="x", padx="10")

        self.filePathFrame = ctk.CTkFrame(self.widgetFrame)
        self.pathLabael = ctk.CTkLabel(self.filePathFrame, text="Путь сохранения:", text_color="#00BFFF", font=("Arial", 15))
        self.pathLabael.pack(side="left", pady=5, padx=5)
        self.btnSelectPath = ctk.CTkButton(self.filePathFrame, text="выбрать", fg_color="#1E90FF", hover_color="#00BFFF", command=self.open_filedialog)
        self.btnSelectPath.pack(anchor="e", pady=5, padx=5)
        self.filePathFrame.pack(pady=10, padx=10, fill="x")

        self.actionAreaFrame = ctk.CTkFrame(self.widgetFrame, border_color="#1E90FF", border_width=5)

        self.colorfulQRParametersFrame = ctk.CTkScrollableFrame(self.actionAreaFrame)

        self.qrCodeViewFrame = ctk.CTkFrame(self.actionAreaFrame)

        self.nameLabel = ctk.CTkLabel(self.colorfulQRParametersFrame, text="Параметры📋", font=("Arial", 15))
        self.nameLabel.pack(anchor="center")

        self.maskFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.descLabel5 = ctk.CTkLabel(self.maskFrame, text="паттерны узора:", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel5.pack(side="left", padx=2)
        self.selectMask = ctk.CTkComboBox(self.maskFrame, values=["паттерн 000", "паттерн 001", "паттерн 010", "паттерн 011", "паттерн 100", "паттерн 101", "паттерн 110", "паттерн 111"], border_color="#00BFFF", border_width=3, button_color="#1E90FF", button_hover_color="#00BFFF", dropdown_fg_color="#1E90FF", dropdown_hover_color="#00BFFF")
        self.selectMask.pack(side="left", padx=2)
        self.maskFrame.pack(pady=10, anchor="ne")

        self.sizeFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.sizeLabeldescription = ctk.CTkLabel(self.sizeFrame, text="размер qr-кода: ", text_color="#00BFFF", font=("Arial", 15))
        self.sizeLabeldescription.pack(side="left")
        self.slider = ctk.CTkSlider(self.sizeFrame, from_=0, to=50, orientation="horizontal",  button_color="#1E90FF", button_hover_color="#00BBFB", command=self.slider_event)
        self.slider.pack(side="left")
        self.slider.set(10)
        self.slValue = self.slider.get()
        self.sizeLabel = ctk.CTkLabel(self.sizeFrame, text="0")
        self.sizeLabel.pack(side="left")
        self.sizeFrame.pack(pady=10, anchor="ne")
        int(self.slValue)
        self.sizeLabel.configure(text=f"{int(self.slValue)} ед.")

        self.borderFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.borderLabeldescription = ctk.CTkLabel(self.borderFrame, text="ширина границы: ", text_color="#00BFFF", font=("Arial", 15))
        self.borderLabeldescription.pack(side="left")
        self.slider2 = ctk.CTkSlider(self.borderFrame, from_=0, to=50, orientation="horizontal", button_color="#1E90FF", button_hover_color="#00BBFB", command=self.slider_event2)
        self.slider2.pack(side="left")
        self.slider2.set(5)
        self.slValue2 = self.slider2.get()
        self.borderLabel = ctk.CTkLabel(self.borderFrame, text="0")
        self.borderLabel.pack(side="left")
        self.borderFrame.pack(pady=10, anchor="ne")
        int(self.slValue2)
        self.borderLabel.configure(text=f"{self.slValue2} ед.")

        self.fillcFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.descLabel = ctk.CTkLabel(self.fillcFrame, text="цвет узора:", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel.pack(side="left", padx=2)
        self.colorLabel = ctk.CTkLabel(self.fillcFrame, width=80, bg_color="white", text="❌")
        self.colorLabel.pack(side="left", padx=2)
        self.btnSelectColor = ctk.CTkButton(self.fillcFrame, text="выбрать", fg_color="#1E90FF", hover_color="#00BFFF", command=self.fill_colorEvent)
        self.btnSelectColor.pack(side="left", padx=2)
        self.fillcFrame.pack(pady=10, anchor="ne")
        
        self.backcFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.descLabel2 = ctk.CTkLabel(self.backcFrame, text="задний фон:", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel2.pack(side="left", padx=2)
        self.colorLabel2 = ctk.CTkLabel(self.backcFrame, width=80, bg_color="white", text="❌")
        self.colorLabel2.pack(side="left", padx=2)
        self.btnSelectColor2 = ctk.CTkButton(self.backcFrame, text="выбрать", fg_color="#1E90FF", hover_color="#00BFFF", command=self.back_colorEvent)
        self.btnSelectColor2.pack(side="left", padx=2)
        self.backcFrame.pack(pady=10, anchor="ne")

        self.borderQRFrame = ctk.CTkFrame(self.colorfulQRParametersFrame)
        self.descLabel5 = ctk.CTkLabel(self.borderQRFrame, text="цвет границы:", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel5.pack(side="left", padx=2)
        self.colorLabel5 = ctk.CTkLabel(self.borderQRFrame, width=80, bg_color="white", text="❌")
        self.colorLabel5.pack(side="left", padx=2)
        self.btnSelectColor5 = ctk.CTkButton(self.borderQRFrame, text="выбрать", fg_color="#1E90FF", hover_color="#00BFFF", command=self.border_colorEvent)
        self.btnSelectColor5.pack(side="left", padx=2)
        self.borderQRFrame.pack(pady=10, anchor="ne")
        
        self.qrCode = ctk.CTkImage(light_image=Image.open(self.resource_path("canvas.png")), dark_image=Image.open(self.resource_path("canvas.png")), size=(200, 200))
        self.qrCodeLabel = ctk.CTkLabel(self.qrCodeViewFrame, image=self.qrCode, text="")
        self.qrCodeLabel.pack(expand=True)
        self.qrCaption = ctk.CTkLabel(self.qrCodeViewFrame, text="")
        self.qrCaption.pack()
        self.qrView = ctk.CTkButton(self.qrCodeViewFrame, text="Посмотреть", fg_color="#1E90FF", hover_color="#00BFFF", command=self.view_qr)
        self.qrView.pack(fill="x")

        self.qrCodeViewFrame.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        self.colorfulQRParametersFrame.pack(anchor="ne", fill="both", padx=10, pady=10, expand=True)

        self.btnStart = ctk.CTkButton(self.actionAreaFrame, width=425, height=100, text="Создать QR-код", fg_color="#1E90FF", hover_color="#00BFFF", command=self.create_qr_code)
        self.btnStart.pack(pady=10, anchor="ne", padx=10, side="bottom")

        self.actionAreaFrame.pack(fill="both", padx=10, expand=True, pady=10)

        self.widgetFrame.pack(expand=True, fill="both")
#UI area-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Functions area---------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)    
    
    def view_qr(self):
        if len(self.path) != 0:
            if platform.system() == "Windows":
                os.startfile(self.path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", self.path])
            else:
                subprocess.run(["xdg-open", self.path])
        else:
            messagebox.showwarning("Внимание", "QR-код еще не создан.")

    def fill_colorEvent(self):
        self.fillcolor = colorchooser.askcolor(title="Выберите цвет узора")
        if self.fillcolor[1] is not None:
            self.colorLabel.configure(fg_color=self.fillcolor[1], text="")

    def back_colorEvent(self):
        self.backcolor = colorchooser.askcolor(title="Выберите цвет заднего фона")
        if self.backcolor[1] is not None:
            self.colorLabel2.configure(fg_color=self.backcolor[1], text="")

    def border_colorEvent(self):
        self.bordercolor = colorchooser.askcolor(title="Выберите цвет границы")
        if self.bordercolor[1] is not None:
            self.colorLabel5.configure(fg_color=self.bordercolor[1], text="")

    def slider_event(self, value):
        self.num = int(value)
        self.sizeLabel.configure(text=f"{self.num} ед.")
        #print(value)

    def slider_event2(self, value):
        self.num2 = int(value)
        self.borderLabel.configure(text=f"{self.num2} ед.")
        #print(value)

    def switch_theme(self):
        #print("value:" + self.switchVar.get())
        self.value = self.switchVar.get()
        if self.value == "off":
            self.theme = "dark"
            ctk.set_appearance_mode(self.theme)
        elif self.value == "on":
            self.theme = "light"
            ctk.set_appearance_mode(self.theme)

    def open_filedialog(self):
        try:
            self.file_path = filedialog.askdirectory(title="Выберите путь")
            str(self.file_path)
            self.pathLabael.configure(text=f"Путь сохранения: {self.file_path}")
            if len(self.file_path) == 0:
                messagebox.showwarning("Внимание", "Необходимо указать куда будет сохраняться qr-код!")
                self.pathLabael.configure(text="Путь сохранения: неизвестен")
            #print(self.file_path)
        except:
            messagebox.showerror("Ошибка", "Путь не найден! Попробуйте еще раз.")

    #создание qr кода
    def create_qr_code(self):
        self.link = self.NameString.get()
        self.name = self.filenameString.get()
        if len(self.name) == 0:
            self.name = f"untitled{randint(0, 1000)}"
        self.size = self.slider.get()
        self.border = self.slider2.get()
        self.mask = self.selectMask.get()
    
        self.maskValue = 0
        match self.mask:
            case "паттерн 000":
                self.maskValue = 0
            
            case "паттерн 001":
                self.maskValue = 1

            case "паттерн 010":
                self.maskValue = 2

            case "паттерн 011":
                self.maskValue = 3

            case "паттерн 100":
                self.maskValue = 4

            case "паттерн 101":
                self.maskValue = 5

            case "паттерн 110":
                self.maskValue = 6

            case "паттерн 111":
                self.maskValue = 7

        try:
            self.qr_code = segno.make(self.link, mask=self.maskValue)
            self.path = f"{self.file_path}/{self.name}.png"

            self.qr_code.save(self.path, scale=int(self.size), border=int(self.border), light=self.backcolor[1], dark=self.fillcolor[1], quiet_zone=self.bordercolor[1])

            self.image = Image.open(f"{self.path}")
            self.width, self.height = self.image.size
            self.qrCode = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(200, 200))
            self.qrCodeLabel.configure(image=self.qrCode)
            self.qrCaption.configure(text=f"{self.width}px x {self.height}px")

            if len(self.link) == 0:
                self.NameString.configure(border_color="#ffff00")
                messagebox.showwarning("Внимание", "Отсутствует ссылка на ресурс! QR-код невозможно прочесть.")
                time.sleep(0.5)
                self.NameString.configure(border_color="#00BBFB")
        except Exception as e:
            self.NameString.configure(border_color="#ff0000")
            self.filenameString.configure(border_color="#ff0000")
            self.filePathFrame.configure(border_color="#ff0000", border_width=3)

            self.colorfulQRParametersFrame.configure(border_color="#ff0000", border_width=5)
            #print(e)
            messagebox.showerror("Ошибка", "Пожалуйста, проверьте правильность и заполнение параметров и повторите генерацию еще раз.")
            time.sleep(0.5)
            self.colorfulQRParametersFrame.configure(border_width=0)
            self.NameString.configure(border_color="#00BBFB")
            self.filenameString.configure(border_color="#00BBFB")
            self.filePathFrame.configure(border_width=0)

    def paste_text(self):
        self.text = self.clipboard_get()
        self.NameString.insert("end", self.text)

#Functions area----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
             
if __name__ == "__main__":
    #запуск программы
    app = App()
    app.mainloop()  