#!/bin/sh

LSAN_OPTIONS=detect_leaks=0 LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ LD_BIND_NOW=1 LD_PRELOAD=libdesock.so ./ldap_fuzzer_old_compiler

