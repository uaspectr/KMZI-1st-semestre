#include "myLib.h"
#include "getopt.h"

argumentsCoders :: argumentsCoders()
{
	inFileName = NULL;
	outFileName = NULL;
	keyFileName = NULL;
	encode = true;
}

bool argumentsCoders :: parseArgs(int argc, char* argv[], const char* programName)
{
	int opt = getopt( argc, argv, "i:o:k:de");
	while( opt != -1 ) 
	{
		switch( opt ) 
		{
		case 'i':
			this->inFileName = optarg;
			break;
		case 'o':
			this->outFileName = optarg;
			break;
		case 'k':
			this->keyFileName = optarg;
			break;
		case 'd':
			this->encode = false;
			break;
		case 'e':
			this->encode = true;
			break;
		}
		opt = getopt( argc, argv, "i:o:k:de");
	}

	if (
		this->inFileName == NULL || 
		this->outFileName == NULL ||
		this->keyFileName == NULL
		)
	{
		cerr << "Wrong arguments" << endl;
		cout << "Coder and decorder "<< programName << endl;
		cout << "Usage: " << endl;
		cout << programName <<"-i <input> -o <output> -k <key> [ -e | -d ]" << endl;
		cout << "Parameters:" << endl;
		cout << "\t<input>  \t file name for input file" << endl;
		cout << "\t<output> \t file name for output file" << endl;
		cout << "\t<key>    \t file name for file with key " << endl;
		cout << "\tUse key \"e\" for encoding, \"d\" for decoding" << endl << endl;
		return false;
	}	
	return true;
}

bool getFileContent(char* fileName, vector<unsigned char> &fileContent)
{
	ifstream inputStream(fileName, std::ios::binary);
	if (inputStream.fail())
		return false;


	inputStream.seekg(0, std::ios::end);
	int inputSize = inputStream.tellg();
	inputStream.seekg(0, std::ios::beg);

	if (!inputSize)
		return false;

	fileContent.resize(inputSize);
	inputStream.read ( (char*) &fileContent.front(), inputSize);
	inputStream.close();

	return true;
}

bool setFileContent(char* fileName, vector<unsigned char> &fileContent)
{
	ofstream outStream(fileName, std::ios::binary);
	outStream.write((char*)&fileContent.front(), fileContent.size());
	outStream.close();
	return true;
}
