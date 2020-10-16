
import os
from os.path import join as pjoin
from pathlib import Path
import configparser


class Config(object):
    BASE_DIR = Path(__file__).parent
    ROOT_DIR = BASE_DIR.parent
    DATABASE_PATH = pjoin(ROOT_DIR, 'database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    configparser = configparser.ConfigParser(interpolation=None)
    configparser.read(pjoin(ROOT_DIR, 'secret.ini'))
    SECRET_KEY = r'{}'.format(configparser['app']['SECRET_KEY'])
