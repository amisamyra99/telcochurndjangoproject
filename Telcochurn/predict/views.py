from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, StandardScaler
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC 
# Create your views here.
import joblib
reloadModel=joblib.load('../Telcochurn/predict/models/gbc.pkl')

def homepage(request):
	return render (request,'home.html')


def predictgbc(request):
	return render (request,'index.html')

def result(request):
	data = pd.read_excel(r'../Telcochurn/predict/models/Telco_customer_churn.xlsx')
	data= data.drop(['CustomerID','Churn Label','Churn Score','CLTV','Churn Reason'], axis=1)
	totalCharges = data.columns.get_loc("Total Charges")
	new_col = pd.to_numeric(data.iloc[:, totalCharges], errors='coerce')
    #coerce: the invalid parsing will be set as NaN
	data.iloc[:, totalCharges] = pd.Series(new_col)
	data = data.dropna(axis=0, subset=['Total Charges'])
	data = data.drop(['Country','State','Count','Gender','Lat Long','City','Zip Code','Lat Long','Latitude','Longitude'], axis=1)
	y = data.iloc[:,18]
	X = data.iloc[:,0:18]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)
	categorical_features =data.select_dtypes(include=['object']).columns
	encoder= OrdinalEncoder()
	X_train[categorical_features]=encoder.fit_transform(X_train[categorical_features])
	X_test[categorical_features]=encoder.transform(X_test[categorical_features])
	Lnum = data.select_dtypes(include=['int64', 'float64']).columns
	X_train_svm,y_train_svm,X_test_svm,y_test_svm = X_train.copy(),y_train.copy(),X_test.copy(),y_test.copy()
	svm =SVC(C= 100, gamma= 0.01, kernel= 'rbf')
	svm.fit(X_train_svm, y_train_svm)
	if request.method=='POST':
		temp={}

		n1_1=request.POST.get('seniorCitizen')
		if(n1_1=="no"):
			n1=0
		else:
			n1=1

		n2_2=request.POST.get('partner')
		if(n2_2=="no"):
			n2=0
		else:
			n2=1
		n3_3=request.POST.get('dependents')
		if(n3_3=="no"):
			n3=0
		else:
			n3=1
		n4=request.POST.get('tenureMonths')
		n5_5=request.POST.get('phoneService')
		if(n5_5=="no"):
			n5=0
		else:
			n5=1
		n6_6=request.POST.get('multipleLines')
		if(n6_6=="no"):
			n6=0
		elif(n6_6=="yes"):
			n6=1
		else:
			n6=2

		n7_8=request.POST.get('internetService')
		if(n7_8=="no"):
			n7=0
		elif(n7_8=="DSL"):
			n7=1
		else:
			n7=2
		n8_8=request.POST.get('onlineSecurity')
		if(n8_8=="no"):
			n8=0
		elif(n8_8=="yes"):
			n8=1
		else:
			n8=2
	
			n9_9=request.POST.get('onlineBackup')
		if(n9_9=="no"):
			n9=0
		elif(n9_9=="yes"):
			n9=1
		else:
			n9=2
		
			n10_8=request.POST.get('deviceProtection')
		if(n10_8=="no"):
			n10=0
		elif(n10_8=="yes"):
			n10=1
		else:
			n10=2

			n11_8=request.POST.get('techSupport')
		if(n11_8=="no"):
			n11=0
		elif(n11_8=="yes"):
			n11=1
		else:
			n11=2
	
			n12_8=request.POST.get('streamingTV')
		if(n12_8=="no"):
			n12=0
		elif(n12_8=="yes"):
			n12=1
		else:
			n12=2
	
			n13_13=request.POST.get('streamingMovies')
		if(n13_13=="no"):
			n13=0
		elif(n13_13=="yes"):
			n13=1
		else:
			n13=2

		n14_13=request.POST.get('contract')
		if(n14_13=="Monthly"):
			n14=0
		elif(n14_13=="OneYear"):
			n14=1
		else:
			n14=2
		n15_13=request.POST.get('paperlessBilling')
		if(n15_13=="no"):
			n15=0
		else:
			n15=1
		
		n16_13=request.POST.get('paymentMethod')
		if(n16_13=="BankTransfer"):
			n16=3
		elif(n16_13=="Mailed"):
			n16=1
		else:
			n16=2
		n17=request.POST.get('monthlyCharges')
		n18=request.POST.get('totalCharges')
	#testDTaa=pd.DataFrame({'x':temp}).transpose()
	pred=svm.predict([[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18]])
	print(pred)
	scoreval="test with value"
	if pred==1:
		scoreval="churn"
	else:
		scoreval="no churn"

	#print(testDTaa)
	return render(request,'index.html',{'result':scoreval})
	
from pymongo import MongoClient
# client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['telco_db']
collectionD = db['telco']

def viewDatabase(request):
    countOfrow=collectionD.find().count()
    context={'countOfrow':countOfrow}
    return render(request,'viewDB.html',context)