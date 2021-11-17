from distutils.core import setup

import golipy

DESC = 'A Game of Life implementation in Python'
LONG_DESC = open('README.md').read()

setup(
    name='golipy',
    version=golipy.__version__,
    description=DESC,
    license='GPLv3+',
    author='Alberto Díaz',
    author_email='alberto.da@gmail.com',
    url='https://github.com/blazaid/golipy',
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    packages=['golipy', 'golipy.resources'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Software Development :: Libraries :: pygame',
    ],
    python_requires='>=3.7',
    tests_require=[],
    install_requires=['pygame'],
)
