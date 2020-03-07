# -*- coding: utf-8 -*-

name = 'tk_core'

version = "0.19.2"

description = 'tk-core'

authors = ['ShotgunSoftware']

tools = []

requires = [
    'python-2.7',
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env.SGTK_CORE_ROOT = "{root}"
    env.PYTHONPATH.append("{root}/python")
    env.RV_TK_CORE = "{root}"
    env.SG_CONFIG_FILE = '{root}/config/core/shotgun.yml'


format_version = 2
