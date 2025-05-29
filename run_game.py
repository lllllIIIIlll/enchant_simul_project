import subprocess
import sys
import os
import pkg_resources

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.run([sys.executable, "game.py"])