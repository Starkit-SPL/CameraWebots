#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

import cv2
import numpy as np
import struct
#from PIL import Image
#import pickle
import sys
import shutil
import os


class ImageMessage:
    def __init__(self, header_, image):
        self.header = header_
        self.image = image
        #self.img_dim = (self.header[-2], self.header[-1])
        #self.bpp = self.header[-3]  # bytes per pixel
        self.img_dim = (480, 640)
        self.bpp = 4  # bytes per pixel
        self.BGRA = np.frombuffer(self.image, dtype=np.uint8).reshape(*self.img_dim, self.bpp)

    def save(self, name):
        cv2.imwrite(name, self.BGRA)


    '''def Image2BGRA(self):
        self.img_dim = (self.header[-2], self.header[-1])
        self.bpp = self.header[-3] # bytes per pixel
        self.bgra = np.frombuffer(ImageMessage, dtype=np.uint8).reshape(*self.img_dim, self.bpp)'''



class ImageWebots:
    def __init__(self, sock_):
        self.sock = sock_

    def getImage(self):
        header = self.sock.recv(16)  # get 16 header bytes
        Header = struct.unpack("8sHBBHH", header)  # b'wbimage\x00', tick, self.camera.value, 4, *self.img_dim
        # print('header:', Header)
        Image = self.sock.recv(66000)
        while sys.getsizeof(Image) < 1228800:
            img = self.sock.recv(66000)
            Image += img
            #print(sys.getsizeof(img), sys.getsizeof(Image))
            #time.sleep(0.0001)
        return ImageMessage(header_=Header, image=Image[:1228800])


shutil.rmtree('./results', ignore_errors=True)
os.mkdir('./results')

sock_top = socket.socket()
sock_top.connect(('localhost', 10001))

sock_bottom = socket.socket()
sock_bottom.connect(('localhost', 10002))

print("Client start receive")
IWTop = ImageWebots(sock_=sock_top)
IWBottom = ImageWebots(sock_=sock_bottom)
count = 0
while (count < 2):
    IM = IWTop.getImage()
    IM.save('./results/image_top_{}.png'.format(count))

    IM = IWBottom.getImage()
    IM.save('./results/image_bottom_{}.png'.format(count))

    count += 1

sock_top.close()
sock_bottom.close()
print("Client end receive")
