#include "DESCoder.h"
#include "string.h"
#include <vector>
#include <iostream>
#include <fstream>
#include "myLib.h"

using namespace std;

vector<unsigned char> encodeVector (vector<unsigned char>& input, DESCoder& coder);
vector<unsigned char> decodeVector (vector<unsigned char>& input, DESCoder& coder);

int main (int argc, char* argv[])
{
	argumentsCoders passedArgs;
	if (!passedArgs.parseArgs(argc, argv, "DES"))
		return -1;

	// считываем входной файл в вектор
	vector<unsigned char> inputContent;
	if (! getFileContent(passedArgs.inFileName, inputContent) )
	{
		cerr << "Can't open input file: " << passedArgs.inFileName << endl;
		return -1;
	}

	// считываем ключ в вектор
	vector<unsigned char> key;
	if (!getFileContent(passedArgs.keyFileName, key) )
	{
		cerr << "Can't open key file: " << passedArgs.keyFileName << endl;
		return -1;
	}

	// проверяем, ключ должен быть 8-байтным
	if (key.size() != 8)
	{
		cerr << "Key must be 8 byte value!" << endl;
		return -1;
	}

	// для шифрования и деширования используется один и тот же ключ
	// поэтому создаём общий "шифратор"
	DESCoder coder(key);

	vector<unsigned char> output; // куда будет записан результат шифрования/дешифрования

	if(passedArgs.encode)
	{
		// шифрование входного фалйа.
		output = encodeVector (inputContent, coder);
	}
	else
	{
		// дешифрование входного файла.
		// первым делом во входном файле записано количество нулей
		// в конце файла для выравнивания длины до кратной 8
		output = decodeVector(inputContent, coder);
	}

	// теперь можно записать результат шифрования/дешифрования
	// в выходной файл

	if (!setFileContent(passedArgs.outFileName, output) )
	{
		cerr << "Can't open output file: " << passedArgs.outFileName << endl;
		return -1;
	}
	return 0;
}

vector<unsigned char> encodeVector (vector<unsigned char>& input, DESCoder& coder)
{
	// шифрование input шифратором coder
	// для этого необходимо разбить input на блоки по 8 байт
	// а остаток дополнить нулями.
	// количество нулей в конце запишем в начало результата для корректного дешифрования
	vector<unsigned char> output;
	output.push_back (8 - input.size() % 8);

	for (int i = 0; i < input.size() / 8; i++)
	{
		vector<unsigned char> dataPart8; // очередной 8-байтовый кусок
		dataPart8.insert(dataPart8.end(), 
			input.begin() + i * 8, input.begin() + (i + 1) * 8 );

		// шифруем кусочек из 8 байт
		vector<unsigned char> codedPart = coder.encode(dataPart8);

		// записываем его в результат
		output.insert(output.end(), codedPart.begin(), codedPart.end());
	}

	// теперь разберёмся с оставшимся кусочком
	if (input.size() % 8)
	{
		// сформируем кусок из 8 байт,
		// записав незашифрованные байты и дополнив нулями до длины 8
		vector<unsigned char> dataPart;
		dataPart.insert(dataPart.end(),
			input.end() - input.size() % 8, input.end());

		dataPart.insert(dataPart.end(), 8 - input.size() % 8, 0);

		vector<unsigned char> codedPart = coder.encode(dataPart);
		output.insert(output.end(), codedPart.begin(), codedPart.end());
	}

	return output;
}

vector<unsigned char> decodeVector (vector<unsigned char>& input, DESCoder& coder)
{
	// дешифрование вектора input шифратором coder
	// первым элементом в векторе input находится количество
	// нулей, которые пришлось вставить в конец шифруемого сообщения
	// для выравнивания длинны
	// затем идут несколько блоков по 8 байт - зашифрованные данные.
	// их-то и будем дешифровывать

	vector<unsigned char> output;
	for (int i = 0; i < (input.size() - 1) / 8; i++)
	{
		// формируем очередной кусочек из 8 байт
		vector<unsigned char> part8;
		part8.insert(part8.end(),
			input.begin() + i * 8 + 1, input.begin() + (i + 1) * 8 + 1 );

		// дешифруем его
		vector<unsigned char> decodedPart = coder.decode(part8);

		// записываем к результату
		output.insert(output.end(), decodedPart.begin(), decodedPart.end());
	}

	// избавляемся от лишних нулей в конце сообщения
	for (int i = 0; i < input[0]; i++)
		output.pop_back();

	return output;
}
