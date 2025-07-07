#include <curl/curl.h>
#include <stdio.h>
#include <sanitizer/lsan_interface.h>

#define URL "http://www.wikipedia.org"
#define LOCAL_PROXY_URL "http://someurl.com:80/"

int main(void)
{
  CURL *curl = curl_easy_init();
  if(curl) {
    CURLcode ret;
    curl_easy_setopt(curl, CURLOPT_URL, URL);
    curl_easy_setopt(curl, CURLOPT_PROXY, LOCAL_PROXY_URL);
    /* set the proxy type */
    curl_easy_setopt(curl, CURLOPT_PROXYTYPE, (long)CURLPROXY_SOCKS5);
    while (__AFL_LOOP(1000)) {
	__lsan_do_leak_check();
    	ret = curl_easy_perform(curl);
	__lsan_do_leak_check();
    }
    curl_easy_cleanup(curl);
  }
}

