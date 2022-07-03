#!/bin/bash

if [ "$(curl -s -o /dev/null -w '%{http_code}' http://elasticsearch:9200/movies)" == "200" ]; then  
    echo "[+] Index movies existing"
else
    echo "[-] Index movies not existing"
    echo "[-] Creating index with map..."
    if [ "$(curl -s -o /dev/null -w '%{http_code}' -XPUT http://elasticsearch:9200/movies -H 'Content-Type: application/json' -d @./elasticsearch/indices/movies.json)" == "200" ]; then  
        echo "[+] Successfull creating index"
    else
        echo "[+] Fatal error: creating index 'movies'... Aborting"
    fi
fi
