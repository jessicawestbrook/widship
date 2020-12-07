"""
A messaging application for Django
"""
# following PEP 386: N.N[.N]+[{a|b|c|rc}N[.N]+][.postN][.devN]
VERSION = (4, 0)
PREREL = ()
POST = 0
DEV = 0

# as of Django 1.7
default_app_config = 'postman.apps.PostmanConfig'


def get_version():
    version = '.'.join(map(str, VERSION))
    if PREREL:
        version += PREREL[0] + '.'.join(map(str, PREREL[1:]))
    if POST:
        version += ".post" + str(POST)
    if DEV:
        version += ".dev" + str(DEV)
    return version

__version__ = get_version()
