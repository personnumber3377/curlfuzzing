#include <curl/curl.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sanitizer/lsan_interface.h>

#define FUZZ_TIMEOUT_MS 5000L
#define MAX_URL_SIZE 10000

int main(void)
{
  char buf[MAX_URL_SIZE + 1] = {0};  // Null-terminated buffer
  size_t len = fread(buf, 1, MAX_URL_SIZE, stdin);

  // If input has no null terminator or seems empty, bail out
  if (len == 0 || memchr(buf, '\0', len) == NULL) {
    return 0;
  }

  CURL *curl = curl_easy_init();
  if (!curl) return 1;

  curl_easy_setopt(curl, CURLOPT_URL, buf);
  curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, FUZZ_TIMEOUT_MS);
  curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
  curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
  // curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

  while (__AFL_LOOP(1000)) {
    __lsan_do_leak_check();
    curl_easy_perform(curl);
    __lsan_do_leak_check();
  }

  curl_easy_cleanup(curl);
  return 0;
}