# Next Word Prediction App - Hack the North Workshop

# A very simple Text autocomplete application



# This repo uses Docker and Flask to build the application.

## Steps:

### Without using Docker:
1. Clone the repository ````git clone https://github.com/Anirudh42/htn_next_word_prediction.git````
2. Download and install the ````pip```` package manager from here https://pip.pypa.io/en/stable/installation/ 
3. Install the packages with the command ````pip install requirements.txt````. Make sure you have the ````requirements.txt```` file
4. Run the application using ````python app.py````
5. Open http://0.0.0.0:5000 in your web browser and you should see the app running

#### With Docker:
1. Download and install Docker desktop from here https://www.docker.com/products/docker-desktop/
2. Execute the following lines to build the docker image and run it locally. Skip this step if you do not want to test it on your local machine
    ```
    docker build -t "your_image_name_here" .
    docker run -d -p 127.0.0.1:5000:5000 "name_of_your_running_container"
    ```
3. Make sure you have the Dockerfile before you run the ````docker build```` command
4. Open http://127.0.0.1:5000 in your web browser and you should see the app running

# Congrats you have built very own Text Autocomplete App!

## Note:
The ````main```` branch is partially filled out for the purpose of conducting the Workshop. In case you would like to run the full application use the ````development```` branch



