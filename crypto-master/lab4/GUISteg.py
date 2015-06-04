#!/usr/bin/python
# -*- coding: UTF-8 -*-

# GUI для третьей лабораторной по КМЗИ

try:
	import Tkinter as myTkinter
except:
	try:
		import tkinter as myTkinter
	except:
		print "You have to install Tkinter"
		sys.exit(-1)

import ttk
import sys
import tkMessageBox
import funcs
	
def stegIn():
	contFileName = funcs.getFileName(entContFileName, "container")
	if contFileName == None:
		return
	
	outFileName = funcs.getFileName(entOutFileName, "output")
	if outFileName == None:
		return
	
	infFileName = funcs.getFileName(entInfFileName, "information")
	if infFileName == None:
		return	
	
	cmd =  "cd ../lab3/ && ./stegwavein.py \"" + contFileName + "\" \"" + infFileName + "\" \"" + outFileName + "\""
	
	errnum, output = funcs.myExec(cmd)
	if errnum:
		tkMessageBox.showerror("Error", output[1])
	else:
		tkMessageBox.showinfo("Finished", "File " + infFileName + " hiden in " + outFileName)
	
def stegOut():
	contFileName = funcs.getFileName(entContFileName, "container")
	if contFileName == None:
		return
	
	outFileName = funcs.getFileName(entOutFileName, "output")
	if outFileName == None:
		return
		
	cmd =  "cd ../lab3/ && ./stegwaveout.py \"" + contFileName + "\" \"" + outFileName + "\""
	
	errnum, output = funcs.myExec(cmd)
	if errnum:
		tkMessageBox.showerror("Error", output[1])
	else:
		tkMessageBox.showinfo("Finished", "File " + outFileName + " ejected to " + outFileName)


# обработчик кнопки выбора файла контейнера
def explCont():
	funcs.setInFileName(entContFileName, root)
		
# обработчик кнопки выбора информационного файла
def explInf():
	funcs.setInFileName(entInfFileName, root)
		
# обработчик кнопки выбора выходного файла
def explOut():
	funcs.setOutFileName(entOutFileName, root)


# создание главного окна
root = myTkinter.Tk()
root.wm_title("GUI for steganography")
root.geometry('500x180')
root.resizable(width=False, height=False)

# создадим на главном окне элементы управления

# кнопки hide и eject
btnDESEnc = ttk.Button(root, text="Hide", command=stegIn)
btnDESEnc.place(relx=0.5, rely=1.0, y=-75, width=100, anchor="n")
btnDESDec = ttk.Button(root, text="Eject", command=stegOut)
btnDESDec.place(relx=0.5, rely=1.0, y=-40, width=100, anchor="n")


# подпись, кнопка и строка для ввода файла контейнера
entContFileName = ttk.Entry(root)
entContFileName.place(relx=0.6, rely=0.1, relwidth=0.55, height=20, anchor="n")
lblInputFN = ttk.Label(root, text="Container file name:")
lblInputFN.place(relx=0.3, x=-3, rely=0.1,anchor="ne")
btnExplCont = ttk.Button(root, text="...", command=explCont)
btnExplCont.place(relx=0.87, x=5, rely=0.1, heigh=20, width=30, anchor="nw")

# подпись, кнопка и строка для ввода информационного файла
entInfFileName = ttk.Entry(root)
entInfFileName.place(relx=0.6, rely=0.25, relwidth=0.55, height=20, anchor="n")
lblKeyFN = ttk.Label(root, text="Information file name:")
lblKeyFN.place(relx=0.3, x=-3, rely=0.25,anchor="ne")
btnExplInf = ttk.Button(root, text="...", command=explInf)
btnExplInf.place(relx=0.87, x=5, rely=0.25, heigh=20, width=30, anchor="nw")

# подпись, кнопка и строка для ввода выходного файла
entOutFileName = ttk.Entry(root)
entOutFileName.place(relx=0.6, rely=0.4, relwidth=0.55, height=20, anchor="n")
lblOutFN = ttk.Label(root, text="Output file name:")
lblOutFN.place(relx=0.3, x=-3, rely=0.4,anchor="ne")
btnExplOut = ttk.Button(root, text="...", command=explOut)
btnExplOut.place(relx=0.87, x=5, rely=0.4, heigh=20, width=30, anchor="nw")
	
root.mainloop()
