# Flask Webcam

## Demo Video: 
https://www.loom.com/share/c185c4e4115d4e90a46d0d952361c6b8

## References: 
1. https://github.com/dxue2012/python-webcam-flask

# Local Setup

NOTE: The webapp currently only works locally on Firefox

0. Clone and enter the repo on your local machine
1. Create a virtual enviornment with `virtualenv -p python3.7 venv`
2. Activate the virtualenv `source ./venv/bin/activate`
3. Install the required dependencies `pip install -r requirements.txt`
4. Run the webserver via `gunicorn -k eventlet -w 1 app:app --log-file=-`


Note: https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957#51004957
