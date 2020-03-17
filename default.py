import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import requests
import datetime
import re

#==========================#

addon = xbmcaddon.Addon('context.fanart.dl')
addon_id = addon.getAddonInfo('id')
addon_path = addon.getAddonInfo('path')
icon_path = imagesPath = os.path.join(addon_path, 'resources', 'images', 'icon.png')
dialog = xbmcgui.Dialog()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

#==========================#

class FanartDL:

    def __init__(self, *args, **kwargs):
        self.folder_path = addon.getSetting('FolderPath')
        self.file_path = None
        self.file_name = None
        self.fanart_url = None
        self.fanart_label = None
    
    #==========================#

    def setFolderPath(self):
        if self.folder_path is 'Not Set' or not os.path.exists:
            xbmc.executebuiltin('Addon.OpenSettings({})'.format(addon_id))

    #==========================#

    def getFanartUrl(self):
        try:
            self.fanart_url = xbmc.getInfoLabel('Listitem.Art(fanart)')
            self.fanart_label = xbmc.getInfoLabel('Listitem.Title')
            self.isValidUrl()
            if not (self.fanart_url and self.fanart_label and self.isValidUrl()):
                self.exit()
        except:
            self.exit()

    #==========================#

    def isValidUrl(self):
        request = requests.get(self.fanart_url, headers={'User-Agent': user_agent})
        return request.status_code == 200

    #==========================#

    def createPaths(self):
        try:
            file_name, file_extension = os.path.splitext(self.fanart_url)
            self.fanart_label = re.sub('[^0-9a-zA-Z]+', '.', self.fanart_label).title() + '-'
            self.file_name = self.fanart_label + str(datetime.date.today()) + file_extension
            self.file_path = os.path.join(self.folder_path, self.file_name)
        except:
            self.exit()

    #==========================#

    def downloadImage(self):
        try:
            with open(self.file_path, 'wb') as file:
                request = requests.get(self.fanart_url, stream=True, headers={'User-Agent': user_agent})
                for chunk in request.iter_content(1024):
                    file.write(chunk)
                dialog.notification('Fanart DL', 'Image Saved Successfully.', icon_path, 3000)
        except:
            dialog.notification('Fanart DL', 'Unable To Save Image', icon_path, 3000)
            sys.exit()


    #==========================#

    def exit(self):
        dialog.notification('Fanart DL', 'No Image Available', icon_path, 3000)
        sys.exit()

#==========================#

if __name__ == '__main__':
    dl = FanartDL()
    dl.setFolderPath()
    dl.getFanartUrl()
    dl.createPaths()
    dl.downloadImage()
