from flask import Flask,render_template,request
import pandas as pd
import openpyxl
import numpy as np



myapp = Flask(__name__)
 
@myapp.route('/',methods =['GET','POST'])
def home():
        return render_template('index.html')

@myapp.route('/register',methods =['GET','POST'])
def register():
        return render_template('registration.html')

@myapp.route('/confirm',methods =['GET','POST'])
def registering():
        if request.method == 'POST':
                #Taking values from registration form and converting it to dictionary
                info= request.form.to_dict(flat=False)

                #converting dictionary to a dataframe df
                df=pd.DataFrame(info)

                #reading registration_details.xlsx to another dataframe df2
                df2=pd.read_excel('registration_details.xlsx')
                #assigning userentered mobile number to variable value_mobile
                value_mobile=int(df['mobile'][0])

                #searching value_mobile in df2(registration_details.xlsx) using apply,lamba and any methods
                # and assigning the returned true/false values in search_value 
                search_value=df2.apply(lambda row:value_mobile in row.values, axis=1).any()
                
                #if mobile number is already available returning html as you are already registered
                if search_value :
                        return render_template('confirmation.html',df=df,value=value)

                #if mobile is not registered appending(adding new rows to the excel)
                #with entered registration details using ExcelWriter method displaying html message
                else:
                        with pd.ExcelWriter('registration_details.xlsx',mode='a',engine='openpyxl',if_sheet_exists='overlay') as writer :
                                df.to_excel(writer,header=False,startrow=len(df2)+1)
                        return render_template('confirmation.html',df=df)
@myapp.route('/login',methods =['GET','POST'])
def login():
        if request.method == 'POST':

                 #Taking values from registration form and converting it to dictionary
                info= request.form.to_dict(flat=False)
                #converting dictionary to a dataframe df1
                df1=pd.DataFrame(info)

                #reading registration_details.xlsx to another dataframe df2
                df2=pd.read_excel('registration_details.xlsx')
                
                #converting username if mobile to "int"(mobile) if error continuing as "str"(email)
                try:
                        value_username=int(df1['username'][0])
                except:
                        value_username=df1['username'][0]
                
                #assigning entered password to value_password
                try:
                        value_password=int(df1['password'][0])
                except:

                        value_password=df1['password'][0]      

                #seaching username in (df2)registration.xlsx and storing true/false value
                search_username=df2.apply(lambda row:value_username in row.values, axis=1).any() 
                
                #if username found
                if search_username:
                        print("username correct")
                        
                        #getting index no. of row of that particular user and storing in variable m 
                        for i in df2.index:
                                if df2['email'][i]==value_username or df2['mobile'][i]==value_username:
                                        m=i
                                        print("im",m)
                        
                        #checking entered password in df2(registration.xlsx) with respect to username using m index
                        password_match=df2['password'][m]==str(value_password)
                        if df2['password'][m]==str(value_password):
                                print("password correct")
                                
                                #if password matches displaying login successful
                                
                                return  render_template("message.html",tables=[df2.to_html(classes='data',header="true")],value1=search_username,password_match=password_match)
                        else:
                                print("password incorrect")
                                #else displaying password incorrect password message
                                return render_template('message.html')
                
                #if username not found displaying username incorrect
                else:
                        print("username incorrect")
                        return render_template('message.html')
                
                
if  __name__ =='__main__':
    myapp.run(debug=True ,host='0.0.0.0',port=5001)



