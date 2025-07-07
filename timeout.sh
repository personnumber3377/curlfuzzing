#!/bin/sh

LSAN_OPTIONS=detect_leaks=0 LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ LD_BIND_NOW=1 LD_PRELOAD=libdesock.so gdb -q ./sample_code -ex "break recv; run < timeout.bin"

