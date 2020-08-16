# [Toy Project NYSCEC]
# 0.1.2va, 20.07.31. First launched.
# written by acoustikue(SukJoon Oh)
# 
# Legal stuff:
#   This simple code follows MIT license. 
# 
# MIT License
# Copyright (c) 2020 SukJoon Oh(acoustikue)

# This file contains essential settings information. 
# The file should be modified as for individual use.

NYSCEC_LOGIN_PARAM = {
    'username': 'your_id',
    'password': 'your_password'
    }

NYSCEC_BASE = 'https://yscec.yonsei.ac.kr'
NYSCEC_LOGIN_INDEX = 'https://yscec.yonsei.ac.kr/login/index.php'

NYSCEC_COURSE_URL = 'https://yscec.yonsei.ac.kr/course/view.php'

NYSCEC_SPLOGIN = 'https://yscec.yonsei.ac.kr/passni/sso/spLogin.php'
NYSCEC_SPLOGIN_DATA = 'https://yscec.yonsei.ac.kr/passni/sso/spLoginData.php'
NYSCEC_SPLOGIN_PROCESS = 'https://yscec.yonsei.ac.kr/passni/spLoginProcess.php'

NYSCEC_PMSSO_SERVICE = 'https://infra.yonsei.ac.kr/sso/PmSSOService'
NYSCEC_PMSSOAUTH_SERVICE = 'https://infra.yonsei.ac.kr/sso/PmSSOAuthService'

NYSCEC_MY = 'https://yscec.yonsei.ac.kr/my/'


# Instance types
NYSCEC_INSTANCE_TYPE_1 = ['jinotechboard']
NYSCEC_INSTANCE_TYPE_2 = [
        'textbook', 'resource', 'turnitintooltwo', 'assign', 'lcm'
        ]



# for import from parent directory
import sys, os
sys.path.append( 
    os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))) )

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
elif __file__:
    BASE_DIR = os.path.dirname(__file__)

NYSCEC_LOG_BASE = BASE_DIR + '/' # Linux
NYSCEC3_DB_BASE = BASE_DIR + '/'
if sys.platform.startswith('win'):
    NYSCEC_LOG_BASE = BASE_DIR + '\\'
    NYSCEC3_DB_BASE = BASE_DIR + '\\'


# For tests on Windows
# WEBDRIVER_DIR = BASE_DIR + '\\webdriver\\'
# FIREFOX_WEBDRIVER = WEBDRIVER_DIR + 'geckodriver.exe'
FIREFOX_WEBDRIVER = BASE_DIR + './webdriver/geckodriver'

if sys.platform.startswith('win'): 
    NYSCEC_LOG_BASE += 'log\\'
    NYSCEC3_DB_BASE += 'db\\'
else: 
    NYSCEC_LOG_BASE += 'log/'
    NYSCEC3_DB_BASE += 'db/'

# First!!
# Make directory if there is no db folder
if not(os.path.isdir(NYSCEC_LOG_BASE)): os.makedirs(os.path.join(NYSCEC_LOG_BASE))
if not(os.path.isdir(NYSCEC3_DB_BASE)): os.makedirs(os.path.join(NYSCEC3_DB_BASE))

import time
 
NYSCEC_RUN = time.localtime()
NYSCEC_RUNT = "%04d.%02d.%02d._%02d-%02d-%02d" % (NYSCEC_RUN.tm_year, NYSCEC_RUN.tm_mon, NYSCEC_RUN.tm_mday, NYSCEC_RUN.tm_hour, NYSCEC_RUN.tm_min, NYSCEC_RUN.tm_sec)
del NYSCEC_RUN


#
# STMP account infos









