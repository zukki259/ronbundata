#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yuya
#
# Created:     18/09/2018
# Copyright:   (c) yuya 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
import sys
from PIL import Image
import os

height=500
width=500
def create_model():
    from keras.layers import Input, Dense,Conv2D,Concatenate,Reshape
    from keras.models import Model
    inputs=Input(shape=(height,width))
    data=Reshape((height,width,1))(inputs)
    #import pdb;pdb.set_trace()
    columns=Conv2D(width,height,strides=(1,height),activation='sigmoid')(data)
    rows=Conv2D(width,height,strides=(width,1),activation='sigmoid')(data)
    c_=Reshape((width,))(columns)
    r_=Reshape((height,))(rows)
    cr=Concatenate()([c_,r_])
    outputs=Dense(1,activation='sigmoid')(cr)
    model=Model(inputs=inputs,outputs=outputs)
    model.compile(optimizer='adagrad',
              loss='cosine_proximity',
              metrics=['accuracy'])
    model.summary()
    return model

def image_makedata(filename):
    im=Image.open(filename)
    #to brightness
    im=im.convert('L')
    im=im.resize((width,height))
    data=[]
    for j in range(height):

        column=[]
        for i in range(width):
            column.append(1.-im.get_pixel((i,j))/255)
        data.append(column)
    data=np.array(data)
    return data



def main():
    pass

if __name__ == '__main__':
    create_model()
