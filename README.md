# Accident Detection System

Real-time road accident detection using a webcam feed and a trained Keras model. When an accident is detected, the system captures a screenshot and sends an email alert with the image attached.

Built and tested on **Raspberry Pi 3 Model B+**.

## How It Works

1. Captures live video from the connected camera (webcam or Pi Camera via V4L2)
2. Each frame is passed through a trained InceptionV3-based Keras model (`Accident.h5`)
3. If an accident is predicted with >50% confidence for 20 consecutive frames, it triggers an alert
4. An email is sent to the configured recipients with a screenshot and the configured location name

## Project Structure

```
.
├── Accident.h5          # Trained Keras model (InceptionV3-based)
├── labels.txt           # Class labels: 0 = Accident, 1 = Neutral
├── detect.py            # Single-image inference script
├── test.py              # Live webcam detection + email alert
├── .env.example         # Environment variable template
└── README.md
```

## Requirements

- Python 3.7+
- Raspberry Pi 3 Model B+ (or any machine with a webcam)
- Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) enabled

Install dependencies:

```bash
pip install tensorflow keras opencv-python pillow python-dotenv
```

## Setup

1. Clone the repo and enter the directory:
   ```bash
   git clone https://github.com/YOUR_USERNAME/accident-detection.git
   cd accident-detection
   ```

2. Copy the environment template and fill in your values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   SENDER_ADDRESS=your_email@gmail.com
   SENDER_PASS=your_app_password
   RECEIVER_ADDRESSES=alert1@example.com,alert2@example.com
   ALERT_LOCATION=Lawspet, Puducherry
   ```

3. Place the `Accident.h5` model file in the project root (not included in the repo due to size).

4. Run:
   ```bash
   python test.py
   ```

   Press `q` to quit.

## Single-Image Test

To test the model on a static image:

```bash
python detect.py
```

Edit the `image = Image.open(...)` line in `detect.py` to point to your image.

## Notes

- The `.env` file is gitignored — never commit it
- Gmail requires an **App Password**, not your regular account password
- On Raspberry Pi, use `cv2.VideoCapture(0)` for USB webcam or configure V4L2 for Pi Camera
