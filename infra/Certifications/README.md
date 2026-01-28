In the following commands we are creating the followings 
- server-ca.crt
- bank.local.crt/key
- client-ca.crt 
- client.crt/key

$mkdir -p certs && cd certs

# Server CA
$openssl genrsa -out server-ca.key 4096
$openssl req -x509 -new -nodes -key server-ca.key -sha256 -days 3650 \
  -subj "/CN=bank-server-ca" -out server-ca.crt

# Server cert for host bank.local
$openssl genrsa -out bank.local.key 2048
$openssl req -new -key bank.local.key -subj "/CN=bank.local" -out bank.local.csr

cat > san-server.ext <<'EOF'
subjectAltName=DNS:bank.local
extendedKeyUsage=serverAuth
EOF

$openssl x509 -req -in bank.local.csr -CA server-ca.crt -CAkey server-ca.key \
  -CAcreateserial -out bank.local.crt -days 365 -sha256 -extfile san-server.ext

# Client CA
$openssl genrsa -out client-ca.key 4096
$openssl req -x509 -new -nodes -key client-ca.key -sha256 -days 3650 \
  -subj "/CN=bank-client-ca" -out client-ca.crt

# Client cert
$openssl genrsa -out client.key 2048
$openssl req -new -key client.key -subj "/CN=bank-client" -out client.csr

$cat > san-client.ext <<'EOF'
extendedKeyUsage=clientAuth
EOF

$openssl x509 -req -in client.csr -CA client-ca.crt -CAkey client-ca.key \
  -CAcreateserial -out client.crt -days 365 -sha256 -extfile san-client.ext
