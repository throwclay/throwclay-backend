# For protected routes, used token (example)

TOKEN=$(make -s token)
curl -s -X POST http://127.0.0.1:8000/api/studios \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"name":"Demo Studio","subdomain":"demo","timezone":"America/Los_Angeles"}' | jq
