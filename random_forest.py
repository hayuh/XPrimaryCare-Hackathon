from app import df

import numpy as np
from sklearn.model_selection import StratifiedKFold

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print(df.columns)

# split data into input and taget variable(s)

X = df.drop("NDC_CODE", axis=1) #input variable, everything excluding NDC_CODE
y = df["NDC_CODE"] #target variable, predict the NDC_CODE

#note: consider converting PAID_AMOUNT to FALSE if 0 (rejected claim) and TRUE if greater than 0 (accepted claim)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #could use StratifiedKFold

model = RandomForestClassifier(n_estimators=100, random_state=42) #n_estimators = number of trees
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)