#!/bin/sh

# rm -r out/
# rm -r ldap_out
export LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/
export AFL_PRELOAD=libdesock.so
export LSAN_OPTIONS=symbolize=0:exitcode=23
# export PYTHONPATH=.
# export AFL_PYTHON_MODULE=mutator
export AFL_AUTORESUME=1
LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ AFL_PRELOAD=libdesock.so LSAN_OPTIONS=symbolize=0:exitcode=23 afl-fuzz -x ldap_dict.dict -t 300 -i ldap_in -o ldap_out_normal -- ./ldap_fuzzer_old_compiler



