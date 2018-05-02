import os
from pprint import pprint
import sys
import subprocess
from time import strftime
from urllib.request import urlopen, urlretrieve
from xml.dom.minidom import parseString


# Defines source and destination of image
rss_feed = 'https://feeds.feedburner.com/bingimages'
dst_dir = os.path.expanduser('~/Pictures/BingWallpapers/')

SET_WALLPAPER = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{0}"
end tell
END"""

NOTIFICATION = """/usr/bin/osascript<<END
display notification "{1}" with title "{0}"
END"""

APP_NAME = "Bing Daily Wallpaper"


def set_desktop_background(destination):
    subprocess.Popen(SET_WALLPAPER.format(destination), shell=True)


def send_notification(title, message):
    subprocess.Popen(NOTIFICATION.format(title, message), shell=True)


def parseFeed(rss):
    send_notification(APP_NAME, 'Updating Bing wallpaper')
    destination = "%s%s.jpg" % (dst_dir, strftime("%y-%m-%d"))
    if os.path.exists(destination):
        send_notification(APP_NAME, "Wallpaper already exist")
        sys.exit(0)
    try:
        rss_contents = urlopen(rss)
    except BaseException:
        print("Failed to read rss feed %s" % rss)
        return
    rss_src = rss_contents.read()
    rss_contents.close()
    dom = parseString(rss_src)
    pprint(dom)
    firstitem = dom.getElementsByTagName('item')[0]
    link = firstitem.getElementsByTagName('enclosure')[0].getAttribute('url')
    urlretrieve(link, destination)
    set_desktop_background(destination)
    send_notification(APP_NAME, 'Wallpaper updated !')


def main():
    if os.path.exists(dst_dir):
        parseFeed(rss_feed)
    else:
        send_notification(APP_NAME, dst_dir + ' does not exist')


if __name__ == "__main__":
    main()
