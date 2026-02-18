Hand Tracking
Real-time hand tracking using OpenCV and MediaPipe. Detects up to 2 hands via webcam and draws 21 joint landmarks with a skeleton overlay.
Run it
git clone https://github.com/ace32233/hand-tracking-py.git
cd hand-tracking-py
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py

Model (25MB) auto-downloads on execution

# Requirements
Python 3.8+
Webcam
Internet connection (first run only)
