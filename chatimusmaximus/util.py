import os
import sys
try:
    import httplib2

    from apiclient.discovery import build
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client.tools import run_flow, argparser
except ImportError:
    pass

from chatimusmaximus.plugin_wrapper import PluginWrapper


def create_services_from_settings(settings, modules: dict):
    # don't want to pass these arguments in
    _rm_arguments = ['connect', 'display_missing']
    # we're going to return these bad boys at the end
    plugin_wrappers = []
    addresses = []

    # need the name of service to check to see if `youtube`
    # service is the platform dict
    for name, service in settings['services'].items():
        # run this code if it's not youtube
        if not name == 'youtube':
            # the python file that we're going to run is the same
            # as the `name` attribute (I.E. irc, xmpp, etc.)
            module = modules[name]
            # Let's grab the actual values now. `platform` is the
            # name of the platform. (I.E. twitch, livecoding, etc)
            for platform, platform_settings in service.items():
                # check to see if we want to connect or not.
                if not platform_settings['connect']:
                    continue
                # we're returning a list of all the socket addresses
                addresses.append(platform_settings['socket_address'])
                # PluginWrapper abstracts out the subprocess lib for us
                plugin_wrapper = PluginWrapper(module)
                # create kwargs with every value having a `--` in front of it
                kwargs = {'--' + key: value
                          for (key, value)
                          in platform_settings.items()
                          if key not in _rm_arguments}

                # add in the service name to kwargs
                kwargs['--service_name'] = platform
                # activate the plugin wrapper and append it to the list
                plugin_wrapper.activate(invoke_kwargs=kwargs)
                plugin_wrappers.append(plugin_wrapper)
        # this is the youtube parsing.
        else:
            if not service['connect']:
                continue
            addresses.append(service['socket_address'])
            client_secrets_file = service['api_connect']['client_secrets_file']
            if client_secrets_file and not client_secrets_file == "":
                print('activating the youtube api!')
                plugin_wrapper = PluginWrapper(modules['youtube_api'])
                kwargs = {'--client_secret_filepath': client_secrets_file,
                          '--socket_address': service['socket_address']}
            else:
                url = service['javascript_scraper']['youtube_url']
                kwargs = {'--url': url,
                          '--comment_element_id': 'all-comments',
                          '--author_class_name': 'yt-user-name',
                          '--message_class_name': 'comment-text',
                          '--socket_address': service['socket_address'],
                          '--service_name': 'youtube'}
                module = modules['javascript_webscraper']
                plugin_wrapper = PluginWrapper(module)
            plugin_wrapper.activate(invoke_kwargs=kwargs)
            plugin_wrappers.append(plugin_wrapper)

    return plugin_wrappers, addresses


_YOUTUBE_API_SERVICE_NAME = 'youtube'
_YOUTUBE_API_VERSION = 'v3'
_READ_ONLY = "https://www.googleapis.com/auth/youtube.readonly"


def youtube_authentication(client_filepath, youtube_scope=_READ_ONLY):
    missing_client_message = "You need to populate the client_secrets.json!"
    flow = flow_from_clientsecrets(client_filepath,
                                   scope=youtube_scope,
                                   message=missing_client_message)

    filepath = "{}-oauth2.json".format(sys.argv[0])
    # remove old oauth files to be safe
    if os.path.isfile(filepath):
        os.remove(filepath)

    storage = Storage(filepath)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, argparser.parse_args())
        return build(_YOUTUBE_API_SERVICE_NAME,
                     _YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))


def _get_youtube_link(client_secrets_filepath):
    youtube_api = youtube_authentication(client_secrets_filepath)
    parts = 'id, snippet, status'
    livestream_requests = youtube_api.liveBroadcasts().list(mine=True,
                                                            part=parts,
                                                            maxResults=5)

    while livestream_requests:
        response = livestream_requests.execute()
        # TODO: add better parsing here
        youtube_id = response.get('items', [])[0]['id']
        return 'http://youtube.com/watch?v={}'.format(youtube_id)
