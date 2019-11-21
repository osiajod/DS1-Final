import pandas as pd
import sklearn
from matplotlib import pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LassoCV

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import multilabel_confusion_matrix
import numpy as np

import statsmodels.api as sm
from statsmodels.api import OLS

crime_property_light_population = pd.read_csv("./model_data/crime_light_density.csv")
crime_property_light_population.head()

resp_predictors = ['OFFENSE_CODE_GROUP', 'SHOOTING', 'MONTH', 'DAY_OF_WEEK', 'HOUR',
                   'Population density (per square mile of land area)', 'BLDG_VAL', 'LAND_VAL', 'light_density']
df = crime_property_light_population[resp_predictors]
df = df.dropna()

# Let's label encode & one-hot encode the Categoricals (SHOOTING, DAY_OF_WEEK)

enc = OneHotEncoder(handle_unknown='ignore')

le = LabelEncoder()

df['SHOOTING'] = le.fit_transform(df['SHOOTING'])
df['DAY_OF_WEEK'] = le.fit_transform(df['DAY_OF_WEEK'])
df['OFFENSE_CODE_GROUP'] = le.fit_transform(df['OFFENSE_CODE_GROUP'])

df_cat = enc.fit_transform(df[["MONTH", "SHOOTING", "DAY_OF_WEEK"]]).toarray()

df_cat = pd.DataFrame(df_cat, columns=enc.get_feature_names(['MONTH', 'SHOOTING', 'DAY_OF_WEEK']))
df = pd.concat([df, df_cat], axis=1)
df = df.dropna()

df.head()

X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns != 'OFFENSE_CODE_GROUP'],
                                                    df.OFFENSE_CODE_GROUP, test_size=0.2,
                                                    random_state=109,
                                                    stratify=df.OFFENSE_CODE_GROUP)

y_train = np.array(y_train)
y_test = np.array(y_test)

display(X_train.head())
print(type(y_train))
print(y_train)

# Let's scale the variables
min_max_scaler = MinMaxScaler()
numerical = ["HOUR", "BLDG_VAL", "LAND_VAL", "light_density", "MONTH",
             "Population density (per square mile of land area)"]
X_normalized = (X_train - X_train.min(axis=0)) / (X_train.max(axis=0) - X_train.min(axis=0))
min_max_scaler.fit(X_train)
X_normalized_tst = pd.DataFrame(min_max_scaler.transform(X_test))
X_normalized_tst.columns = X_test.columns

display(X_normalized.head())
display(X_normalized_tst.head())

# Let's first start with Logistic Model

logreg = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', max_iter=1000)
logreg.fit(X_normalized, y_train)
y_pred = logreg.predict(X_normalized_tst)

mcm = multilabel_confusion_matrix(y_test, y_pred, sample_weight=None, labels=None, samplewise=False)
# logreg.score(X_normalized, y_test)
# print(mcm)

print(y_pred[:10])
print(y_test[:10])

knn = KNeighborsClassifier(n_neighbors=7).fit(X_normalized, y_train)

# accuracy on X_test
accuracy = knn.score(X_normalized_tst, y_test)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print(cm)

import pickle

pickle.dump(logreg, open('logreg.sav', 'wb'))
pickle.dump(knn, open('knn.sav', 'wb'))