CXXFLAGS = -O3 -Wall -Wextra -Wsign-compare -Wshadow -Wno-unused-parameter -std=c++11 -fmessage-length=0 -Wfatal-errors -I/home/tim/dev/build/rocksdb/include/

default: all

insertkv: insertkv.o
	$(CXX) -o $@ $^ -static -L/home/tim/dev/build/rocksdb -lrocksdb -lrt -lz -lbz2 -lpthread -lsnappy -Wl,-rpath=/home/tim/dev/build/rocksdb

updatekv: updatekv.o
	$(CXX) -o $@ $^ -static -L/home/tim/dev/build/rocksdb -lrocksdb -lrt -lz -lbz2 -lpthread -lsnappy -ljsoncpp -Wl,-rpath=/home/tim/dev/build/rocksdb


%.o : %.cc *.h Makefile
	@echo "***" $< "***"
	$(CXX) $(CXXFLAGS) -c $< -o $@  

.PHONY : all clean
all:    insertkv updatekv

clean:
	rm -f insertkv updatekv
