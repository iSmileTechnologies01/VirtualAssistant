#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score,precision_score,f1_score

df=pd.read_csv('test+previous.csv')
len(df['pixel'].iloc[1].split(' '))

img_arr = df.pixel.apply(lambda x : np.array(str(x).split(' ')).astype('float32'))
img_arr_f = np.stack(img_arr,axis=0)
print(img_arr_f.shape)
img_arr_f

data=pd.DataFrame(img_arr_f)
from sklearn.preprocessing import MinMaxScaler
tr=MinMaxScaler()
tr.fit(data)
fet=pd.DataFrame(tr.transform(data))
data=pd.DataFrame(tr.transform(data))
data['res']=df.label
data

from sklearn.model_selection import train_test_split  
x_tr,x_te,y_tr,y_te=train_test_split(fet,data['res'],test_size=0.4,shuffle=True)
print(list(y_tr).count(1),list(y_te).count(1))

from sklearn import svm
model=svm.SVC(C=2.125,kernel='rbf',gamma=0.1)
model.fit(x_tr,y_tr)

import joblib
joblib.dump(model,SVM.pkl)

