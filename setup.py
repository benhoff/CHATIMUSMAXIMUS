import os
from setuptools import find_packages, setup


# directory = os.path.abspath(os.path.dirname(__file__))
"""
with open(os.path.join(directory, 'README.rst')) as f:
    long_description = f.read()
"""

setup(
    name="chatimusmaximus",
    version='0.1.1',
    description='Chat GUI for youtube, twitch, livecoding, and WatchPeopleCode chats',
    # long_description=long_description,
    url='https://github.com/benhoff/chatimusmaximus',
    license='GPL3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Operating System :: OS Independent'],
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    entry_points={'vexbot.plugins': ['chatimusmaximus = chatimusmaximus.__main__'],
                  'gui_scripts': ['chatimusmaximus = chatimusmaximus.__main__:main']},

    packages= find_packages(), # exclude=['docs', 'tests']
    package_data={'chatimusmaximus': ['default_settings.yml', 'gui/resources/click.wav', 'gui/resources/icons/*', 'gui/resources/buttons/*']},

    install_requires=[
        'pyzmq',
        'PyYAML',
        'pYqT5',
        'Quamash',
        'vexbot',
        ],

    extras_require={
        'dev': ['flake8'],
        },
)
