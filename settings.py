import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ART_DIR = os.path.join(BASE_DIR, 'art')

SCREEN_WIDTH = 1920 - 512
SCREEN_HEIGHT = 1080 - 256-128


DEBUG_MODE = True


# You can override the default settings by creating a local_settings.py file
try:
    from local_settings import *
except ImportError:
    print('could not load local_settings.py')
