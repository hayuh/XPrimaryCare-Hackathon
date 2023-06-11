from app import df

import numpy as np
import pandas as pd
import bidict
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle


TARGET_COLUMN_NAME = 'NDC_CODE'
X_LABELS = [f'DIAGNOSIS_CODE_{i}' for i in range(1, 26)] + ['PAID_AMOUNT']

df_original = df.copy(deep=True)
y_original = df_original.loc[:,TARGET_COLUMN_NAME]

# Encode strings as ints because sklearn classifiers can only operate on ints.
# I would use pd.get_dummies(df) except it uses too much memory and crashes.
# There are probably better solutions inside sklearn.preprocessing but
# I don't have the time to learn.

# encoder_pickle is a bidict mapping the strings in the data to ints for classification.
# model_pickle is the trained machine learning model. This model was trained using kfold validation
# with an accuracy of 0.389. The train_test_split method of training the model had an accuracy of
# 0.387 which is slightly lower which is why I went with the kfold approach. (I thought the kfold
# version would be a lot higher but the accuracy is low regardless lol)

encoding = bidict.bidict({None: 0})
counter = 1
for i in range(len(df)):
    for j in range(len(df.columns)):
        string = df.iat[i, j]
        if not isinstance(string, int) and not isinstance(string, float):
            if string not in encoding:
                encoding[string] = counter
                counter += 1
            df.iat[i, j] = encoding[string]

print(df)

y = df.loc[:,TARGET_COLUMN_NAME]
#X = df.drop(TARGET_COLUMN_NAME, axis=1) #input variable, everything excluding NDC_CODE

# #note: consider converting PAID_AMOUNT to FALSE if 0 (rejected claim) and TRUE if greater than 0 (accepted claim)
# X_train, X_test, y_train, y_test = train_test_split(X.astype('int'), y.astype('int'), test_size=0.2, random_state=42) #could use StratifiedKFold

# model = RandomForestClassifier(n_estimators=100, random_state=42) #n_estimators = number of trees
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)

# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)

seed = 0
np.random.seed(seed)

best_model = None
max_accuracy = float('-inf')

model = RandomForestClassifier(n_estimators=100, random_state=seed)
for train_i, test_i in StratifiedKFold(n_splits=4, shuffle=True, random_state=seed).split(df_original, y_original):
    train, test = df.loc[train_i,:].astype('int'), df.loc[test_i,:].astype('int')

    X_train = train[X_LABELS]
    y_train = train[[TARGET_COLUMN_NAME]]
    X_test = test[X_LABELS]
    y_test = test[[TARGET_COLUMN_NAME]]

    print(X_train)
    print(y_train)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(pred)
    for val in pred:
        if val in encoding.inverse:
            print(encoding.inverse[val])
    accuracy = accuracy_score(y_test, pred)
    print(accuracy)
    print(max_accuracy)
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        best_model = model

print(df.columns)
print(max_accuracy)

model_file_name = 'model_pickle2'
with open(model_file_name, 'wb') as f:
    pickle.dump(model, f)

encoder_file_name = 'encoder_pickle2'
with open(encoder_file_name, 'wb') as f:
    pickle.dump(encoding, f)
