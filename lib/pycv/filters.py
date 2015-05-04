#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last-Updated : <2015/05/04 15:36:07 by ymnk>

import cv2
class Filter:
    @classmethod
    def hueFilter(self,im_in,hue,hueRange):
        im_hsv = cv2.cvtColor(im_in,cv2.COLOR_BGR2HSV)
        im_dst = im_in.copy()
        im_h,im_s,im_v = cv2.split(im_hsv)
        
        im_hMask = im_h.copy()
        cv2.threshold(im_hMask,hue+hueRange,hue,cv2.THRESH_TOZERO_INV,im_hMask)
        cv2.threshold(im_hMask,hue-hueRange,hue,cv2.THRESH_BINARY, im_hMask)

        cv2.merge((im_hMask,im_s,im_v),im_hsv)
        cv2.cvtColor(im_hsv,cv2.COLOR_HSV2BGR,im_dst)
        return im_dst


def main():
    import os
    path = os.path.abspath(os.path.dirname(__file__) )
    img_fn = os.path.join(path,"../../data","A.png")
    im_in = cv2.imread(img_fn,cv2.COLOR_BGR2GRAY)
    
    im_hsv = Filter.hueFilter(im_in,110,10)
    cv2.imshow("AA",im_hsv)
    cv2.waitKey(0)
    print img_fn

if __name__  == "__main__":
    main()

