# from ultralytics import YOLO
# import cv2
# import traceback
import ctypes
import os
try:
    if os.path.exists('C:\\Users\\Marc\\Documents\\GitHub\\IA-MarcJosep\\Projecte2\\venv\\Lib\\site-packages\\cv2\\opencv_videoio_ffmpeg4110_64.dll'):
        ctypes.CDLL('C:\\Users\\Marc\\Documents\\GitHub\\IA-MarcJosep\\Projecte2\\venv\\Lib\\site-packages\\cv2\\opencv_videoio_ffmpeg4110_64.dll')
        import cv2
except OSError as e:
    print(f'DLL: {e}')


# print(cv2.__version__)

# model = YOLO('yolov8n.pt')