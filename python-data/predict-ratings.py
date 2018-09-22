import json
import sys
import time
import requests
import pandas as pd
import numpy as np
import mysql.connector
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

engine = create_engine('mysql+mysqlconnector://'+DATABASE_USER+':'+DATABASE_PASSWORD+'@127.0.0.1/CFB', echo=False)

sql = '''
select
	a.rating,
    f.rating as prevRating,
	b.points as recruiting1,
	c.points as recruiting2,
	d.points as recruiting3,
	e.points as recruiting4
from ratings a
inner join recruiting_rankings b
	on a.year - 1 = b.year and a.teamID = b.teamID
inner join recruiting_rankings c
	on a.year - 2 = c.year and a.teamID = c.teamID
inner join recruiting_rankings d
	on a.year - 3 = d.year and a.teamID = d.teamID
inner join recruiting_rankings e
	on a.year - 4 = e.year and a.teamID = e.teamID
inner join ratings f
	on a.year - 1 = f.year and a.teamID = f.teamID
order by a.year, b.points desc
'''

data = pd.read_sql(sql, engine)
data = data.fillna(0)

X=data[['prevRating','recruiting1','recruiting2','recruiting3','recruiting4']].values
y=data[['rating']].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train_std, y_train)
# Make predictions using the testing set
y_pred = regr.predict(X_test_std)

# The intercept
print('Intercept: ', regr.intercept_)
# The coefficients
print('Coefficients: ', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))

# Plot outputs
# plt.scatter(X_test, y_test,  color='black')
# plt.plot(X_test, y_pred, color='blue', linewidth=3)
#
# plt.xticks(())
# plt.yticks(())
#
# plt.show()
