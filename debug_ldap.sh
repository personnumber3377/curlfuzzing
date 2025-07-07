#!/bin/sh

LSAN_OPTIONS=detect_leaks=0 LD_LIBRARY_PATH=/home/oof/curlsocksfuzzer/ LD_BIND_NOW=1 LD_PRELOAD=libdesock.so gdb -q ./ldap_fuzzer -ex "run < ldap_out/default/crashes/id\:000000\,sig\:04\,src\:000092\,time\:486220\,execs\:1163504\,op\:havoc\,rep\:2"

