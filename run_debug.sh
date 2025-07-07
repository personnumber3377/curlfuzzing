#!/bin/sh

 LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ LSAN_OPTIONS=verbosity=1:log_threads=1 LD_BIND_NOW=1 LD_PRELOAD=libdesock.so gdb --args ./sample_code

