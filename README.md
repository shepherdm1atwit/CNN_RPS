<!-- ABOUT THE PROJECT -->
# About The Project

CNN_RPS is an implementation of the game "rock paper scissors" that a human can play vs a computer through the use of a convolutional neural network. The computer chooses random hand signs to play, but uses a Keras image classification model running on a flask backend to recieve images from a web client and determine which hand sign the user is showing the camera. Try it out at [rps.CodeSmith.link](https://rps.codesmith.link)!

### Built With

* [Keras](https://keras.io/)
* [TensorFlow](https://www.tensorflow.org/)
* [MediaPipe](https://google.github.io/mediapipe/)
* [Flask](https://flask.palletsprojects.com/)
* [JQuery](https://jquery.com)
* [NGINX](https://www.nginx.com/)
* [gUnicorn](https://gunicorn.org/)

## Dataset / Feature Extraction
The dataset I chose to use for this project is a modified version of the "Rock-Paper-Scissors Images" dataset by [Julien de la Bruère-Terreault](https://github.com/imfdlh), found [here](https://www.kaggle.com/datasets/drgfreeman/rockpaperscissors). Google's [MediaPipe](https://google.github.io/mediapipe/) was used to perform feature extraction to simplify each image into it's basic shape by converting the images from full color and detail images of hands into greyscale skeletons with dots to represent each joint and lines to represent segments of the hand. This allows for my model to focus entirely on recognizing the shape of each hand sign in order to classify them into "rock", "paper", or "scissors", rather than also having to differentiate the hand from the surrounding environment before attempting to recognize and classify it's shape. An example of an original and feature extracted image can be seen below.<br>
![pre-feature-extraction](https://github.com/shepherdm1atwit/CNN_RPS/blob/1ba3257410f35213e830676064164381bb21e29b/train_test/hands_dataset/paper/04l5I8TqdzF9WDMJ.png)![post-feature-extraction](https://github.com/shepherdm1atwit/CNN_RPS/blob/1ba3257410f35213e830676064164381bb21e29b/train_test/dataset/paper/04l5I8TqdzF9WDMJ.png)


<!-- Deployment -->
# Deployment

## Basic/Local Setup - Python
**This setup is** *much* **simpler than the advanced setup, but is made to be temporary, not a "production" deployment**
1. Make sure `Python3`, `pip`, and `virtualenv` are installed on your system before continuing
2. Clone the repo and enter the directory it creates

   ```sh
   git clone https://github.com/shepherdm1atwit/CNN_RPS
   cd CNN_RPS
   ```
3. On the last line of `app.py`, change `host='0.0.0.0'` to `host='127.0.0.1'`
4. Create a python virtual environment and activate it
   
   ```python
   virtualenv rps
   source rps/bin/activate
   ``` 
   If running on Windows, use the following in place of `source rps/bin/activate`
   ```bat
   .\rps\Scripts\activate
   ```
   
5. Install required dependencies and run app.py
   
   ```python
   pip install -r requirements.txt
   python app.py

   ```

## Advanced/Persistent Setup - Nginx with gUnicorn
**This will create a persistent server accessable via your domain name and is intended for use as a "production" deployment**\

**Note: This setup is linux-only due to the usage of systemd and gUnicorn**

### Part 1: Python and Initial Setup
1. Make sure `Python3`, `pip`, `virtualenv`, and `nginx` are installed on your system before continuing
2. Clone the repo and enter the directory it creates

   ```sh
   git clone https://github.com/shepherdm1atwit/CNN_RPS
   cd CNN_RPS
   ``` 
   *the rest of the tutorial will assume you have cloned the repository to `/var/www`*
3. Create a python virtual environment and activate it
   
   ```python
   virtualenv rps
   source rps/bin/activate
   ``` 
4. Install required dependencies and deactivate virtual environment
   
   ```python
   pip install -r requirements.txt
   pip install wheel
   pip install gunicorn
   deactivate
   ```
   
### Part 2: Systemd Service Creation
1. Create the `CNN_RPS.service` file to start the application at boot
   ```sh
   sudo nano /etc/systemd/system/CNN_RPS.service
   ```
2. Fill `CNN_RPS.service` with the following (replacing <YOUR_USERNAME> with your username and updating paths if neccsary

   ```
   [Unit]
   Description=Gunicorn instance to serve CNN_RPS
   After=network.target

   [Service]
   User= <YOUR_USERNAME>
   Group=www-data
   WorkingDirectory=/var/www/CNN_RPS
   Environment="PATH=/var/www/CNN_RPS/rps/bin"
   ExecStart=/var/www/CNN_RPS/rps/bin/gunicorn --workers 3 --bind unix:CNN_RPS.sock -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Start and enable the newly created `CNN_RPS` service
   
   ```sh
   sudo systemctl start CNN_RPS
   sudo systemctl enable CNN_RPS
   ```

### Part 3: Nginx Configuration
1. Create a Nginx server configuration file called `CNN_RPS` in `sites-available`
   
   ```sh
   sudo nano /etc/nginx/sites-available/CNN_RPS
   ```
2. Fill this newly created file with, replacing `yourdomain` with your domain name and updating the path if neccsary
   
   ```
   server {
      listen 80;
      server_name yourdomain www.yourdomain;
      location / {
         include proxy_params;
         proxy_pass http://unix:/var/www/CNN_RPS/CNN_RPS.sock;
      }
   }
   ```
 
3. Link the file to the `/etc/nginx/sites-enabled` directory

   ```sh
   sudo ln -s /etc/nginx/sites-available/CNN_RPS /etc/nginx/sites-enabled
   ```

4. Restart Nginx to apply changes

   ```sh
   sudo systemctl restart nginx
   ```
### Part 4: SSL Configuration - Note: this example uses [CertBot](https://certbot.eff.org/) and [LetsEncrypt](https://letsencrypt.org/)
   Install and run CertBot, replacing `yourdomain` with your domain name - Note: certbot will ask for an email and TOS agreement the first time
   
   ```sh
   sudo add-apt-repository ppa:certbot/certbot
   sudo apt install python-certbot-nginx
   sudo certbot --nginx -d yourdomain -d www.yourdomain
   ```



<!-- USAGE EXAMPLES -->
## Usage

Once your flask server is running, either in development mode through `python app.py` or on your server, simply 
visit the webpage by going to www.yourdomain or localhost and enjoy.


## Final Report
For full report, please see the [presentation PDF](DataSci%20Final.pdf).


<!-- LICENSE -->
## License

Distributed under the CC-BY-SA 4.0 License. See `licence_and_credit.txt` for more information.



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Dataset is modified work by [Julien de la Bruère-Terreault](https://github.com/imfdlh)
