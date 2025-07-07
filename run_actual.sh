#!/bin/sh

LSAN_OPTIONS=verbosity=1:log_threads=1 LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ LD_BIND_NOW=1 LD_PRELOAD=libdesock.so ./sample_code

