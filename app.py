from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import gzip
import pandas as pd
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
with gzip.open('Final_Attendance_Mahim.pkl', 'rb') as ifp:
    model=pickle.load(ifp)
#model = pickle.load(open('Attendance.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('Final_attendance_mahim.html')


standard_to = StandardScaler()
#@app.route("/predict", methods=['POST'])
#def predict():
@app.route('/', methods=("POST", "GET"))
def html_table():
    
    if request.method == 'POST':
        test_data= pd.read_excel('Details_Mahim.xlsx')
        test_data=test_data.drop(labels= ['Year '], axis =1 )
        Department=request.form['Department']
        if(Department=='BANGALORE / HYDERABAD MARKETING'):
            Department1=[1,0,0,0,0,0,0,0,0,0]
        elif(Department=='CCD'):
            Department1=[0,1,0,0,0,0,0,0,0,0]
        elif(Department=='DIRECTOR ASSISTANT'):
            Department1=[0,0,1,0,0,0,0,0,0,0]
        elif(Department=='EXPORTS LOGISTIC'):
            Department1=[0,0,0,1,0,0,0,0,0,0]
        elif(Department=='EXPORTS MARKETING'):
            Department1=[0,0,0,0,1,0,0,0,0,0]
        elif(Department=='IT SUPPORT / ADMIN'):
            Department1=[0,0,0,0,0,1,0,0,0,0]
        elif(Department=='MINCO MARKETING'):
            Department1=[0,0,0,0,0,0,1,0,0,0]
        elif(Department=='MUMBAI MARKETING'):
            Department1=[0,0,0,0,0,0,0,1,0,0]
        elif(Department=='ORDER EXECUTION'):
            Department1=[0,0,0,0,0,0,0,0,1,0]
        else:
            Department1=[0,0,0,0,0,0,0,0,0,1]
        
        index=np.where(test_data['Department']==Department)
        test1=test_data.iloc[index]
        test1=test1.drop(labels= ['Department'], axis =1 )
        
        Month=request.form['Month']
        if(Month=='January'):
            Month1=[0,0,0,0,1,0,0,0,0,0,0,0]
        elif(Month=='February'):
            Month1=[0,0,0,1,0,0,0,0,0,0,0,0]
        elif(Month=='March'):
            Month1=[0,0,0,0,0,0,0,1,0,0,0,0]
        elif(Month=='April'):
            Month1=[1,0,0,0,0,0,0,0,0,0,0,0]
        elif(Month=='May'):
            Month1=[0,0,0,0,0,0,0,0,1,0,0,0]
        elif(Month=='June'):
            Month1=[0,0,0,0,0,0,1,0,0,0,0,0]
        elif(Month=='July'):
            Month1=[0,0,0,0,0,1,0,0,0,0,0,0]
        elif(Month=='August'):
            Month1=[0,1,0,0,0,0,0,0,0,0,0,0]
        elif(Month=='September'):
            Month1=[0,0,0,0,0,0,0,0,0,0,0,1]
        elif(Month=='October'):
            Month1=[0,0,0,0,0,0,0,0,0,0,1,0]
        elif(Month=='November'):
            Month1=[0,0,0,0,0,0,0,0,0,1,0,0]
        else:
            Month1=[0,0,1,0,0,0,0,0,0,0,0,0]
        Year=int(request.form['Year'])
        dates=[]
        if(Month == 'January'):
            for i in range(1,32):
                dates.append(i)
        elif(Month == 'September'):
            for i in range(1,31):
                dates.append(i)
        elif(Month == "March"):
            for i in range(1,32):
                dates.append(i)
        elif(Month == 'May'):
            for i in range(1,32):
                dates.append(i)
        elif(Month == "July"):
            for i in range(1,32):
                dates.append(i)
        elif(Month == "August"):
            for i in range(1,32):
                dates.append(i)
        elif(Month == "October"):
            for i in range(1,32):
                dates.append(i)
        elif(Month == "Decemeber"):
            for i in range(1,32):
                dates.append(i)
        elif(Month == 'November'):
            for i in range(1,31):
                dates.append(i)
        elif(Month == 'April'):
            for i in range(1,31):
                dates.append(i)
        elif(Month == 'June'):
            for i in range(1,31):
                dates.append(i)
        else:
            if((Year % 4)==0 or (Year % 400)==0):
                for i in range(1,30):
                    dates.append(i)
            else:
                for i in range(1,29):
                    dates.append(i)
        import datetime  
        from datetime import date 
        import calendar  
  
        def findDay(date): 
            day, month, year = (int(i) for i in date.split(' '))     
            born = datetime.date(year, month, day) 
            return born.strftime("%A")
        Month_int={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
        dayss=[]
        day={'Monday':[0,1,0,0,0,0,0],'Tuesday':[0,0,0,0,0,1,0],'Wednesday':[0,0,0,0,0,0,1],'Thursday':[0,0,0,0,1,0,0],'Friday':[1,0,0,0,0,0,0],'Saturday':[0,0,1,0,0,0,0],'Sunday':[0,0,0,1,0,0,0]}
        for i in range(len(dates)):
            y=findDay(str(i+1)+" "+str(Month_int[Month])+" "+str(Year))
            day1=day[y]
            dayss.append(day1)
        test=[]
        for i in range(test1.shape[0]):
            a=np.concatenate((np.array(test1.iloc[i,1:].values).reshape(1,-1),np.array(Department1).reshape(1,-1)),axis=1)
            test.append(a)
        test=np.array(test).reshape(test1.shape[0],-1)
        test2=list([])
        for a in range(0,test[:,:].shape[0]): 
                for i in range(len(dates)):
                    X=np.concatenate((np.array(test[a,0:]).reshape(1,-1),np.array(dates[i]).reshape(1,-1)),axis=1)
                    Y=np.concatenate((X,np.array(dayss[i]).reshape(1,-1)),axis=1)
                    Z=np.concatenate((Y,np.array(Month1).reshape(1,-1)),axis=1)
                    for k in range(Z.shape[1]):
                        test2.append(Z[0,k]) 
        test3=np.array(test2).reshape(-1,Z.shape[1])
        
        prediction=model.predict(test3)
        arr=[]
        for i in range(prediction.shape[0]):
            if(list(prediction[i])==[0,1,0]):
                arr.append('P')
            elif(list(prediction[i])==[1,0,0]):
                arr.append('A')
            else:
                arr.append('WO')
        arr=np.array(arr).reshape(-1,len(dates))
        name=test1['Name of employee'].reset_index(drop=True)
        ar=[]
        for i in range(arr.shape[0]):
            ar.append(name[i])
            for j in range(arr.shape[1]):
                ar.append(arr[i,j])
        ar=np.array(ar).reshape(arr.shape[0],arr.shape[1]+1)
        if(len(dates)==31):
            Prediction=pd.DataFrame(data=ar, columns=["Name of Employee","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"])
        elif(len(dates)==30):
            Prediction=pd.DataFrame(data=ar, columns=["Name of Employee","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"])
        elif(len(dates)==29):
            Prediction=pd.DataFrame(data=ar, columns=["Name of Employee","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29"])
        else:
            Prediction=pd.DataFrame(data=ar, columns=["Name of Employee","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"])
        
    
        return render_template('Final_attendance_mahim.html',tables=[Prediction.to_html(classes='data')], titles=Prediction.columns.values)
    else:
        return render_template('Final_attendance_mahim.html')


if __name__=="__main__":
    app.run(debug=True)
