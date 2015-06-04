#!/usr/bin/python
# -*- coding: UTF-8 -*-

# GUI для первых двух лабораторных по КМЗИ
# (GUI для третьей реализован отдельно)
# В качестве библиотеки для создания графического интерфейса
# выбрана Tkinter, т. к. она её функционал достаточен для создания
# такого несложного графического интерфейса и она является стандартной
# библиотекой для Python.
# Использование функционала предыдущих лабораторных работ основано
# на вызове их как консольных утилит и проверке возвращаемого значения


# в Python 2.x библиотека называется Tkinter
# в 3.x - tkinter, поэтому сделаем так:
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
import funcs # модуль с функциями, общими для обоих GUI
	
# компиляция библиотеки, 1 и 2 лабораторных
def compileL12():
	toCompile = ['../library', '../lab1/caesar', '../lab1/vizhiner', '../lab2']
	for i in toCompile:
		errnum, output = funcs.myExec("cd " + i + "&& make")		
		if errnum:
			tkMessageBox.showerror("Can't compile 1 and 2 labs", output[1])
			return False
	return True
	
# запуск консольной утилиты с введёнными параметрами
# на вход поступает путь к исполняемому файлу и флаг запуска
def encSmthng(command, flag):
	# cчитаем имя входного файла
	inFileName = funcs.getFileName(entInFileName, "input")
	if inFileName == None:
		return
	
	outFileName = funcs.getFileName(entOutFileName, "output")
	if inFileName == None:
		return
	
	keyFileName = funcs.getFileName(entKeyFileName, "key")
	if inFileName == None:
		return	
	
	# формируем строку запуска консольной утилиты
	cmd = command + " -i \"" + inFileName + "\" -o \"" + outFileName + "\" -k \"" + keyFileName + "\" " + flag
	
	# собственно, пытаемся выполнить консольную утилиту
	errnum, output = funcs.myExec(cmd)
	if errnum:
		tkMessageBox.showerror("Error", output[1])
	else:
		tkMessageBox.showinfo("Finished", "Finished")
	

# обработчики кнопок кодирования и декодирования
def caesarEnc():
	encSmthng("cd ../lab1/caesar/ && ./caesar", "-e")
	
def caesarDec():
	encSmthng("cd ../lab1/caesar/ && ./caesar", "-d")
	
def vizhinerEnc():
	encSmthng("cd ../lab1/vizhiner/ && ./vizhiner", "-e")
	
def vizhinerDec():
	encSmthng("cd ../lab1/vizhiner/ && ./vizhiner", "-d")
	
def DESEnc():
	encSmthng("cd ../lab2/ && ./DES", "-e")
	
def DESDec():
	encSmthng("cd ../lab2/ && ./DES", "-d")
	

# обработчик кнопки выбора входного файла
def explIn():
	funcs.setInFileName(entInFileName, root)
		
# обработчик кнопки выбора файла c ключом
def explKey():
	funcs.setInFileName(entKeyFileName, root)
		
# обработчик кнопки выбора выходного файла
def explOut():
	funcs.setOutFileName(entOutFileName, root)


# создание главного окна
root = myTkinter.Tk()
root.wm_title("GUI for 1 and 2 labs")
root.geometry('500x200')
root.resizable(width=False, height=False)

# создадим на главном окне элементы управления

# подпись, кнопки кодирования и декодирования Цезаря
btnCaesarEnc = ttk.Button(root, text="Encode", command=caesarEnc)
btnCaesarEnc.place(relx=0.2, rely=1.0, y=-75, anchor="n")
btnCaesarDec = ttk.Button(root, text="Decode", command=caesarDec)
btnCaesarDec.place(relx=0.2, rely=1.0, y=-40, anchor="n")
lblCaesar = ttk.Label(root, text="Caesar", font="Arial 14")
lblCaesar.place(relx=0.2, rely=1.0, y=-100, anchor="n")

# подпись, кнопки кодирования и декодирования Виженера
btnVizhinerEnc = ttk.Button(root, text="Encode", command=vizhinerEnc)
btnVizhinerEnc.place(relx=0.5, rely=1.0, y=-75, anchor="n")
btnVizhinerDec = ttk.Button(root, text="Decode", command=vizhinerDec)
btnVizhinerDec.place(relx=0.5, rely=1.0, y=-40, anchor="n")
lblVizhiner = ttk.Label(root, text="Vizhiner", font="Arial 14")
lblVizhiner.place(relx=0.5, rely=1.0, y=-100, anchor="n")

# подпись, кнопки кодирования и декодирования DES
btnDESEnc = ttk.Button(root, text="Encode", command=DESEnc)
btnDESEnc.place(relx=0.8, rely=1.0, y=-75, anchor="n")
btnDESDec = ttk.Button(root, text="Decode", command=DESDec)
btnDESDec.place(relx=0.8, rely=1.0, y=-40, anchor="n")
lblDES = ttk.Label(root, text="DES", font="Arial 14")
lblDES.place(relx=0.8, rely=1.0, y=-100, anchor="n")

# подпись, кнопка и строка для ввода входного файла
entInFileName = ttk.Entry(root)
entInFileName.place(relx=0.6, rely=0.1, relwidth=0.55, height=20, anchor="n")
lblInputFN = ttk.Label(root, text="Input file name:")
lblInputFN.place(relx=0.3, x=-3, rely=0.1,anchor="ne")
btnExplIn = ttk.Button(root, text="...", command=explIn)
btnExplIn.place(relx=0.87, x=5, rely=0.1, heigh=20, width=30, anchor="nw")

# подпись, кнопка и строка для ввода файла с ключом
entKeyFileName = ttk.Entry(root)
entKeyFileName.place(relx=0.6, rely=0.2, relwidth=0.55, height=20, anchor="n")
lblKeyFN = ttk.Label(root, text="Key file name:")
lblKeyFN.place(relx=0.3, x=-3, rely=0.2,anchor="ne")
btnExplKey = ttk.Button(root, text="...", command=explKey)
btnExplKey.place(relx=0.87, x=5, rely=0.2, heigh=20, width=30, anchor="nw")

# подпись, кнопка и строка для ввода выходного файла
entOutFileName = ttk.Entry(root)
entOutFileName.place(relx=0.6, rely=0.3, relwidth=0.55, height=20, anchor="n")
lblOutFN = ttk.Label(root, text="Output file name:")
lblOutFN.place(relx=0.3, x=-3, rely=0.3,anchor="ne")
btnExplOut = ttk.Button(root, text="...", command=explOut)
btnExplOut.place(relx=0.87, x=5, rely=0.3, heigh=20, width=30, anchor="nw")

# попробуем скомпилировать 1 и 2 лабораторные
# если не удастся - выход из программы
if not compileL12():
	root.destroy()
	sys.exit(-1)
	
# запускаем главный цикл обработки событий
root.mainloop()
