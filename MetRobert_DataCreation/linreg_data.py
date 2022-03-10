import numpy as np
from sklearn.linear_model import LinearRegression
import math

# we are a supermarket
# we are going to save how many products are sold each day
# we are also going to measure how many people there are each day

# x = amount of people in store
x = np.array([20, 30, 40, 50, 60, 70, 80, 85, 100])

# y = amount of products stored
acc = np.array([89.88, 90.23, 90.91, 91.73, 92.09, 92.37, 92.48, 92.80, 93.32])
f1 = np.array([67.24, 69.76, 71.22, 72.38, 74.21, 75.54, 76.37, 76.29, 79.22])

x = x.reshape(-1, 1)
#print(x)
#print(acc)
#print(f1)

acc_model = LinearRegression().fit(x, acc)
f1_model = LinearRegression().fit(x, acc)

# how good is our model?
r_sq_acc = acc_model.score(x, acc)
r_sq_f1 = f1_model.score(x, f1)

print("acc model score = " + str(r_sq_acc))
print("f1 model score = " + str(r_sq_f1))

# predict using our model 
y_pred_110 = acc_model.predict(np.array([110]).reshape(1, -1))
y_pred_120 = acc_model.predict(np.array([120]).reshape(1, -1))
y_pred_130 = acc_model.predict(np.array([130]).reshape(1, -1))
y_pred_140 = acc_model.predict(np.array([140]).reshape(1, -1))
y_pred_150 = acc_model.predict(np.array([150]).reshape(1, -1))

print(y_pred_110)
print(y_pred_120)
print(y_pred_130)
print(y_pred_140)
print(y_pred_150)

# predict using logaritmic model
acc_pred_110 = 83.0222 + 2.1976 * np.log(110)
acc_pred_120 = 83.0222 + 2.1976 * np.log(120)
acc_pred_130 = 83.0222 + 2.1976 * np.log(130)
acc_pred_140 = 83.0222 + 2.1976 * np.log(140)
acc_pred_150 = 83.0222 + 2.1976 * np.log(150)

print(acc_pred_110)
print(acc_pred_120)
print(acc_pred_130)
print(acc_pred_140)
print(acc_pred_150)

y_pred_110 = f1_model.predict(np.array([110]).reshape(1, -1))
y_pred_120 = f1_model.predict(np.array([120]).reshape(1, -1))
y_pred_130 = f1_model.predict(np.array([130]).reshape(1, -1))
y_pred_140 = f1_model.predict(np.array([140]).reshape(1, -1))
y_pred_150 = f1_model.predict(np.array([150]).reshape(1, -1))

print(y_pred_110)
print(y_pred_120)
print(y_pred_130)
print(y_pred_140)
print(y_pred_150)

# predict using logaritmic model
f1_pred2_110 = 45.2291 + 7.1536 * np.log(110)
f1_pred2_120 = 45.2291 + 7.1536 * np.log(120)
f1_pred2_130 = 45.2291 + 7.1536 * np.log(130)
f1_pred2_140 = 45.2291 + 7.1536 * np.log(140)
f1_pred2_150 = 45.2291 + 7.1536 * np.log(150)

print(f1_pred2_110)
print(f1_pred2_120)
print(f1_pred2_130)
print(f1_pred2_140)
print(f1_pred2_150)
