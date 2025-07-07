#!/bin/sh

# gcc sample_code.c -o sample_code $(pkg-config --cflags --libs libcurl)


# afl-clang-fast sample_code.c -o sample_code \
#   -I$HOME/curl_build/include \
#   -L$HOME/curl_build/lib \
#   -lcurl -fsanitize=address,undefined

afl-clang-fast -fsanitize=address,undefined ldap_fuzzer.c -o ldap_fuzzer_old_compiler \
  -I$HOME/curl_build_other/include \
  $HOME/curl_build_other/lib/libcurl.a \
  -lz -lssl -lcrypto -lidn2 -lpsl -lbrotlidec -lbrotlienc -lbrotlicommon -lzstd -lresolv -lm -ldl -lldap -llber



