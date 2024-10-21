from fastapi import FastAPI
import fsd_backend_db as fsd_db
import json
import schemas

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


