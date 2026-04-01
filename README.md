# Accident Detection

Watches a webcam feed and emails you when it spots an accident. Runs on a Raspberry Pi 3 Model B+.

The model (InceptionV3-based, saved as `Accident.h5`) classifies each frame as either "Accident" or "Neutral". If it predicts an accident for 20 frames in a row, it saves a screenshot and sends it to the configured recipients.

## Files

```
.
├── Accident.h5      — trained Keras model
├── labels.txt       — class labels (0 = Accident, 1 = Neutral)
├── test.py          — live webcam detection and email alert
├── detect.py        — single-image inference script
└── .env.example     — copy this to .env and fill in your values
```

## Setup

```bash
pip install tensorflow keras opencv-python pillow python-dotenv
```

Copy `.env.example` to `.env` and fill it in:

```
SENDER_ADDRESS=your_email@gmail.com
SENDER_PASS=your_app_password
RECEIVER_ADDRESSES=alert1@example.com,alert2@example.com
ALERT_LOCATION=Lawspet, Puducherry
```

Gmail requires an App Password, not your account password: https://support.google.com/accounts/answer/185833

## Run

```bash
python test.py
```

Press `q` to quit. On Raspberry Pi, `cv2.VideoCapture(0)` works for a USB webcam. For the Pi Camera use V4L2.

## Test on a single image

Edit the `Image.open(...)` path in `detect.py`, then:

```bash
python detect.py
```
