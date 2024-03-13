from .common import *


DEBUG = True

SECRET_KEY = 'taq%$zgh7r%#=5r7(gpk9%vf%3e%p%@ikg%z^4lt-)@b@l2fc9'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exibition',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'MyPassword'
    }
}
