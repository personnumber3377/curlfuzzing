#!/bin/sh

# rm -r out/

export LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/
export AFL_PRELOAD=libdesock.so
export LSAN_OPTIONS=symbolize=0:exitcode=23
LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ AFL_PRELOAD=libdesock.so LSAN_OPTIONS=symbolize=0:exitcode=23 afl-fuzz -x dictionary.dict -t 300 -i - -o no_custom -- ./sample_code



