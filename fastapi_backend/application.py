from fastapi import FastAPI
import fsd_backend_db as fsd_db
import json
import schemas
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/get_subjects_and_courses_data")
def get_subjects_and_courses_data():
    result = fsd_db.get_subjects_and_courses_data()
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.get("/get_course_data")
def get_course_data():
    result = fsd_db.get_course_data()
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.get("/get_studying_year_data")
def get_studying_year_data():
    result = fsd_db.get_studying_year_data()
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.get("/get_about_data")
def get_about_data():
    result = fsd_db.get_about_data()
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.post("/save_user_registration_details")
def save_user_registration_details(reg_details:schemas.UserRegistration):
    print(reg_details)
    result = fsd_db.save_user_registration_details(reg_details.dict())
    return "Success"

@app.post("/attempt_to_login_for_user")
def attempt_to_login_for_user(login_data:schemas.LoginForUser):
    valid_user_login = ""
    valid_user = fsd_db.validate_login_details(login_data.dict())
    if(valid_user):
        valid_user_login = "Login Successful"
    else:
        valid_user_login = "Login Failed"

    response = {
        "status" : valid_user_login
    }
    return JSONResponse(content=response, status_code=200)
    

@app.post("/get_students_data")
def get_students_data(students_data:schemas.StudentData):
    print(students_data)
    result = fsd_db.get_students_data(students_data.student_id)
    response = {
        "data" : result
    }
    return JSONResponse(content=response, status_code=200)

@app.post("/get_profile_data")
def get_profile_data(profile_data:schemas.ProfileData):
    print(profile_data)
    result = fsd_db.get_profile_data(profile_data.student_id)
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.post("/save_image")
def save_image(image_data:schemas.ImageData):
    print(image_data.reg_number)
    result = fsd_db.upload_image(image_data)
    response = {
        "data" : result
    }
    return json.dumps(response)