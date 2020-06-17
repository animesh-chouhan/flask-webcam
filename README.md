# Webapp to check health of user
We use Euler Video Magnification to detect slight changes in the video to predict approximate health metrics.  

Detect heart rates using a webcam. In the future, this can be overlayed onto video calls, etc to help in tele-medicine. Also, would be a useful product in the current Covid19 times.

![alt text](https://raw.githubusercontent.com/ankitchiplunkar/myhealthcheck/master/static/demo_pic.png)

## Demo Video: 
https://www.loom.com/share/c185c4e4115d4e90a46d0d952361c6b8

## Demo website: 
https://myhealthcheckapp.herokuapp.com/ 

Note: you might see other users
Note: Works best with firefox

## Participants: 
Ankit Chiplunkar : https://twitter.com/ankitchiplunkar 

Animesh Singh : https://twitter.com/animeshsingh38


## References: 
1. https://www.youtube.com/watch?v=EhZXDgG9oSk 
2. https://github.com/dxue2012/python-webcam-flask

# Local Setup

NOTE: The webapp currently only works locally on Firefox

0. Clone and enter the repo on your local machine
1. Create a virtual enviornment with `python3.7`
2. Install the required dependencies `pip install -r requirements.txt`
4. Run the webserver via `gunicorn -k eventlet -w 1 app:app --log-file=-`


Note: https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957#51004957
