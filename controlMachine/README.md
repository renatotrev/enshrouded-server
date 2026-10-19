
# Steps

gcloud iam roles create vmStartStop --project=jogos-free-511916 \
  --permissions=compute.instances.get,compute.instances.start,compute.instances.stop

gcloud iam service-accounts create enshrouded-ctl

gcloud compute instances add-iam-policy-binding enshrouded \
  --zone=us-east1-c \
  --member="serviceAccount:enshrouded-ctl@jogos-free-511916.iam.gserviceaccount.com" \
  --role="projects/jogos-free-511916/roles/vmStartStop"


gcloud services enable cloudfunctions.googleapis.com run.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com

gcloud functions deploy enshrouded-ctl --gen2 --runtime=python312 \
  --region=us-east1 --source=. --entry-point=vm --trigger-http \
  --allow-unauthenticated \
  --service-account=enshrouded-ctl@jogos-free-511916.iam.gserviceaccount.com \
  --set-env-vars=PROJECT=jogos-free-511916,TOKEN=ceea5b616a66517cde29b6db9b410a6c



## Command to start auto-shutdown

echo "* * * * * root python3 /home/portalfactorymess/enshrouded-server/controlMachine/idle-check.py" | sudo tee /etc/cron.d/idle-check

sudo rm /etc/cron.d/idle-check

## Commands to use

### Start Server
-  https://us-east1-jogos-free-511916.cloudfunctions.net/enshrouded-ctl?key=ceea5b616a66517cde29b6db9b410a6c&action=start
### Stop Server
-  https://us-east1-jogos-free-511916.cloudfunctions.net/enshrouded-ctl?key=ceea5b616a66517cde29b6db9b410a6c&action=stop
### Check Server Status
-  https://us-east1-jogos-free-511916.cloudfunctions.net/enshrouded-ctl?key=ceea5b616a66517cde29b6db9b410a6c

