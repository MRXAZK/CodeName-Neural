from schemas.s_users import UserSchema, Users
from models.m_users import User
from fastapi import APIRouter, Response, status
from config.database import conn

user = APIRouter()

#get all users
@user.get("/user/all", response_model=Users, description="Show All User Data")
async def find_all_user(limit: int = 10, offset: int = 0):
    query = User.select().offset(offset).limit(limit)
    data = conn.execute(query).fetchall()
    response = {"limit": limit, "offset": offset, "data": data}
    return response

#get user by id
@user.get("/user/{id}", description="Show Details Data")
async def find_user(id: int, response: Response):
    query = User.select().where(User.c.id_users == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message" : "Data Not Found", "Status" : response.status_code
        }
    
    response = {
        "message" : f"Success show data with id {id}", "data": data
    }
    return response

#Add new User

@user.post("/user/", description="Add User")
async def insert_user(usr: UserSchema, response: Response):
    
    email_check = User.select().filter(User.c.email == usr.email)
    email_check = conn.execute(email_check).fetchone()
    
    if email_check is not None:
        
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": response.status_code, 
            "message": "Email Already Exists"
        }
        
    query = User.insert().values(
        name = usr.name,
        address = usr.address,
        date_of_birth = usr.date_of_birth,
        telp = usr.telp,
        email = usr.email
    )
    
    conn.execute(query)
    data = User.select().order_by(User.c.id_users.desc())
    response = {
        "message" : f"Success add new user data", "data": conn.execute(data).fetchone()
    }
    return response

#Edit User data

@user.post("/user/{id}", description="Edit User Data")
async def update_user(id: int, usr : UserSchema, response: Response):
    
    email_check = User.select().filter(User.c.email == usr.email, User.c.id_users != id)
    email_check = conn.execute(email_check).fetchone()
    
    if email_check is not None:
        
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": response.status_code, 
            "message": "Email Already Exists"
        }
        
    query = User.Update().values(
        name = usr.name,
        address = usr.address,
        date_of_birth = usr.date_of_birth,
        telp = usr.telp,
        email = usr.email
    ).where(User.c.id_users == id)
    
    conn.execute(query)
    data = User.select().where(User.c.id_users == id)
    response = {
        "message" : f"Success change user data with id {id}", "data": conn.execute(data).fetchone()
    }
    return response                    
                            


#Delete User
@user.delete("/user/{id}", description="Delete Data User")
async def delete_user(id: int, response: Response):
    query = User.select().where(User.c.id_users == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": "Data Not Found", "Status": response.status_code
        }
    
    query = User.delete().where(User.c.id_users == id)
    conn.execute(query)
    response = {
        "message" : f"Success delete user with id {id}"
    }
    return response