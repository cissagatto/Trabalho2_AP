# -*- coding: utf-8 -*-
"""Trab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b7g33hx2O3hpHQ3oFiCHXPifTiOkvxLY
"""

!pip install -U -q PyDrive
from google.colab import auth
auth.authenticate_user()

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.client import GoogleCredentials
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

myfile = drive.CreateFile({'id': '1DfCxMV1Os-_O-BZXiq0V2rhf_NZ2HioR'})
myfile.GetContentFile('train.csv')
myfile.GetContentFile('test.csv')

"""# New Section"""

import pandas as pd
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

trainData = pd.read_csv('train.csv')
testData = pd.read_csv('test.csv')

trainData.head()

testData.head()

trainPriceRange = trainData["price_range"]
trainData = trainData.drop("price_range", axis=1)

"""# Normalizando os dados"""

scaler = MinMaxScaler()
scaler.fit(trainData)
trainDataScaled = scaler.transform(trainData)
print(trainDataScaled)

kmeans = KMeans(n_clusters=4, random_state=0).fit(trainDataScaled)
print(kmeans.labels_)

import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 12))

plt.subplot(221)
plt.scatter(trainDataScaled[:, 0], trainDataScaled[:, 13], c=kmeans.labels_)
plt.title("Grafico Bateria e Memoria Ram")

# # Anisotropicly distributed data
# transformation = [[0.60834549, -0.63667341], [-0.40887718, 0.85253229]]
# X_aniso = np.dot(X, transformation)
# y_pred = KMeans(n_clusters=3, random_state=random_state).fit_predict(X_aniso)

# plt.subplot(222)
# plt.scatter(X_aniso[:, 0], X_aniso[:, 1], c=y_pred)
# plt.title("Anisotropicly Distributed Blobs")

# # Different variance
# X_varied, y_varied = make_blobs(n_samples=n_samples,
#                                 cluster_std=[1.0, 2.5, 0.5],
#                                 random_state=random_state)
# y_pred = KMeans(n_clusters=3, random_state=random_state).fit_predict(X_varied)

# plt.subplot(223)
# plt.scatter(X_varied[:, 0], X_varied[:, 1], c=y_pred)
# plt.title("Unequal Variance")

# # Unevenly sized blobs
# X_filtered = np.vstack((X[y == 0][:500], X[y == 1][:100], X[y == 2][:10]))
# y_pred = KMeans(n_clusters=3,
#                 random_state=random_state).fit_predict(X_filtered)

# plt.subplot(224)
# plt.scatter(X_filtered[:, 0], X_filtered[:, 1], c=y_pred)
# plt.title("Unevenly Sized Blobs")

plt.show()

from scipy.cluster.hierarchy import dendrogram, linkage

a = linkage(trainDataScaled, "ward")
dendrogram(a)

plt.show()

import numpy as np
import matplotlib.pyplot as plt
 
# Make a fake dataset:
height = kmeans.labels_[:100]
bars = list(range(100))

y_pos = np.arange(len(bars))
 
# Create bars
plt.scatter(y_pos, height)
 
# Show graphic
plt.show()

height = trainPriceRange[:100]
bars = list(range(100))

y_pos = np.arange(len(bars))
 
# Create bars
plt.scatter(y_pos, height)
 
# Show graphic
plt.show()

import csv

def export_csv(output_file,solution_list):
    with open(output_file, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, dialect='excel')
        w.writerow(["Expected", "Kmeans"])
        for i in range(len(solution_list[0])):
            w.writerow([solution_list[0][i],solution_list[1][i]])

# print(len(trainPriceRange))
labels = [trainPriceRange.values, kmeans.labels_]
# print(labels)
# print(labels)
export_csv("labels.csv", labels)

from sklearn import metrics

metrics.adjusted_rand_score(trainPriceRange.values, kmeans.labels_)