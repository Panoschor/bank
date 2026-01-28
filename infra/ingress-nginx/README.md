Install NGINX Ingress Controller

1- Create a namespace
$kubectl create namespace ingress-nginx

2- Deploy manifests
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

3- Patch the NodePort
kubectl -n ingress-nginx patch svc ingress-nginx-controller --type='json' -p='[
  {"op":"replace","path":"/spec/type","value":"NodePort"},
  {"op":"replace","path":"/spec/ports/0/nodePort","value":30080},
  {"op":"replace","path":"/spec/ports/1/nodePort","value":30443}
]'

In case that IngressClass is needed

cat > ingressclass-nginx.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
EOF

$kubectl apply -f ingressclass-nginx.yaml
