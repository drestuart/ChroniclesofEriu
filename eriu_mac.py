#!/usr/bin/env python2.7-32

'''
Created on Mar 10, 2013

@author: dstu
'''

import site
import os

site.addsitedir(os.getcwd())

import Const as C
import EriuGame

import warnings
warnings.simplefilter('error')

fontsize = 14
font = u'FreeMono.otf'

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
#     os.environ['SDL_VIDEODRIVER'] = 'x11'
# x11, dga, fbcon, directfb, ggi, vgl, svgalib, aalib    

    print '-=' + C.TITLE + '=-'
    
    EriuGame.game.initialize(fontsize = fontsize, font = font, debug = True)
    
    EriuGame.game.play()

if __name__ == '__main__':
    main()
