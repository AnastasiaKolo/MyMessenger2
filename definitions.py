import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = os.path.join(ROOT_DIR, 'images')
USER_PATH = os.path.join(ROOT_DIR, 'user')
LOG_PATH = os.path.join(ROOT_DIR, 'logs')

sys.path.append(os.path.join(ROOT_DIR, 'messenger'))
sys.path.append(os.path.join(ROOT_DIR, 'ui'))
sys.path.append(os.path.join(ROOT_DIR, 'utils'))
