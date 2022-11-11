from app import db
from datetime import datetime

'''Role ORM'''
class Roles(db.Model):
    role_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    role_name = db.Column(db.String(15),unique =True)
  
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

    def __init__(self,role_id,role_name,create_date,update_date):
        self.role_id = role_id
        self.role_name = role_name
     
        self.create_date = create_date
        self.update_date = update_date

    def serialize(self):
        return {"role_id": self.role_id,
                "role_name": self.role_name,
                "permission_short_description": self.permission_short_description,
              
                "create_date":self.create_date,
                "update_date":self.update_date,
                }


'''Permission ORM'''
class Permissions(db.Model):
    permission_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    permission_name = db.Column(db.String(15),unique=True)
    permission_short_description = db.Column(db.String(100))
    permission_description = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)
    child = db.relationship('Permissions_Roles_Junction',backref ='permissions',uselist=False)

    def __init__(self,permission_id,permission_name,permission_short_description,permission_description,create_date,update_date):
        self.permission_id = permission_id
        self.permission_name = permission_name
        self.permission_short_description = permission_short_description
        self.permission_description = permission_description
        
        self.create_date = create_date
        self.update_date = update_date

    def serialize(self):
        return {"permission_id": self.permission_id,
                "permission_name": self.permission_name,
                "permission_short_description": self.permission_short_description,
                "permission_description":self.permission_description,
                "create_date":self.create_date,
                "update_date":self.update_date,
                }


'''Permission Roles Junction'''
class Permissions_Roles_Junction(db.Model):
    # role_id = db.Column(db.Integer,primary_key=True)
    role_id = db.Column('role_id',db.Integer, db.ForeignKey(Roles.role_id), primary_key=True)
    # permission_id =  db.Column(db.Integer,db.ForeignKey('permissions.permission_id'))
    permission_id = db.Column('permission_id',db.Integer, db.ForeignKey(Permissions.permission_id), primary_key=True)
    permission_name = db.Column(db.String(15),unique=True)
    permission_short_description = db.Column(db.String(100))
    permission_description = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

    def __init__(self,permission_id,permission_name,permission_short_description,permission_description,create_date,update_date):
        self.permission_id = permission_id
        self.permission_name = permission_name
        self.permission_short_description = permission_short_description
        self.permission_description = permission_description     
        self.create_date = create_date
        self.update_date = update_date

    def serialize(self):
        return {"permission_id": self.permission_id,
                "permission_name": self.permission_name,
                "permission_short_description": self.permission_short_description,
                "create_date":self.create_date,
                "update_date":self.update_date,
                }



'''Currency Reference'''
class Currency_Reference(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    country = db.Column(db.String(20),nullable=False,unique=True)
    currency = db.Column(db.String(5),nullable=False,unique=True)
    code = db.Column(db.String(5),nullable=False,unique=True)
    number = db.Column(db.String(5),nullable=False,unique=True)
    # currency_reference = db.relationship("Company", backref="currency_reference", uselist=False)
    
    def __init__(self,country,currency,code,number
                    ):
       
        self.country = country
        self.currency = currency
        self.code = code
        self.number = number
    
    def serialize(self):
        return {"id": self.id,
                "country": self.country,
                "currency": self.currency,
                "code":self.code,
                "number":self.number,
                }

'''Company_Data_Master'''
class Company_Data_Master(db.Model):
    data_type_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    data_type = db.Column(db.String(50),primary_key=True,autoincrement=False)
    
    def __init__(self,data_type):
        self.data_type = data_type

    def serialize(self):
        return {"data_type_id": self.data_type_id,
                "data_type": self.data_type
                }

'''Status_Master'''
class Status_Master(db.Model):
    status_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    status = db.Column(db.String(50))
    def __init__(self,status):
        self.status = status

    def serialize(self):
        return {"status_id": self.status_id,
                "status": self.status
               }


''' Company table  ORM'''

class Company(db.Model):
    # __table_args__ = (
    #     db.UniqueConstraint('company_name', name='unique_component_commit'),
    # )
    company_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    company_name = db.Column(db.String(100),unique=True)
    # company_data = db.Column(db.String(100))
    company_data= db.Column('company_data',db.Integer, db.ForeignKey(Company_Data_Master.data_type_id))
    # currency_refference_id =db.Column(db.Integer, db.ForeignKey('currency_reference.id')) #foreign key
    currency_reference_id = db.Column('currency_refference_id',db.Integer, db.ForeignKey(Currency_Reference.id))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

    def __init__(self,company_name,company_data,currency_refference_id,create_date,update_date):
       
        self.company_name = company_name
        self.company_data = company_data
        self.currency_refference_id = currency_refference_id
        self.create_date = create_date
        self.update_date = update_date
    
    def serialize(self):
        return {"company_name": self.company_name,
                "company_data": self.company_data,
                "currency_reference_id": self.currency_reference_id,
                "create_date":self.create_date,
                "company_id":self.company_id,
                "update_date":self.update_date
               
                }



'''Employee ORM'''
class Employee(db.Model):
    employee_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone_number = db.Column(db.String(15),nullable=False)
    email_id = db.Column(db.String(30),unique=True,nullable=False)
    employee_name = db.Column(db.String(50),nullable=False)
    # role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id')) #foreign key
    role_id = db.Column('role_id',db.Integer, db.ForeignKey(Roles.role_id))
    employee_profile_pic = db.Column(db.String(100))
    # company_id = db.Column(db.Integer, db.ForeignKey('Company.company_id')) #foreign key
    company_id = db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

    def __init__(self,phone_number,email_id,employee_profile_pic,role_id,create_date,update_date):
        # self.employee_id = employee_id
        self.phone_number = phone_number
        self.email_id = email_id
        self.employee_profile_pic = employee_profile_pic
        self.role_id = role_id
        self.create_date = create_date
        self.update_date = update_date

    def serialize(self):
        return {"employee_id": self.employee_id,
                "phone_number": self.phone_number,
                "email_id": self.email_id,
                "employee_profile_pic":self.employee_profile_pic,
                "role_id":self.role_id,
                "create_date":self.create_date,
                 "update_date":self.update_date  
                }

'''Licence ORM'''
class Licence(db.Model):
    licence_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    licence_key = db.Column(db.String(100))
    start_date = db.Column(db.String(100),nullable=False)
    expiry_date = db.Column(db.String(100),nullable=False)
    otp = db.Column(db.String(15))
    passive_liveness = db.Column(db.String(100),nullable=False)
    active_liveness  = db.Column(db.String(100),nullable=False)
    facial_comparison = db.Column(db.String(100),nullable=False)
    # company_id = db.Column(db.Integer, db.ForeignKey('Company.company_id')) #foreign key
    company_id = db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

    def __init__(self,licence_key,start_date,expiry_date,otp,
                     active_liveness,facial_comparison,company_id
                     ,passive_liveness,create_date,update_date):
        # self.licence_id = licence_id
        self.licence_key = licence_key
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.otp = otp
        self.active_liveness = active_liveness
        self.passive_liveness = passive_liveness
        self.facial_comparison = facial_comparison
        self.company_id = company_id
        self.create_date = create_date
        self.update_date = update_date
    def serialize(self):
        return {"licence_id": self.licence_id,
                "licence_key": self.licence_key,
                "start_date": self.start_date,
                "expiry_date":self.expiry_date,
                "otp":self.otp,
                "active_liveness":self.active_liveness,
                 "passive_liveness":self.passive_liveness,
                "facial_comparison":self.facial_comparison,
                "company_id":self.company_id,
                "create_date":self.create_date,
                "update_date":self.update_date
               
                }
    

# class Externam_company_data(db.Model):
#     company_id = db.Column(db.Integer,primary_key=True)
#     api1_endpoint = db.Column(db.String(15))
#     api1_method = db.Column(db.String(100))
#     api1_request_header = db.Column(db.String(100))
#     api1_request_payload = db.Column(db.String(100))
#     api1_constants = db.Column(db.String(100))
#     api1_response_schema = db.Column(db.String(10))
#     api2_endpoint = db.Column(db.String(15))
#     api2_method = db.Column(db.String(100))
#     api2_request_header = db.Column(db.String(100))
#     api2_request_payload = db.Column(db.String(100))
#     api2_constants = db.Column(db.String(100))
#     api2_response_schema = db.Column(db.String(10))
#     db_conn_string = db.Column(db.String(100))
#     create_date = db.Column(db.String(100))
#     update_date = db.Column(db.String(100))

#     def __init__(self,company_id,api1_endpoint,api1_method,api1_request_header,
#                 api1_request_payload,api1_constants,api1_response_schema,
#                 api2_endpoint,api2_method,api2_request_header,api2_request_payload,
#                 api2_constants,api2_response_schema,db_conn_string,create_date,update_date):
#         self.company_id = company_id
#         self.api1_endpoint = api1_endpoint
#         self.api1_method = api1_method
#         self.api1_request_header = api1_request_header
#         self.api1_request_payload = api1_request_payload
#         self.api1_constants = api1_constants
#         self.api1_response_schema =api1_response_schema
#         self.api1_endpoint = api1_endpoint
#         self.api2_method = api2_method
#         self.api2_request_header = api2_request_header
#         self.api2_request_payload = api2_request_payload
#         self.api2_constants = api2_constants
#         self.api2_response_schema =api2_response_schema
#         self.db_conn_string = db_conn_string
#         self.create_date = create_date
#         self.update_date = update_date

'''External_Company_Data'''
class External_Company_Data(db.Model):
    company_id =db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id),primary_key=True)
    api_parser = db.Column(db.String(50))
    def __init__(self,api_parser):
        self.api_parser = api_parser

    def serialize(self):
        return {"company_id": self.company_id,
                "api_parser": self.api_parser
               }


''' User table '''
class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False) #not null
    phone_number = db.Column(db.String(15),nullable=False)
    email_id = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(100))
    # company_id =db.Column(db.Integer, db.ForeignKey('company.company_id'))
    company_id = db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id))
    company = db.relationship("Company", backref=db.backref("company", uselist=False))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)
    #created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self,name,phone_number,email_id,image,company_id,create_date,update_date):
        self.name = name
        self.phone_number = phone_number
        self.email_id = email_id
        self.image = image
        self.company_id = company_id
        self.create_date = create_date
        self.update_date = update_date

    def serialize(self):
        return {"name": self.name,
                "phone_number": self.phone_number,
                "email_id": self.email_id,
                "image":self.image,
                "company_id":self.company_id,
                "create_date":self.create_date,
                "update_date":self.update_date
                }


# class External_Company_Data(db.Model):
#     company_id = db.Column(db.Integer,primary_key=True)
#     api1_endpoint = db.Column(db.String(15))
#     api1_method = db.Column(db.String(100))
#     api1_request_header = db.Column(db.String(100))
#     api1_request_payload = db.Column(db.String(100))
#     api1_constants = db.Column(db.String(100))
#     api1_response_schema = db.Column(db.String(10))
#     api2_endpoint = db.Column(db.String(15))
#     api2_method = db.Column(db.String(100))
#     api2_request_header = db.Column(db.String(100))
#     api2_request_payload = db.Column(db.String(100))
#     api2_constants = db.Column(db.String(100))
#     api2_response_schema = db.Column(db.String(10))
#     db_conn_string = db.Column(db.String(100))
#     create_date = db.Column(db.String(100))
#     update_date = db.Column(db.String(100))

#     def __init__(self,company_id,api1_endpoint,api1_method,api1_request_header,
#                 api1_request_payload,api1_constants,api1_response_schema,
#                 api2_endpoint,api2_method,api2_request_header,api2_request_payload,
#                 api2_constants,api2_response_schema,db_conn_string,create_date,update_date):
#         self.company_id = company_id
#         self.api1_endpoint = api1_endpoint
#         self.api1_method = api1_method
#         self.api1_request_header = api1_request_header
#         self.api1_request_payload = api1_request_payload
#         self.api1_constants = api1_constants
#         self.api1_response_schema =api1_response_schema
#         self.api1_endpoint = api1_endpoint
#         self.api2_method = api2_method
#         self.api2_request_header = api2_request_header
#         self.api2_request_payload = api2_request_payload
#         self.api2_constants = api2_constants
#         self.api2_response_schema =api2_response_schema
#         self.db_conn_string = db_conn_string
#         self.create_date = create_date
#         self.update_date = update_date



'''Session Logs'''
class Session_Logs(db.Model):
    session_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # user_id = db.Column(db.String(100))
    # company_id = db.Column(db.String, db.ForeignKey('Company.company_id')) #foreign key
    company_id=db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id))
    user_id=db.Column('user_id',db.Integer, db.ForeignKey(User.user_id))
    # licence_id = db.Column(db.String, db.ForeignKey('Licence.licence_id')) #foreign key
    licence_id= db.Column('licence_id',db.Integer, db.ForeignKey(Licence.licence_id))
    app_version = db.Column(db.String(100))
    device_brand_name = db.Column(db.String(100))
    device_model_name = db.Column(db.String(100))
    device_os = db.Column(db.String(100))
    device_id = db.Column(db.String(100))


    def __init__(self,user_id,company_id,licence_id,app_version,device_brand_name,device_model_name,
               device_os,device_id ):
        # self.session_id = session_id
        self.user_id = user_id
        self.company_id = company_id
        self.licence_id = licence_id
        self.app_version =app_version
        self.device_brand_name =device_brand_name
        self.device_model_name = device_model_name
        self.device_os =device_os
        self.device_id = device_id

    def serialize(self):
        return {"session_id": self.session_id,
                "user_id": self.user_id,
                "company_id": self.company_id,
                "licence_id":self.licence_id,
                "app_version":self.app_version,
                "device_brand_name":self.device_brand_name,
                "device_model_name":self.device_model_name,
                 "device_os":self.device_os,
                "device_id":self.device_id
                }

'''Active Liveness Logs'''
class Active_Liveness_Logs(db.Model):
    active_liveness_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # status = db.Column(db.String, db.ForeignKey('Status_Master.status')) #foreign key
    
    session_id=db.Column('session_id',db.Integer, db.ForeignKey(Session_Logs.session_id))
    status_id=db.Column('status_id',db.Integer, db.ForeignKey(Status_Master.status_id))
    execution_time = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)
    def __init__(self,session_id,status,execution_time,create_date):
        self.session_id = session_id
        self.status = status
        self.execution_time = execution_time
        self.create_date = create_date

    def serialize(self):
        return {"active_liveness_id": self.active_liveness_id,
                "session_id": self.session_id,
                "status": self.status,
                "execution_time":self.execution_time,
                "create_date":self.create_date
              
                }
'''Passive Liveness Logs'''
class Passive_Liveness_Logs(db.Model):
    passive_liveness_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # status = db.Column(db.String, db.ForeignKey('Status_Master.status')) #foreign key
    session_id=db.Column('session_id',db.Integer, db.ForeignKey(Session_Logs.session_id))
    status_id=db.Column('status_id',db.Integer, db.ForeignKey(Status_Master.status_id))
    
    execution_time = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,session_id,status_id,execution_time,create_date):
        self.session_id = session_id
        self.status_id = status_id
        self.execution_time = execution_time
        self.create_date = create_date

    def serialize(self):
        return {"passive_liveness_id": self.passive_liveness_id,
                "session_id": self.session_id,
                "status_id": self.status_id,
                "execution_time":self.execution_time,
                "create_date":self.create_date
              
                }

'''Facial Comparision Logs'''
class Facial_Comparision_Logs(db.Model):
    facial_liveness_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    session_id=db.Column('session_id',db.Integer, db.ForeignKey(Session_Logs.session_id))
    status_id=db.Column('status_id',db.Integer, db.ForeignKey(Status_Master.status_id))
    # status = db.Column(db.String, db.ForeignKey('Status_Master.status')) #foreign key
    # db.Column('status',db.Integer, db.ForeignKey(Status_Master.status), primary_key=True)
    execution_time = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,session_id,status_id,execution_time,create_date):
        self.session_id = session_id
        self.status_id = status_id
        self.execution_time = execution_time
        self.create_date = create_date

    def serialize(self):
        return {"facial_liveness_id": self.facial_liveness_id,
                "session_id": self.session_id,
                "status_id": self.status_id,
                "execution_time":self.execution_time,
                "create_date":self.create_date   
                }

'''Otp_Logs'''
class Otp_Logs(db.Model):
    otp_log_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    session_id=db.Column('session_id',db.Integer, db.ForeignKey(Session_Logs.session_id))
    status_id=db.Column('status_id',db.Integer, db.ForeignKey(Status_Master.status_id))
    # status = db.Column(db.String, db.ForeignKey('Status_Master.status')) #foreign key
    # db.Column('status',db.Integer, db.ForeignKey(Status_Master.status), primary_key=True)
    execution_time = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,session_id,status_id,execution_time,create_date):
        self.session_id = session_id
        self.status_id = status_id
        self.execution_time = execution_time
        self.create_date = create_date

    def serialize(self):
        return {"otp_log_id": self.otp_log_id,
                "session_id": self.session_id,
                "status_id": self.status_id,
                "execution_time":self.execution_time,
                "create_date":self.create_date   
                }

'''Cost Table'''
class Cost_Table(db.Model):
    company_id=db.Column('company_id',db.Integer, db.ForeignKey(Company.company_id),primary_key=True)
    sms_cost = db.Column(db.String(100))
    email_cost = db.Column(db.String(100))
    active_liveness_cost = db.Column(db.String(100))
    passive_liveness_cost = db.Column(db.String(100))
    facial_comparison_cost = db.Column(db.String(100))
    

    def __init__(self,company_id,sms_cost,email_cost,active_liveness_cost,passive_liveness_cost,
                     facial_comparison_cost):
        self.company_id = company_id
        self.sms_cost = sms_cost
        self.email_cost = email_cost
        self.active_liveness_cost = active_liveness_cost
        self.passive_liveness_cost = passive_liveness_cost
        self.facial_comparison_cost = facial_comparison_cost

    def serialize(self):
        return {"company_id": self.company_id,
                "sms_cost": self.sms_cost,
                "email_cost": self.email_cost,
                "active_liveness_cost":self.active_liveness_cost,
                "passive_liveness_cost":self.passive_liveness_cost,
                "facial_comparison_cost":self.facial_comparison_cost      
                }

#####################

# '''User Logs View'''
# class User_Logs_View(db.Model):
#     user_id = db.Column(db.Integer,primary_key=True)
#     company_id = db.Column(db.String, db.ForeignKey('Company.company_id')) #foreign key
#     session_id = db.Column(db.String, db.ForeignKey('Session_Logs.session_id')) #foreign key
#     otp_status = db.Column(db.String(100))
#     facial_comparision_status = db.Column(db.String(100))
#     active_liveness_status = db.Column(db.String(100))
#     passive_liveness_status = db.Column(db.String(100))
#     create_date = db.Column(db.DateTime)

#     def __init__(self,user_id,company_id,session_id,otp_status
#             ,facial_comparision_status,active_liveness_status,passive_liveness_status
#             ,create_date):
#         self.user_id = user_id
#         self.company_id = company_id
#         self.session_id = session_id
#         self.otp_status =otp_status
#         self.facial_comparision_status = facial_comparision_status
#         self.active_liveness_status =active_liveness_status
#         self.passive_liveness_status =passive_liveness_status
#         self.create_date = create_date
        
