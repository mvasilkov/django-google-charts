from distutils.core import setup

setup(
    name = 'django-google-charts',
    packages = ['googlecharts', 'googlecharts.templatetags'],
    version = '0.1',
    description = 'Google Visualization API template tags and helpers for Django framework',
    author = 'Mark Vasilkov',
    author_email = 'mvasilkov@gmail.com',
    url = 'http://publishedin.com/django-google-charts/',
    keywords = ['django', 'template', 'googlecharts'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ],
)
