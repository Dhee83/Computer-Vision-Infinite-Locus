# Step1. Install Python

- After installing paython, install virtualenv 
```brew install virtualenv```
for more infor visit [this link](https://formulae.brew.sh/formula/virtualenv)

after installing virtualenv create virtualenv by following command
- `virtualenv <you_env_name> -p pyhton3`

- activate Virtualenv
    `source <path/your_env_folder>/bin/activate` 

- after activating venv install dependecies
    ```pip install -U channels["daphne"]```
    - Note : run this to avaoid  some dependecy conflicts

- after this run the following command
    ```pip install -r requirements.txt```

once finish you can run scripts by 
- `python <script name>.py`


Note: if you want to access webcam change value of `VIDEO_FILE` in constant.py to numeric value 0 or 1 depending on your number of camera, if you want to process the video file just change value to file name with proper path

