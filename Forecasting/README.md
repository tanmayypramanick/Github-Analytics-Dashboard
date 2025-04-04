#LSTM

> > Step1: What will LSTM do?

      1. LSTM will accept the GitHub data from flask microservice and will forecast the data for the next year using past 2 months data.
      2. It will also plot three different graph (i.e.  "model_loss", "lstm_generated_data", "all_issues_data") using matplot lib
      3. It will also plot graphs using the 'prophet' library and 'statsmodels' library.
      4. This graph will be stored as image in gcloud storage.
      5. The image URL are then returned back to flask microservice.

> > Step2: What is Google Cloud Storage?

       Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud
       Platform infrastructure.

> > Step3: Deploying LSTM to gcloud platform

      1: You must have Docker(https://www.docker.com/get-started) and Google Cloud SDK(https://cloud.google.com/sdk/docs/install)
           installed on your computer. Then, Create a gcloud project and enable the following:
           a.billing account
           b.Conatiner Registry API
           c. Cloudbuild API

      2. Update the GOOGLE BUCKET URL and BASE IMAGE PATH to the 'bucket url' as well as 'base image path' for your respective google storage bucket in line ...

      3: Use 'Docker' and 'gcloud' to create an image, update the tag and build on the google cloud using 'docker' commands (docker build, docker tag and docker push) and 'gcloud' commands (gcloud init, gcloud auth configure-docker).

      4: Click on create, this will create the service on port 5000 and will generate the url, hit the url.

      5: Copy flask gcloud generated url to be used later.

      6: Kindly add the following to the environment variable during the 'gcloud cloud run'
                Name                                 value
            a. GOOGLE_APPLICATION_CREDENTIALS     "<your_json_filename>.json"
            b. BASE_IMAGE_PATH                    "https://storage.googleapis.com/your bucket name/"
            c. BUCKET_NAME                         "your bucket name"

      7: Hit the create, this will create the service on port 5000 and will generate the url, hit the url.

      8: Copy the generated Flask gcloud url and store it for later use.
