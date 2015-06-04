#!/usr/bin/python
# -*- coding: UTF-8 -*-

# извлечение информации из .wav файла, спрятанной там скриптом stegwavein
# суть - в младших битах каждого сэмпла находятся информационные биты
# причём в первых 16 - количество байт, спрятанных в оставшейся части файла

import argparse
import sys
import wave
import numpy

# парсинг аргументов командной строки
def getArguments ():
	parser = argparse.ArgumentParser(prog = "stegwaveout", description = "Steganography to wave files. Extracts file from .wav")
	parser.add_argument ('container', help = "File name of .wav file for container")
	parser.add_argument ('output', help = "File name for extracted result")
	
	return parser.parse_args()

# список типов, которые могут использоваться для хранения сэмплов
types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}

def main():	
	arguments = getArguments()
	
	# попытаемся открыть .wav файл - контейнер
	try:
		wav = wave.open(arguments.container, mode="r")
	except:
		print >> sys.stderr, arguments.container, "- not .wav file!"
		sys.exit(-1)
		
	nframes = wav.getnframes()
	sampwidth = wav.getsampwidth()
	content = wav.readframes(nframes)
	samples = numpy.fromstring(content, dtype=types[sampwidth])
	
	# вытащим первые 16 бит - количество байт, спрятанных в остальной части
	samplesIndexator = 0
	hiddenFileSize = 0
	for i in range(16):
		hiddenFileSize += (samples[samplesIndexator] % 2) * 2 ** i
		samplesIndexator += 1
		
	byteList = [] # список байтов спрятанного файла
	# теперь достанем size * 8 бит спрятанного файла
	for j in range (hiddenFileSize):
		curByte = 0
		for i in range (8):
			curByte += (samples[samplesIndexator] % 2) * 2 ** i
			samplesIndexator += 1
		
		# в curByte - очередной байт числа
		# запишем его в массив
		byteList.append(curByte)

	# преобразуем получившийся список из элементов типа numpy.int8
	# в массив байт
	byteArray = numpy.array(byteList, dtype=numpy.int8).tostring()
	
	# запишем получившийся массив в файл
	outFile = open(arguments.output, 'wb')
	outFile.write(byteArray)
	outFile.close()
	
if __name__ == "__main__":
	main()
