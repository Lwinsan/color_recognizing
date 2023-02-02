# -*- coding: utf-8 -*-
"""code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/100oBWcPABZkBzH2FYrRQ6na9PItPoHMB
"""

# import the libraries
import cv2
import imutils
import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots
import plotly.offline as py
import urllib.request

from tempfile import NamedTemporaryFile
import streamlit as st

#for image display
from PIL import Image

import webcolors
from ast import literal_eval



st.title('Recognizing Of Color Composition...')


            
##########################

upload_tab = st.tabs(["Upload"])
Image_upload = st.file_uploader("Upload Image!", type=["png", "jpg"], key="Upload_img")


if Image_upload is None:
    pass
else:
    with open(Image_upload.name,'wb') as img_up:
        img_up.write(Image_upload.read())
    K_Mean = st.slider('Define K-mean Value!', 1, 45, 15)

    col1, col2 = st.columns([1,1])
#Variable K value
#with col1:
#K_Mean = st.slider('Define K-mean Value!', 1, 45, 15)


    img = cv2.imread(Image_upload.name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    org_img = img.copy()
#print('Org image shape --> ',img.shape)


    img_up = imutils.resize(img,height=200,width=400)
#print('After resizing shape --> ',img.shape)


    flat_img = np.reshape(img_up,(-1,3))
#print('After Flattening shape --> ',flat_img.shape)

##################################################################

    kmeans = KMeans(n_clusters = K_Mean, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
#y_kmeans = kmeans.fit_predict(x)
    y_kmeans = kmeans.fit(flat_img)

    clusters_br = K_Mean

    dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')


    percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages,dominant_colors)
    p_and_c = sorted(p_and_c,reverse=True)


    bar = np.ones((50,1000,3),dtype='uint')

    start = 0
    i = 1
    for p,c in p_and_c:
        end = start+int(p*bar.shape[1])
        if i==clusters_br:
            bar[:,start:] = c[::1] #if your image is BGR count from back, -1
        else:
            bar[:,start:end] = c[::1] #if your image is BGR count from back, -1
        start = end
        i+=1

    st.subheader('Composition ofcolor, Detection with K values...')
#with col1:
    st.image(bar, caption='Colors Bar')



#####

###################################################################################
    rows = 1000
    cols = int((org_img.shape[0]/org_img.shape[1])*rows)
    img = cv2.resize(org_img,dsize=(rows,cols),interpolation=cv2.INTER_LINEAR)

    vectorized = img.reshape((-1,3))
    vectorized = np.float32(vectorized)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    K = K_Mean
    attempts=10
    ret,label,center=cv2.kmeans(vectorized,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape((img.shape))



    with col1:
        st.subheader('Color Detection with K values...')
        st.subheader(' ')
    with col1:
        st.image(result_image, caption='Segmented Image when K',channels="RGB")


###################################################################################

    x = np.reshape(img_up,(-1,3))
    print('After Flattening shape --> ',flat_img.shape)

    kmeans = KMeans(n_clusters = K_Mean, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
#y_kmeans = kmeans.fit_predict(x)
    y_kmeans = kmeans.fit(x)


# 3d scatterplot using plotly
    Scene = dict(xaxis = dict(title  = 'RED--->'),yaxis = dict(title  = 'GREEN--->'),zaxis = dict(title  = 'BLUE--->'))

# model.labels_ is nothing but the predicted clusters i.e y_clusters

    labels = kmeans.labels_
    trace = go.Scatter3d(x=x[:, 0], y=x[:, 1], z=x[:, 2], mode='markers',marker=dict(color = labels, size= 3, line=dict(color= 'black',width = 10)))
    layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 500,width = 500)
    data = [trace]
    fig = go.Figure(data = data, layout = layout)
#fig.show()
    with col2:
        st.plotly_chart(fig, use_container_width=True)


###################################################################################


    st.title(' ')
    st.title(' ')
    st.subheader('Original Image')


#Original Image
    st.image(img, caption='Original Image!',channels="RGB")




    st.subheader('Coolors Composition...')

###################################################################################

    clusters = 5
    kmeans = KMeans(n_clusters = clusters, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
#y_kmeans = kmeans.fit_predict(x)
    y_kmeans = kmeans.fit(flat_img)


#clusters = 5
#kmeans = KMeans(n_clusters=clusters,random_state=0)
#kmeans.fit(flat_img)


    dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')


    percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages,dominant_colors)
    p_and_c = sorted(p_and_c,reverse=True)


    rows = 1000
    cols = int((org_img.shape[0]/org_img.shape[1])*rows)
    img = cv2.resize(org_img,dsize=(rows,cols),interpolation=cv2.INTER_LINEAR)

    copy = img.copy()
    cv2.rectangle(copy,(rows//2-250,cols//2-90),(rows//2+250,cols//2+110),(255,255,255),-1)

    final = cv2.addWeighted(img,0.1,copy,0.9,0)
    cv2.putText(final,'Five Dominant Colors In The Scence',(rows//2-230,cols//2-40),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,0),1,cv2.LINE_AA)


    start = rows//2-220
    for i in range(clusters):
        end = start+70
        final[cols//2:cols//2+70,start:end] = p_and_c[i][1]
        cv2.putText(final,str(str(round(p_and_c[i][0]*100,1))+'%'),(start+10,cols//2+40),cv2.FONT_HERSHEY_DUPLEX,.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(final,str(str(list(p_and_c[i][1]))),(start-3,cols//2+80),cv2.FONT_HERSHEY_DUPLEX,.35,(25,25,25),1,cv2.LINE_AA)
        start = end+20

    st.image(final, caption='Dominant Color Dectected Image!',channels="RGB")

#final_img = st.image(final, caption='Dominant Color Dectected Image!',channels="RGB")

#Download

#st.download_button(label = "Download", data = final_img, file_name="final.png")

####################################################################################

    clusters = 1
    kmeans = KMeans(n_clusters = clusters, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
#y_kmeans = kmeans.fit_predict(x)
    y_kmeans = kmeans.fit(flat_img)


#kmeans = KMeans(n_clusters=clusters,random_state=0)
#kmeans.fit(flat_img)


    dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')


    percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages,dominant_colors)
    p_and_c = sorted(p_and_c,reverse=True)


    rows = 1000
    cols = int((org_img.shape[0]/org_img.shape[1])*rows)
    img = cv2.resize(org_img,dsize=(rows,cols),interpolation=cv2.INTER_LINEAR)

    copy = img.copy()
    cv2.rectangle(copy,(rows//2-250,cols//2-90),(rows//2+250,cols//2+110),(255,255,255),-1)

    final = cv2.addWeighted(img,0.1,copy,0.9,0)
    cv2.putText(final,'Most Dominant Colors In The Scence',(rows//2-230,cols//2-40),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,0),1,cv2.LINE_AA)



###################
##########
#Namming for color
    def est_color(requested_color):
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_color_name(rgb_color):
        try:
            closest_color_name = webcolors.rgb_to_name(rgb_color)
        except ValueError:
            closest_color_name = est_color(rgb_color)
        return closest_color_name

    rgb_color = list(p_and_c[0][1])
    closest_color_name = get_color_name(rgb_color)

#RGB to Hex
    def RGB2HEX(color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

    hex_colors = RGB2HEX(rgb_color)

#########
###################


    start = rows//2-220
    for i in range(clusters):
        end = 720
        final[cols//2:cols//2+70,start:end] = p_and_c[i][1]
        cv2.putText(final,str(rgb_color) + ' ' + str(hex_colors),(start+15,cols//2+45),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1,cv2.LINE_AA)
        start = end+20

    
#plt.show()

    st.image(final, caption='The Most Dominant Color Dectected Image!',channels="RGB")



################################################