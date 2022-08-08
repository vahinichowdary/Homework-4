import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField, SelectField, TextAreaField
from flask import Flask
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__, template_folder="")
app.config['SECRET_KEY'] = 'advancehw'
app. config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app. config[ 'SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class MyForm(FlaskForm):
    name = StringField('Company Name:')
    email = StringField('Company Email:')
    phone = StringField('Company Phone:')
    address = StringField('Company Address:')
    ID = StringField('Company Phone:')

class UpdateForm(FlaskForm):
    name = StringField('Company Name:')
    email = StringField('Company Email:')
    phone = StringField('Company Phone:')
    address = StringField('Company Address:')
    
@app.route('/', methods=['GET', 'POST'])
def index():     
    form = MyForm()
    if request.method == 'POST':
        if request.form['submit'] == 'Add Record':
            name = form.name.data
            email = form.email.data 
            phone = form.phone.data 
            address = form.address.data 
            if name:
                if email:
                    if phone:
                        if address:
                            #print(name)
                            db.create_all() 
                            companydetails = company(name,email,phone,address)
                            db.session.add_all([companydetails])
                            db.session.commit() 
                            name = ""
                            email = "" 
                            phone=""
                            address=""
                            form.name.data = name
                            form.email.data = email
                            form.phone.data = phone
                            form.address.data = address 
        elif request.form['submit'] == 'All Records':
            return redirect(url_for('allrecords'))
        elif request.form['submit'] == 'Delete Record':
            tel = form.ID.data
            print(tel)
            if tel:
                companyrecorddelete = company.query.filter_by(phone = form.ID.data).first()
                print(companyrecorddelete)
                if companyrecorddelete:
                    db.session.delete(companyrecorddelete)
                    db.session.commit()  
                    tel = ""
                    form.ID.data = tel    
        elif request.form['submit'] == 'Update a Record':    
            tel = form.ID.data
            if tel:
                companyrecordupdate = company.query.filter_by(phone = tel).first()
                if companyrecordupdate:
                    record_id = companyrecordupdate.id
                    name = companyrecordupdate.name
                    email = companyrecordupdate.email
                    phone = companyrecordupdate.phone
                    address = companyrecordupdate.address
                    return redirect(url_for('updating',param_a = name,param_b = email,param_c = phone,param_d = address,param_e = record_id))
                    print(record_id)
    return render_template ('Yellow.html', form = form)

@app.route('/allrecords')     
def allrecords():
    return render_template('results.html', company = company.query.all() )  

@app.route('/updating', methods=['GET', 'POST'])  
def updating():
    form = UpdateForm()
    id = request.args.get('param_e')
    if request.method == 'POST':
        if request.form['submit'] == 'Update Record':
            old_data = company.query.filter_by(id = id).first()
            old_data.name = form.name.data
            old_data.email = form.email.data
            old_data.phone = form.phone.data
            old_data.address = form.address.data
            db.session.add(old_data)
            print('abcd')
            db.session.commit() 
            return redirect(url_for('index'))
    form.name.data = request.args.get('param_a')
    form.email.data = request.args.get('param_b')
    form.phone.data = request.args.get('param_c')
    form.address.data = request.args.get('param_d')
    return render_template('UpdatePage.html', form = form )      

      
class company(db.Model):
    __tablename__ = "company"

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text)
    email=db.Column(db.Text)
    phone=db.Column(db.Integer)
    address=db.Column(db.Text)

    def __init__ (self, name, email, phone, address):
        self.name=name
        self.email=email
        self.phone=phone 
        self.address=address    

    def __repr__(self):
        return f'Company ID: {self.id}, Company Name: {self.name},  Company Email: {self.email}, Comapny Phone: {self.phone}, Company Address: {self.address}'
    

if __name__ == '__main__':
    app.run(debug=True)    
    


# References:
#     1.Dr. Unan lecture: https://uab.instructure.com/courses/1576210/pages/week-07?module_item_id=16803884
#     2.https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
#     3.https://pythonbasics.org/flask-http-methods/   
#     4. Homework-3 and Lab-6,7 Reference
