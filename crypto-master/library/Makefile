linuxdyn: myLib.cpp myLib.h
	g++ -c -fPIC myLib.cpp
	g++ -shared -o libmyLib.so myLib.o
	rm *.o
	
windowsdyn: myLib.cpp myLib.h
	g++ -c myLib.cpp
	g++ -shared -o libmyLib.dll myLib.o
	del *.o
