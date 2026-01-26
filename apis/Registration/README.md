The following folder contains 
- The source code for the reqistration of the devices
- The docker file of the image from the source code and the requirements.txt
    - In order to create the image 
        1) Create the folder in your local machine 
        2) To build the image ,execute the following commands
            $ cd foldername (where are the files )
            $ sudo docker build -t  foldername/dockerhubrepo:tag . 


The image are located 

- DockerHub: panoschor/bank:

#In order to pull the image 
docker pull panoschor/bank:device-registration-1.0.0