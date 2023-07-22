import numpy as np
import pandas as pd

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings('ignore')

def train():
    global scaler, pca, k2
    df = pd.DataFrame(pd.read_csv("SleepStudyData.csv"))

    df_categorical = df[['Enough', 'PhoneReach', 'PhoneTime', 'Breakfast']]
    df_numeric = df[['Hours', 'Tired']]

    le = preprocessing.LabelEncoder()
    df_categorical = df_categorical.apply(le.fit_transform)

    scaler = StandardScaler()
    df_numeric = scaler.fit_transform(df_numeric)
    df_numeric = pd.DataFrame(df_numeric, columns=['Hours', 'Tired'])
    df_final = pd.concat([df_numeric, df_categorical], axis=1, join='inner')

    pca = PCA(n_components = 2)
    X_principal = pca.fit_transform(df_final)
    X_principal = pd.DataFrame(X_principal)
    X_principal.columns = ['P1', 'P2']

    k2 = KMeans(n_clusters=4, random_state=9)
    k2.fit(X_principal)
    
def predicts(input):
    df_numeric = pd.DataFrame(input[:2]).T
    df_numeric.columns = ["Hours",	"Tired"]

    df_numeric = scaler.transform(df_numeric)
    df_numeric = pd.DataFrame(df_numeric, columns=['Hours', 'Tired'])

    df_categorical = pd.DataFrame(input[2:]).T
    df_categorical.columns = ['Enough', 'PhoneReach', 'PhoneTime', 'Breakfast']

    df_final = pd.concat([df_numeric, df_categorical], axis=1, join='inner')

    df_final = pca.transform(df_final)

    prediction = int(k2.predict(df_final)[0])
    return prediction

#train()
#predict([8, 3, 0, 1, 1, 0])