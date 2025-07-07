#include <curl/curl.h>
#include <stdlib.h>
#include <stdio.h>
#include <sanitizer/lsan_interface.h>

#define URL "http://127.0.0.1:8081"  // Change to local HTTP service (or your proxy dummy response handler)
#define LOCAL_PROXY_URL "http://127.0.0.1:8080"  // Local SOCKS5 proxy running on your fuzz harness

int main(void)
{

  if (getenv("AFL_CRASH_FILE")) {
    freopen(getenv("AFL_CRASH_FILE"), "r", stdin);
}      
	CURL *curl = curl_easy_init();
  if (curl) {
    CURLcode ret;

    curl_easy_setopt(curl, CURLOPT_URL, URL);
    curl_easy_setopt(curl, CURLOPT_PROXY, LOCAL_PROXY_URL);
    curl_easy_setopt(curl, CURLOPT_PROXYTYPE, (long)CURLPROXY_SOCKS5);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 5000L);  // Optional: avoid infinite hangs

    while (__AFL_LOOP(1000)) {
      __lsan_do_leak_check();  // Leak detection before
      ret = curl_easy_perform(curl);
      __lsan_do_leak_check();  // Leak detection after
    }

    curl_easy_cleanup(curl);
  }

  return 0;
}

