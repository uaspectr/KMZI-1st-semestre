#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

class argumentsCoders
{
public:
	char* inFileName;
	char* outFileName;
	char* keyFileName;
	bool encode;

	argumentsCoders();

	bool parseArgs(int argc, char* argv[], const char* programName);
	
};

bool getFileContent(char* fileName, vector<unsigned char> &fileContent);
bool setFileContent(char* fileName, vector<unsigned char> &fileContent);
