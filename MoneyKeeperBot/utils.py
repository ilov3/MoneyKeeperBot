# coding=utf-8
import glob
import logging
import os

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


def setup_env(env_dir='envdir'):
    env_vars = glob.glob(os.path.join(env_dir, '*'))
    if env_vars:
        for env_var in env_vars:
            with open(env_var, 'r') as env_var_file:
                os.environ.setdefault(env_var.split(os.sep)[-1],
                                      env_var_file.read().strip())
