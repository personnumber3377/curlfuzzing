#include <curl/curl.h>
#include <stdio.h>
#include <sanitizer/lsan_interface.h>

#define FUZZ_TIMEOUT_MS 5000L  // Optional: timeout to avoid hangs

int main(void)
{
  CURL *curl = curl_easy_init();
  if (curl) {
    CURLcode ret;

    // This base URL will be mutated by your fuzzer
    curl_easy_setopt(curl, CURLOPT_URL, "ldap://127.0.0.1:8888/ou=users,dc=example,dc=com");
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, FUZZ_TIMEOUT_MS);

    // Disable verification (if using LDAPS)
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

    // Optional: verbose/debug logging
    curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

    while (__AFL_LOOP(1000)) {
      __lsan_do_leak_check();  // Leak detection before
      ret = curl_easy_perform(curl);
      __lsan_do_leak_check();  // Leak detection after
    }

    curl_easy_cleanup(curl);
  }

  return 0;
}