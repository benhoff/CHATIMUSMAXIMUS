import os
from setuptools import find_packages, setup


# directory = os.path.abspath(os.path.dirname(__file__))
"""
with open(os.path.join(directory, 'README.rst')) as f:
    long_description = f.read()
"""

setup(
    name="chatimusmaximus",
    version='0.0.8',
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
    entry_points={'chatimusmaximus.communication_protocols': ['irc = chatimusmaximus.communication_protocols.irc',
                                                              'javascript_webscraper = chatimusmaximus.communication_protocols.javascript_webscraper',
                                                              'xmpp = chatimusmaximus.communication_protocols.xmpp',
                                                              'socket_io = chatimusmaximus.communication_protocols.socket_io',
                                                              'youtube_api = chatimusmaximus.communication_protocols.youtube_api'],

                  'vexbot.plugins': ['chatimusmaximus = chatimusmaximus.__main__'],

                  'gui_scripts': ['chatimusmaximus = chatimusmaximus.__main__:main']},
                                                              #'youtube = chatimusmaximus.communication_protocols.client']},

    packages= find_packages(), # exclude=['docs', 'tests']
    package_data={'chatimusmaximus': ['default_settings.yml', 'gui/resources/click.wav', 'gui/resources/icons/*', 'gui/resources/buttons/*']},

    install_requires=[
        'pluginmanager',
        'pyzmq',
        'PyYAML',
        ],

    extras_require={
        'gui': ['Quamash'],
        'dev': ['flake8'],
        'javascript_webscrapper': ['selenium'],
        'irc': ['irc3'],
        'socket_io': ['requests', 'websocket-client'],
        'xmpp': ['slixmpp', 'dnspython3'],
        'youtube': ['google-api-python-client'],
        },
)
