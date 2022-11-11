
from ast import Pass
import email
import json
from flask import  request, jsonify, Blueprint, abort
from app.models.models import *
import sqlalchemy

web = Blueprint('web', __name__,url_prefix="/pekla")

@web.get("/company" )
@web.post("/company")
@web.put("/company")
@web.delete("/company")
def company():
    print(request.method)
    if ( rm := request.method ) == "GET":

        ## get all record of Company
        # getCompany = Company.query.all()
        # return jsonify(companyList=[i.serialize() for i in getCompany])

        try:
            company_id = request.args.get('company_id')
            #Currency Reference 
            companyWithCurrency = db.session.query(Company,Currency_Reference)\
            .join(Company, Company.currency_reference_id==Currency_Reference.id)\
            .filter(Company.company_id == company_id)

            #licence_info
            if request.args.get('includeLicenseInfo'):
                companyWithLicence = db.session.query(Company,Licence)\
                .join(Company, Company.company_id==Licence.company_id)\
                .filter(Company.company_id == company_id)   

            print(companyWithCurrency) 

            # for com in companyWithCurrency:
            #     print(com.Company.company_id,com.Company.company_name)

            companyData = {}
            for companys in companyWithCurrency:
                companyData['company_id'] = companys.Company.company_id
                companyData['company_name'] = companys.Company.company_name
            
            
            licenceInfos={}
            licenceInfoArr=[]
            if request.args.get('includeLicenseInfo'):
                for licence in companyWithLicence:
                    licenceInfo={}
                    licenceInfo['licence_key']=licence.Licence.licence_key
                    licencePermission ={}
                    licencePermission["otp"]=licence.Licence.otp
                    licencePermission["face_compare"]=licence.Licence.facial_comparison
                    licenceInfo['licencePermission'] = licencePermission
                    licenceInfo['start_date'] =licence.Licence.start_date
                    licenceInfo['end_date'] =licence.Licence.expiry_date

                    licenceInfoArr.append(licenceInfo)
                
                companyData['licenceInfos'] =licenceInfoArr

            
            currencyInfo={}
            for currencies in companyWithCurrency:
                # print(company.company_name,currency.country,currency.code) 
                
                currencyInfo['country']=currencies.Currency_Reference.country
                currencyInfo['code'] = currencies.Currency_Reference.code
                currencyInfo['currency']=currencies.Currency_Reference.currency
                currencyInfo['phone'] = currencies.Currency_Reference.number
            companyData['currency_info'] = currencyInfo

            print(companyData)
        
            return jsonify({'companyData': companyData})
        except sqlalchemy.exc.OperationalError as e:
                db.session.rollback() 
                return e     
        except sqlalchemy.exc.ProgrammingError as e:
                db.session.rollback()
                return e
        except sqlalchemy.exc.IntegrityError as e:
                db.session.rollback()
                return e
        except Exception as e:
                db.session.rollback()
                return e

    elif rm == "POST":
        x = datetime.now()
        data=request.get_json(force=True)
        company_name = data['company_name']
        company_data = data['company_data']
        currency_refference_id = data['currency_refference_id']
      
        ###### insert data into db #####
        # company_name,company_data,currency_refference_id,create_date,update_date
        c1 = Company(company_name=company_name,company_data=company_data,
                currency_refference_id=currency_refference_id, create_date = x,update_date=x)
        try:
            db.session.add(c1)
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e       
    elif rm == "PUT":
        company_id = request.args.get('company_id')
        company  =   User.query.get(company_id)#query
        data=request.get_json(force=True)
        company_name = data['company_name']
        company_data = data['company_data']
        currency_refference_id = data['currency_refference_id']

        company.company_name = company_name
        company.company_data = company_data
        company.currency_reference_id = currency_refference_id
        try:
            db.session.commit()
            return jsonify({"status":2,"message":"Updated Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e       

        

    elif rm == "DELETE":
        company_id = request.args.get('company_id')
        delComp = Company.query.filter_by(company_id=company_id).delete()
        try:
            db.session.commit()
            return jsonify({"status":3,"message":"Deleted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e       
        # abort(501)
          

@web.get("/license")
@web.post("/license")
@web.put("/license")
@web.delete("/license")
def peklaLicense():

    if ( rm := request.method ) == "GET":
       getCompany = Licence.query.all()
       return jsonify(licenceList=[i.serialize() for i in getCompany])
    elif rm == "POST":
        x = datetime.now()
        data=request.get_json(force=True)
        licence_key = data['licence_key']
        start_date = data['start_date']
        expiry_date = data['expiry_date']
        otp = data['otp']
        active_liveness = data['active_liveness']
        facial_comparison = data['facial_comparison']
        company_id = data['company_id']
        passive_liveness = data['passive_liveness']

      
        ###### insert data into db #####
    #  self,licence_id,licence_key,start_date,expiry_date,otp,
                    #  active_liveness,facial_comparison,company_id
                    #  ,passive_liveness,create_date,update_date
        c1 = Licence(licence_key=licence_key,start_date=start_date,
                expiry_date=expiry_date, otp = otp,active_liveness=active_liveness
                ,facial_comparison=facial_comparison,
                 company_id = company_id,passive_liveness=passive_liveness, create_date = x,update_date=x)

        try:
            db.session.add(c1)
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e       
        
    elif rm == "PUT":
        licence_id = request.args.get('licence_id')
        lic  =   Licence.query.get(licence_id)#query
        data=request.get_json(force=True)
        
        licence_key = data['licence_key']
        start_date = data['start_date']
        expiry_date = data['expiry_date']
        otp = data['otp']
        active_liveness = data['active_liveness']
        facial_comparison = data['facial_comparison']
        company_id = data['company_id']
        passive_liveness = data['passive_liveness']

        lic.licence_key = licence_key
        lic.start_date = start_date
        lic.expiry_date = expiry_date
        lic.otp = otp
        lic.active_liveness = active_liveness
        lic.facial_comparison = facial_comparison
        lic.company_id = company_id
        lic.passive_liveness = passive_liveness
        
        try:
            
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        

    elif rm == "DELETE":
        licence_id = request.args.get('licence_id')
        delComp = Licence.query.filter_by(licence_id=licence_id).delete()
        try:  
            db.session.commit()
            return jsonify({"status":3,"message":"Deleted Successfully!"})  
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        

@web.get("/users")
@web.post("/users")
@web.put("/users")
@web.delete("/users")
def users():

    if ( rm := request.method ) == "GET":
        
        # getUser = User.query.filter_by(email='peter').first()
        getUser = User.query.all()
        
        return jsonify(userList=[i.serialize() for i in getUser])
        
    elif rm == "POST":
        x = datetime.now()
        data=request.get_json(force=True)
   
        name = data['name']
        email_id = data['email_id']
        phone_number = data['phone_number']
        image = data['image']
        company_id = data['company_id']
        # create_date =data['create_date']
        # update_date = data['update_date']
        c1 = User(name=name,phone_number=phone_number,email_id=email_id,image=image,
             company_id = company_id,create_date=x,update_date=x)
        try:  
            db.session.add(c1)
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
       
    elif rm == "PUT":
        user_id = request.args.get('user_id')
        user  =   User.query.get(user_id)#query
        data=request.get_json(force=True)
        name = data['name']
        email_id = data['email_id']
        phone_number = data['phone_number']
        image = data['image']
        company_id = data['company_id']

        user.name=name
        user.email_id=email_id
        user.phone_number = phone_number
        user.image = image
        user.company_id = company_id

        try:  
            db.session.commit()
            return jsonify({"status":2,"message":"Updated Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        


        
        # getUser = User.query.filter_by(user_id=user_id).first()
        # if not email_id:
        #     email_id =getUser.email_id
        # if not name:
        #     name=getUser.name
        # if not phone_number:
        #     phone_number = getUser.phone_number
        # if not image:
        #     image = getUser.image
        # if not company_id:
        #     company_id=getUser.company_id
        #update query
        # User.query().\
        # filter_by(User.user_id == user_id).\
        # update({"phone_number": (phone_number),"email_id":email_id,"name":name,"image":image,"company_id":company_id})
        # db.session.commit()
        # userList =jsonify({"name":User.name,"phone_number":User.phone_number})
        # print(User.name,User.email_id)
        
     
    elif rm == "DELETE":
        #1 method delete
        # user = User.query.get(id)
        # db.session.delete(user)
        # db.session.commit()
        
        #2 second method for delete
        user_id = request.args.get('user_id')
        delUser = User.query.filter_by(user_id=user_id).delete()
       
        try:  
            db.session.commit()
            return jsonify({"status":3,"message":"Deleted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        # abort(501)
       
   


@web.get("/currency_reff")
def currency_reff():

    if ( rm := request.method ) == "GET":
        
        # getUser = User.query.filter_by(email='peter').first()
        getCurrencyRef = Currency_Reference.query.all()
        return jsonify(currencyList=[i.serialize() for i in getCurrencyRef])
    
   
@web.get("/employee")
@web.post("/employee")
@web.put("/employee")
@web.delete("/employee")
def employee():

    if ( rm := request.method ) == "GET":
         # getUser = User.query.filter_by(email='peter').first()
        getCurrencyRef = Employee.query.all()
        return jsonify(employeeList=[i.serialize() for i in getCurrencyRef])
    elif rm == "POST":
        x = datetime.now()
       
        data=request.get_json(force=True)
        # print(data)
        phone_number = data['phone_number']
        email_id = data['email_id']
        employee_profile_pic = data['employee_profile_pic']
        role_id = data['role_id']
     
        c1 = Employee(phone_number=phone_number,email_id=email_id,employee_profile_pic=employee_profile_pic,role_id=role_id
        ,create_date=x,update_date=x)
       

        try:  
            db.session.add(c1)
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        
        

    elif rm == "PUT":
        employee_id = request.args.get('employee_id')
        emp  =   Employee.query.get(employee_id)#query
        data=request.get_json(force=True)
        # print(data)
        phone_number = data['phone_number']
        email_id = data['email_id']
        employee_profile_pic = data['employee_profile_pic']
        role_id = data['role_id']

        emp.phone_number = phone_number
        emp.email_id = email_id
        emp.employee_profile_pic =employee_profile_pic
        emp.role_id = role_id
        db.session.commit()

        try:  
            db.session.commit()
            return jsonify({"status":2,"message":"Updated Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        


       
    elif rm == "DELETE":
        employee_id = request.args.get('employee_id')
        delcr = Employee.query.filter_by(employee_id=employee_id).delete()
    
        try:  
            db.session.commit()
            return jsonify({"status":3,"message":"Deleted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        # abort(501)
        
    
@web.get("/logs")
@web.post("/logs")
def logs():

    if ( rm := request.method ) == "GET":
        abort(501)
    elif rm == "POST":
        abort(501)
    
    abort(405)



@web.get("/cost_table")
@web.post("/cost_table")
@web.put("/cost_table")
@web.delete("/cost_table")
def cost_table():
    print(request.method)
    if ( rm := request.method ) == "GET":
        getPermission = Cost_Table.query.all()
        
        return jsonify(costList=[i.serialize() for i in getPermission])
        
    elif rm == "POST":
        x = datetime.now()
        data=request.get_json(force=True)
        company_id = data['company_id']
        sms_cost = data['sms_cost']
        email_cost = data['email_cost']
        # create_date = data['create_date']
        active_liveness_cost = data['active_liveness_cost']
        passive_liveness_cost = data['passive_liveness_cost']
        facial_comparison_cost = data['facial_comparison_cost']
      
        ###### insert data into db #####
    #  self,company_id,sms_cost,email_cost,active_liveness_cost,passive_liveness_cost,
                    #  facial_comparison_cost)
        c1 = Cost_Table(company_id=company_id,sms_cost=sms_cost,
                email_cost=email_cost, active_liveness_cost = active_liveness_cost
                , passive_liveness_cost = passive_liveness_cost,
                 facial_comparison_cost = facial_comparison_cost)
        

        try:  
            db.session.add(c1)
            db.session.commit()
            return jsonify({"status":1,"message":"Inserted Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
        
    elif rm == "PUT":
        company_id = request.args.get('company_id')
        CostT  =   Otp_Logs.query.get(company_id)#query
        data=request.get_json(force=True)
        company_id = data['company_id']
        sms_cost = data['sms_cost']
        email_cost = data['email_cost']
        active_liveness_cost = data['active_liveness_cost']
        passive_liveness_cost = data['passive_liveness_cost']
        facial_comparison_cost = data['facial_comparison_cost']

        #UPDATE
        CostT.company_id = company_id
        CostT.sms_cost = sms_cost
        CostT.email_cost = email_cost
        CostT.active_liveness_cost = active_liveness_cost
        CostT.passive_liveness_cost = passive_liveness_cost
        CostT.facial_comparison_cost = facial_comparison_cost
     

        
        try:  
            db.session.commit()

            return jsonify({"status":2,"message":"Updated Successfully!"})
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        

        

    elif rm == "DELETE":
        company_id = request.args.get('company_id')
        delComp = Cost_Table.query.filter_by(company_id=company_id).delete()
       
        try:  
            db.session.commit()
            return jsonify({"status":3,"message":"Deleted Successfully!"})  
        except sqlalchemy.exc.OperationalError as e:
            db.session.rollback() 
            return e     
        except sqlalchemy.exc.ProgrammingError as e:
             db.session.rollback()
             return e
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return e
        except Exception as e:
             db.session.rollback()
             return e        
       