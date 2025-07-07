#!/bin/sh

gcc sample_code.c -o sample_code $(pkg-config --cflags --libs libcurl)

