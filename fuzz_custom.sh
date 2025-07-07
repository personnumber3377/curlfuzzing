#!/bin/sh

# rm -r out/
export PYTHONPATH=.
export LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/
export AFL_PRELOAD=libdesock.so
export LSAN_OPTIONS=symbolize=0:exitcode=23
export AFL_PYTHON_MODULE=mutator
PYTHONPATH=. AFL_PYTHON_MODULE=mutator LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ AFL_PRELOAD=libdesock.so LSAN_OPTIONS=symbolize=0:exitcode=23 afl-fuzz -x dictionary.dict -t 300 -i - -o out -- ./sample_code



