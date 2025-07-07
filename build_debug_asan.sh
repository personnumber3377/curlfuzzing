#!/bin/sh

# gcc sample_code.c -o sample_code $(pkg-config --cflags --libs libcurl)


afl-clang-fast sample_code.c -o sample_code \
  -I$HOME/curl_build/include \
  -L$HOME/curl_build/lib \
  -lcurl -fsanitize=address,undefined

