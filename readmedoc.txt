gcloud auth login
gcloud config set project lunar-pact-484800-c3
gcloud config list
gcloud services enable artifactregistry.googleapis.com
gcloud services enable compute.googleapis.com



docker tag 

docker build -t fast-web3 .
docker tag fast-web3 us-central1-docker.pkg.dev/lunar-pact-484800-c3/fast-repo/fast-web3:latest
docker push us-central1-docker.pkg.dev/lunar-pact-484800-c3/fast-repo/fast-web3:latest


VM 
gcloud compute instances create fast-web1-vm `
  --zone=us-central1-a `
  --machine-type=e2-micro `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --metadata-from-file user-data=cloud-init.yaml `
  --tags=http-server


firewall 
gcloud compute firewall-rules create allow-http `
  --allow tcp:80 `
  --target-tags=http-server
gcloud compute instances list
