#!/usr/bin/python
# -*- coding: UTF-8 -*-

# стеганография в .wav файл методом LSB
# суть вкратце:
# в .wav файл в байты, которые отвечают за амлитуду очередного сэмпла,
# в самые младшие биты записываются биты входного файла.

# в данной работе использован модуль wave, который позволяет довольно просто
# вытащить из .wav файла байты, отвечающие за сэмплы

# вкратце о .wav файлах:
# формат wav служит для хранения НЕСЖАТОГО аудиопотока 
# (поэтому можно довольно спокойно менять младшие биты в сэмплах, не беспокоясь о заметности)
# Типичный wave-файл состоит из заголовочной части, тела с аудиопотоком и хвоста для дополнительной информации.
# (Вот именно в тело с аудиопотокам мы и будем прятать файл)
# Из заголовочной части извлекаются основные параметры — число каналов, битрейт, число фреймов — на основании
# которых осуществляется разбор аудиопотока. Wave-файл хранит в себе 1 или 2 канала, каждый из которых кодируется
# 8, 16, 24 или 32 битами. Последовательность бит, описывающая амплитуду волны в момент времени, называется сэмплом. 
# Последовательность сэмплов для всех каналов в определенный момент называется фреймом.

import argparse
import sys
import wave
import numpy

# парсинг аргументов командной строки
def getArguments ():
	parser = argparse.ArgumentParser(prog = "stegwavein", description = "Steganography to wave files. Hides file in .wav file")
	parser.add_argument ('container', help = "File name of .wav file for container")
	parser.add_argument ('information', type = argparse.FileType(mode = 'rb'), help = "File name of file which you want to hide in .wav")
	parser.add_argument ('output', help = "File name of .wav file for result")
	
	return parser.parse_args()

# список типов, которые могут использоваться для хранения сэмплов
types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}

# устанавливает младший бит числа num битом bit
def setLastBit(num, bit):
	if num % 2: # если последний бит числа равен 1
		if bit == 0:
			return num + 1
		else:
			return num
	else: # если последний бит числа равен 0
		if bit == 1:
			return num + 1
		else:
			return num
	

def main():	
	arguments = getArguments()
	
	# попытаемся открыть .wav файл, в который будем прятать информацию, 
	# заодно проверив, действительно ли .wav файл был передан, а не что-то другое
	try:
		wav = wave.open(arguments.container, mode="r")
	except:
		print >> sys.stderr, arguments.container, "- not .wav file!"
		sys.exit(-1)
		
	nframes = wav.getnframes() # узнаем количество фреймов во входном файле	
	
	# узнаем размер (в байтах) одного сэмпла
	sampwidth = wav.getsampwidth()

	# считываем все фреймы в строку
	content = wav.readframes(nframes)
	
	# Теперь нужно разобрать эту строку. 
	# Параметр sampwidth определяет, сколько байт уходит на кодирование одного сэмпла.
	# Функция fromstring() создает одномерный массив из байтовой строки, 
	# при этом параметр dtype определяет, как будут интерпретированы элементы массива. 
	# В нашем случае, тип данных берется из словаря «types», в котором сопоставлены размеры сэмпла и типы данных numpy.
	samples = numpy.fromstring(content, dtype=types[sampwidth])
	
	# Теперь у нас есть массив сэмплов аудиопотока.
	# по сути - просто числа, определяющие амплитуду аудиосигнала в каждый момент времени.
	# у этих чисел и будем менять младшие биты
	# но для начала необходимо считать информационный файл и проверить, сможем ли мы
	# все биты этого файла + размер файла уместить в контейнере
	infFileContent = arguments.information.read() # считываем содержимое файла
	infFileContent = numpy.fromstring(infFileContent, dtype=numpy.int8) # представим его в виде массива байт
	arguments.information.close()
	
	if len(infFileContent) > 2 ** 16: # если размер файла не вместится в 2 байта
		print >> sys.stderr, arguments.information, "is too large file to hide in", arguments.container
		sys.exit(-1)
		
	if (len(infFileContent) + 2) * 8 > len(samples): # если количество бит, которые необходимо спрятать, больше, чем число сэмплов
		print >> sys.stderr, arguments.information, "is too large file to hide in", arguments.container
		sys.exit(-1)
		
	samplesIndexator = 0
	# спрячем размер информационного файла
	infSize = len(infFileContent)
	for i in range(16): # отведём под размер 16 бит (2 байта)
		samples[samplesIndexator] = setLastBit(samples[samplesIndexator], infSize % 2)
		infSize /= 2
		samplesIndexator += 1
		
	# теперь спрячем сам файл
	for i in range (len(infFileContent)):
		curByte = infFileContent[i]
		for j in range (8):
			samples[samplesIndexator] = setLastBit(samples[samplesIndexator], curByte % 2)
			curByte /= 2
			samplesIndexator += 1
		
	# запишем изменённые сэмплы в новый .wav файл
	wavOut = wave.open(arguments.output, 'w')
	wavOut.setparams( wav.getparams() ) # параметры выходного .wav совпадают со входным
	wavOut.writeframes(samples.tostring()) # а вот сэмплы уже другие
	
	
if __name__ == "__main__":
	main()
