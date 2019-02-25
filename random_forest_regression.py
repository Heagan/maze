
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

regressor = None

X = []
y = []

def setup_ml(cols):
	print("Setting up ML")

	global regressor

	dataset = pd.read_csv('data.csv', ';')
	X = dataset.iloc[:, 1:cols].values
	y = dataset.iloc[:, cols].values

	print(X)
	print(y)

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.05, random_state = 0)

	sc_X = StandardScaler()
	X_train = sc_X.fit_transform(X_train)
	X_test = sc_X.transform(X_test)
	sc_y = StandardScaler()
	y_train = sc_y.fit_transform(y_train.reshape(-1, 1))


	regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
	regressor.fit(X, y)

	print("Done! Ready to predict!")

def predict(X):
	global regressor

	return regressor.predict(X)
