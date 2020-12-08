import cv2       
import numpy as np
import pandas as pd
import time

def smoothing(img):
    img=cv2.medianBlur(img,3)
    #img=cv2.bilateralFilter(img,3,75,75)     ##9 邻域直径，两个 75 分别是空间高斯函数标准差，灰度值相似性高斯函数标准差
    return img

def bianyuan_canny(img,blurparam):
    img_mohu=cv2.blur(img,(blurparam,blurparam))
    img_v=cv2.Canny(img_mohu,100,200)
    return img_v

def cutoffedge(img,edge):
    img_x=img.copy()
    for i in range(len(img_x)):
        for j in range(len(img_x[0])):
            if img[i][j]==0 and edge[i][j]==255:
                img_x[i][j]=255
    return img_x

def get_HBG(img):
    sum=0
    for i in range(len(img)):
        for j in range(len(img[0])):
            sum+=int(img[i][j][0])

    result=int(sum/len(img)/len(img[0]))
    return result

def get_HL(hbg,l):
    result=int(hbg+(3-l)*pow(-1,l)*255/10)
    return result

def bianyuan_selfmade(img):
    img_copy=img.copy()
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j]==255:
                img_copy[i][j]=0
            else:
                if i>=1 and i<=len(img)-2 and j>=1 and j<=len(img[0])-2:
                    sum=int(img[i-1][j-1])+int(img[i-1][j])+int(img[i-1][j+1])+int(img[i][j-1])+int(img[i][j+1])+int(img[i+1][j-1])+int(img[i+1][j])+int(img[i+1][j+1])
                    if sum!=0:
                       img_copy[i][j]=255

    return img_copy

def convert(img,img1,img2,img3,HBG,HL_1,HL_2,HL_3,k):
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i][j][0]>=127):
                img[i][j][0]=HBG-50
                img[i][j][1]=HBG-50
                img[i][j][2]=HBG-50
                #img[i][j][0]=127
                #img[i][j][1]=127
                #img[i][j][2]=127
            else:
                if(img1[i][j]==255):
                    img[i][j][0]=HL_1
                    img[i][j][1]=HL_1
                    img[i][j][2]=HL_1
                elif(img2[i][j]==255):
                    img[i][j][0]=HL_2
                    img[i][j][1]=HL_2
                    img[i][j][2]=HL_2
                elif(img3[i][j]==255):
                    img[i][j][0]=HL_3
                    img[i][j][1]=HL_3
                    img[i][j][2]=HL_3
                elif(int((i/k))%2 == int((j/k))%2 ):
                    img[i][j][0]=0
                    img[i][j][1]=0
                    img[i][j][2]=0
                else:
                    img[i][j][0]=255
                    img[i][j][1]=255
                    img[i][j][2]=255

def HideText(img,center_x,center_y,x_size,y_size,bianyuan_mode=0,blurparam=3,smoothing=0,k=3):

    # parameters setting
    BIANYUAN_MODE=bianyuan_mode            #  0 for cv2.canny ; 1 for methods mentioned in paper
    BLURPARAM=blurparam                               #  param for blur-preposing in cv2.canny
    SMOOTHING=smoothing                               #  0 for not smoothing ;  1 for smoothing
    K=k                                                                  # the size of black and white blocks

    # coord transform
    ROW=img.shape[0]
    COL=img.shape[1]
    CENTER_ROW=int(ROW*center_y)
    CENTER_COL=int(COL*center_x)
    X_SIZE=int(COL*x_size)
    Y_SIZE=int(ROW*y_size)



    # get the square area
    P1_ROW=int(CENTER_ROW-Y_SIZE/2)
    P1_COL=int(CENTER_COL-X_SIZE/2)
    P2_COL=int(CENTER_COL+X_SIZE/2)
    P3_ROW=int(CENTER_ROW+Y_SIZE/2)


    # prepare the gray img
    img_square=img[P1_ROW:P3_ROW,P1_COL:P2_COL]
    img_gray=cv2.cvtColor(img_square, cv2.COLOR_BGR2GRAY)


    # fisrt layer
    if BIANYUAN_MODE==0:
        edge_one=bianyuan_canny(img_gray,BLURPARAM)
    if BIANYUAN_MODE==1:
        edge_one=bianyuan_selfmade(img_gray)
    img_v1=cutoffedge(img_gray,edge_one)
    if SMOOTHING==1:
        img_v1=smoothing(img_v1)

    # second layer
    if BIANYUAN_MODE==0:
        edge_two=bianyuan_canny(img_v1,BLURPARAM)
    if BIANYUAN_MODE==1:
        edge_two=bianyuan_selfmade(img_v1)
    img_v2=cutoffedge(img_v1,edge_two)
    if SMOOTHING==1:
        img_v2=smoothing(img_v2)

    # third layer 
    if BIANYUAN_MODE==0:
        edge_three=bianyuan_canny(img_v2,BLURPARAM)
    if BIANYUAN_MODE==1:
        edge_three=bianyuan_selfmade(img_v2)
    
    # get the result
    HBG=get_HBG(img_square)
    HL_1=get_HL(HBG,1)
    HL_2=get_HL(HBG,2)
    HL_3=get_HL(HBG,3)

    convert(img_square,edge_one,edge_two,edge_three,HBG,HL_1,HL_2,HL_3,K)

    # pinjie
    img[P1_ROW:P3_ROW,P1_COL:P2_COL]=img_square

    cv2.imwrite("static/assets/img/handle.png", img)
    # return img


## example
#img=cv2.imread('C:/Users/user/Desktop/demo5.bmp')
#cv2.imshow("origin",img)
#cv2.waitKey(0)
#begin_time=time.time()
#img2=HideText(img,0.5,0.5,0.5)
#end_time=time.time()
#cv2.imshow("after",img2)
#cv2.waitKey(0)

#print("Hide Text process time:{}".format(end_time-begin_time))      # 0.1825122833251953s


#img=cv2.imread('C:/Users/user/Desktop/keyboard/8.bmp')
##img=cv2.imread('C:/Users/user/Desktop/demo5.bmp')
#cv2.imshow("origin",img)
#cv2.waitKey(0)
#img2=HideText(img,0.5,0.5,1,1,bianyuan_mode=0)
#cv2.imshow("after",img2)
#cv2.waitKey(0)