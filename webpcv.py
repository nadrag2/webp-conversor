from tkinter import *
from tkinter.ttk import *
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
from PIL import Image
import keyboard
import os

root = TkinterDnD.Tk()
root.title("Webp Converter")
root.geometry("425x417+622+271")
root.resizable(False, False)
progress = StringVar()

#FUNÇÕES

def drop_inside_list_box(event):
    files = event.data
    if re.search(".webp", files):
        files_list = [f.strip() for f in files.split("webp")]
        del files_list[-1]
        for f in files_list:
            new_f = re.search("([A-Z]:.*)", f)
            print(new_f.group(0))
            listbox.insert("end", f"{new_f.group(0)}webp")
    if re.search(".png", files):
        files_list = [f.strip() for f in files.split("png")]
        del files_list[-1]
        for f in files_list:
            new_f = re.search("([A-Z]:.*)", f)
            print(new_f.group(0))
            listbox.insert("end", f"{new_f.group(0)}png")
        
def bt_convert():
    index = 0
    lbImg = listbox.get(0, 'end')
    amount = len(lbImg)
    ext = [".jpeg", ".png"]

    def check_file(file_name):
        for x in ext:
            if os.path.exists(f"{file_name}{x}"):
                return True

    for item in lbImg:
        im = Image.open(item)
        name_regex = re.search("(?<=\/)[^\/]*(?=\.)", im.filename)
        index += 1

        if check_file(name_regex.group()):
            continue

        if im.mode == "RGBA":
            im.save(f"{name_regex.group()}.png")
            progress.set(str(index)+"/"+str(amount))
            root.update_idletasks()
            continue

        im.save(f"{name_regex.group()}.jpeg")
        progress.set(str(index)+"/"+str(amount))
        root.update_idletasks()

def open_image(arg):
    img = Image.open(listbox.get(ACTIVE))
    img.show()

def bt_delete_all():
    listbox.delete("0", "end")
    progress.set("")

def key_press(arg):
    if keyboard.is_pressed('delete'):
        index = listbox.curselection()
        listbox.delete(index)


#WIDGETS

#CONFIGURANDO LISTBOX E BARRA DE SCROLL
lb_frame = Frame(root)

x_scrollbar = Scrollbar(lb_frame, orient=HORIZONTAL)
y_scrollbar = Scrollbar(lb_frame, orient=VERTICAL)

listbox = Listbox(lb_frame, selectmode=SINGLE, background="#252526", width=66, height=18, borderwidth=0, xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
listbox.drop_target_register(DND_FILES)

x_scrollbar.config(command=listbox.xview)
x_scrollbar.pack(side=BOTTOM, fill=X)

y_scrollbar.config(command=listbox.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)

lb_frame.pack()
listbox.pack()
#
progressLabel = Label(root, textvariable=progress)
progressLabel.place(y=315, x= 185)
#
button_comecar = Button(root, text="START", command=bt_convert, width=10)

button_comecar.place(y=350, x=84)
#
button_deletar = Button(root, text="DELETE ALL", command=bt_delete_all, width=10)
button_deletar.place(y=350, x=245)

#EVENTOS
listbox.dnd_bind("<<Drop>>", drop_inside_list_box)
listbox.bind("<Double-Button-1>", open_image)
root.bind("<Key>", key_press)
#
root.mainloop()