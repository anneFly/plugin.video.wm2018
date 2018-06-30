import sys
from urllib import urlencode
from urlparse import parse_qsl, urlparse
import xbmc
import xbmcgui
import xbmcplugin


# 3 arguments are passed to the script:
# - plugin url in plugin:// notation
# - plugin handle
# - url parameters
base_url = sys.argv[0]
handle = int(sys.argv[1])
paramstring = sys.argv[2]

# convert url params to dict
params = dict(parse_qsl(urlparse(paramstring).query))


STREAM_CONFIG = {
    'ard': {
        'name': 'Sportschau live',
        'stream_url': 'https://wm2018.akamaized.net/hls/live/625036/wm2018/master.m3u8',
    },
    'one': {
        'name': 'One live',
        'stream_url': 'https://onelivestream-lh.akamaihd.net/i/one_livestream@568814/index_7_av-p.m3u8'
    },
    'zdf': {
        'name': 'ZDF live',
        'stream_url': 'https://zdf1314-lh.akamaihd.net/i/de14_v1@392878/index_3096_av-p.m3u8',
    },
    'zdf_info': {
        'name': 'ZDF Info live',
        'stream_url': 'https://zdf1112-lh.akamaihd.net/i/de12_v1@392882/master.m3u8',
    },
}


def get_url(**kwargs):
    return '{}?{}'.format(base_url, urlencode(kwargs))


def list_videos():
    xbmcplugin.setContent(handle, 'videos')

    for stream_id, conf in STREAM_CONFIG.items():
        title = conf['name']
        video_settings = {
            'title': title,
            'mediatype': 'video',
        }

        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', video_settings)

        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?stream_id=ard
        url = get_url(stream_id=stream_id)

        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=False)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(handle)


def play_video(stream_id):
    stream = STREAM_CONFIG[stream_id]
    list_item = xbmcgui.ListItem(label=stream['name'])
    url = stream['stream_url']

    # we use xmbc.PLayer() instead of xbmcplugin.setResolvedUrl()
    # because it seems to work better than xbmcplugin.setResolvedUrl()
    xbmc.Player().play(url, list_item)


if __name__ == '__main__':
    # Check the parameters passed to the plugin
    if params and params.get('stream_id'):
        play_video(params['stream_id'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_videos()
