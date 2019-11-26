# coding: utf-8
import os
import sys
import platform


def default_sdk_home():
    osname = platform.system()
    if osname == 'Linux':
        return "/opt/zzq/resources/zzqc"
    elif osname == 'Darwin':
        return "/Applications/zzq.app/Contents/Resources/zzqc"
    elif osname == 'Windows':
        return "C:\\Program Files\\zzq\\resources\\zzqc"


def setup_environment_variables():
    if not getattr(sys, 'frozen', False):
        if not hasattr(sys, 'zzq_sdk_home'):
            sys.zzq_sdk_home = default_sdk_home()
        sys.path.append(sys.zzq_sdk_home)
        os.environ['PATH'] = sys.zzq_sdk_home + os.pathsep + os.environ['PATH']