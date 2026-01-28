This repository contains the Kubernetes deployment solution for the full ecosystem:
- **StatisticsAPI** (publicly accessible via NGINX Ingress with mTLS termination)
- **DeviceRegistrationAPI** (internal-only, accessible only inside the cluster)
- **PostgreSQL** running in Kubernetes (StatefulSet) with storage on **external NFS**
- Security hardening (NetworkPolicies + mTLS certificates)


## Repository Structure

- `apis/`
  - Source code for the APIs (DeviceRegistrationAPI & StatisticsAPI)
- `infra/`
  - `infra/nfs/` : NFS provisioner / storage class manifests (external storage)
  - `infra/db/`  : PostgreSQL manifests (StatefulSet/Service/Secrets/PVC)
  - `ingress-nginx/`
    - NGINX Ingress Controller manifests (NodePort)
  - `certifications/`
    - Self-signed certificate generation instructions (see `certification.txt`)
- `kubernetes/`
  - `kubernetes/namespace.yaml` : namespace
  - `kubernetes/Registration/`  : manifests for DeviceRegistrationAPI (Deployment/Service/Secret)
  - `kubernetes/Statistics/`    : manifests for StatisticsAPI (Deployment/Service/ConfigMap)
  - `kubernetes/api-networkpolicy.yaml` : NetworkPolicies for APIs
  - `kubernetes/nginx.yaml` : Ingress resources for StatisticsAPI (mTLS)


- In order to create the namespace for application run the following 

    $kubectl apply -f kubernetes/namespace.yaml 

- After the creation of the namespace run the following commands in order to create the applications
    
    $kubectl apply -f kubernetes/Registration 
    
    $kubectl apply -f kubernetes/Statistics

- For the infra part 
First run the manifest for the creation of the nfs storage (in case the we habe already nfs storage for storaging the data outside of the cluster)

    $kubectl apply -f infra/nfs 

Second run the manifest for the creation of the postgress db 

    $kubectl -f apply infra/db 

For external communication run the following deploy ingress-nginx

    $kubectl apply -f infra/ingress-nginx 

For security:
1)Read the following folder Certification in order to create the self-signed crts for applications and certification.txt
2)Network hardening 

    $kubectl -f kubernetes/api-networkpolicy.yaml 

    $kubectl -f kubernetes/nginx.yaml 