# fetchimages.py
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:02:12 2019

@author: Koutsellis Themistoklis


Description
-----------


"""

import os
import sys
import shutil
import urllib
import urllib.request

__all__ = ['fetch_images', ]


def _download_image(image_url, image_filepath, img_vol):
    '''
    Downloads an image from mage_url &
    save that image to image_filepath.
    For internal use only. Never call it
    from outside module/script.

    Arguments:
        image_url {str} -- the url of the image
        image_filepath {str} -- the filepath to save the image
    '''
    # Downloads & saves the image
    try:
        with urllib.request.urlopen(image_url) as response:
            with open(image_filepath, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                img_vol += 1
    except Exception as ex:
        # We only need to print a msg when an exception occurs,
        # and then exit the script. Therefore, in that case,
        # we can use a general Exception to catch cases such as:
        # -wrong URL- web page not availalbe -
        # -no internet connection-denied access to URL-file etc.
        print("\n>> Operation failed with the following error: ", ex, '\n')
        sys.exit(1)
    else:
        return img_vol


def fetch_images(img_url_file, *target_path):
    '''
    This is the main function of the module.
    Reads the URLs from img_url_file and saves
    the images to target_path. In case target_path
    is not given, it saves all images to the dir
    where the script/module lies on.

    Arguments:
        img_url_file {path-str} -- the path of file with URLs
        *target_path {path-str} -- the filepath where to save the images
    '''
    # img_vol (:images' volume)
    img_vol = 0

    #  checks if target_path arg is acceptable
    if len(target_path) == 0:
        # No target_path given
        _target_path = os.path.dirname(__file__)
    elif len(target_path) == 1 and target_path[0]:
        # 1 valid target_path is given
        _target_path = target_path[0]
    else:
        # None or more than 1 target_path given
        print('Number of arguments given: {}'.format(len(target_path)+1))
        print('Maximum number of arguments is 2.')
        sys.exit(1)

    # opens the input text file and reads it line ny line
    try:
        with open(img_url_file) as file:
            # The following line opens the file to read the URLs
            file.seek(0)
            lines = (row for row in file)

            # This for loop activates/consumes the generator
            for line in lines:
                _image_url = line.rstrip()
                _image_name = _image_url.rsplit('/', 1)[-1]
                _image_filepath = os.path.abspath(os.path.join(_target_path,
                                                               _image_name
                                                               )
                                                  )
                img_vol = _download_image(_image_url, _image_filepath, img_vol)
    except Exception as ex:
        # We only need to print a msg when an exception occurs,
        # and then exit the script. Therefore, in that case,
        # we can use a general Exception to catch cases such as:
        # -wrong URL- web page not availalbe -
        # -no internet connection-denied access to URL-file etc.
        print("\n>> Operation failed with the following error: ", ex, '\n')
        sys.exit(1)
    else:
        # Successful executions. Prints logs.
        print('\n~~~~~~~~~~~ * ~~~~~~~~~~~')
        print('\nfetch_images() terminated successfully!')
        print('\nSaved {} images to {} '.format(img_vol, _target_path), '\n')
        return img_vol


if __name__ == '__main__':
    IMG_URL_FILE = "imgUrlFile.txt"
    fetch_images(IMG_URL_FILE,)
