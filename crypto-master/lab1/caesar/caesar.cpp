#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <vector>
#include "myLib.h"

using namespace std;

int main(int argc, char* argv[])
{
	argumentsCoders passedArgs;
	if (!passedArgs.parseArgs(argc, argv, "caesar"))
		return -1;

	vector<unsigned char> inputContent;
	if ( !getFileContent(passedArgs.inFileName, inputContent) )
	{
		cerr << "Can't open input file: " << passedArgs.inFileName << endl;
		return -1;
	}

	int shear = 0; //сдвиг
	ifstream keyStream(passedArgs.keyFileName);
	if (keyStream.fail())
	{
		cerr << "Can't open key file: " << passedArgs.keyFileName << endl;
		return -1;
	}
	keyStream >> shear ;
	keyStream.close();

	for(int i = 0; i < inputContent.size(); i++)
	{
		if(passedArgs.encode)
		{
			inputContent[i] += (unsigned char)(shear);
		}
		else
		{
			inputContent[i] -= (unsigned char)(shear);
		}
	}

	if (! setFileContent(passedArgs.outFileName, inputContent) )
	{
		cerr << "Can't open output file: " << passedArgs.outFileName << endl;
		return -1;
	}
	return 0;
}
