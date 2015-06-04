#!/usr/bin/python
# -*- coding: UTF-8 -*-

# функции, общие для обоих GUI

import tkMessageBox
import subprocess
import os
import tkFileDialog

# выполнение команды command
# возвращает полученное значение (код ошибки), содержимое stdout и stderr
def myExec(command):
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	proc.wait()
	return proc.returncode, proc.communicate()
	
# получить имя файла из поля ввода tkEntry
# если его нет - вывести сообщение об ошибке
def getFileName(tkEntry, what):
	fileName = tkEntry.get()
	if fileName == '':
		tkMessageBox.showerror("Error", "You must specify " + what + " file name!")
		return None
	# если путь относительный - сделаем абсолютным относительно текущей директории
	if '/' not in fileName:
		fileName = os.getcwd() + "/" + fileName
	return fileName
	
# установка имени входного файла в tkEntry
# вызовом диалога открытия файла
def setInFileName(tkEntry, root):
	fn = tkFileDialog.Open(root, filetypes = [('All files', '*')]).show()	
	if fn != '':
		tkEntry.delete(0, 'end')
		tkEntry.insert(0, fn)
		
# аналогичная функция для выходного файла
def setOutFileName(tkEntry, root):
	fn = tkFileDialog.SaveAs(root, filetypes = [('All files', '*')]).show()	
	if fn != '':
		tkEntry.delete(0, 'end')
		tkEntry.insert(0, fn)
