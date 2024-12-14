from fastapi import FastAPI
from fastapi.responses import JSONResponse
import fsd_backend_db as fsd_db
import json
import schemas
import base64
import io 
import pandas as pd

app = FastAPI()

@app.get("/fastapi")

def read_root():

    return {"message": "Hello, FastAPI!"}

@app.get("/get_subjects_and_courses_data")
def get_subjects_and_courses_data():
    result = fsd_db.get_subjects_and_courses_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_courses_semester_subjects_data")
def get_courses_semester_subjects_data():
    result = fsd_db.get_courses_semester_subjects_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_about_data")
def get_about_data():
    result = fsd_db.get_about_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_marks_data")
def get_marks_data():
    result = fsd_db.get_marks_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_courses_semester_subjects_data")
def get_courses_semester_subjects_data():
    result = fsd_db.get_courses_semester_subjects_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_department_data")
def get_department_data():
    result = fsd_db.get_department_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_studying_year_data")
def get_studying_year_data():
    result = fsd_db.get_studying_year_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.get("/get_user_registration_data")
def get_user_registration_data():
    result = fsd_db.get_user_registration_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.post("/save_user_registration_details")
def save_user_registration_details(reg_details:schemas.UserRegistration):
    print(reg_details)
    print(reg_details.user_type)
    result = fsd_db.save_user_registration_details(reg_details.dict(),reg_details.user_type)
    response = {
        "data" : result
    }
    return JSONResponse(content=response)


@app.post("/get_profile_data")
def get_profile_data(get_profile:schemas.GetProfileData):
    print(get_profile)
    result = fsd_db.get_profile_data(get_profile.student_id)
    response = {
        "data": result
    }
    return JSONResponse(content=response, status_code=200)

@app.post("/post_user_registration_data")
def post_user_registration_data(post_registration:schemas.PostUserRegistration):
    result = fsd_db.post_user_registration_data(post_registration.student_id)
    response = {
        "data" : result
    }
    return JSONResponse(content=response, status_code=200)

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
    return JSONResponse(content=response,status_code =200)

@app.post("/save_image")
def save_image(image_data:schemas.ImageData):
    print(image_data.reg_number)
    result = fsd_db.upload_image(image_data)
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.get("/get_year_semester_department_subjects_data")
def get_year_semester_department_subjects_data():
    result = fsd_db.get_year_semester_department_subjects_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.post("/upload_excel")
def upload_file(file_data:schemas.fileData):
    excel_base64 = file_data.file
    decoded_data = base64.b64decode(excel_base64)

    # Step 2: Write the decoded data into an in-memory buffer
    buffer = io.BytesIO(decoded_data)

    # Step 3: Load the Excel file into a DataFrame
    # Specify the sheet name if needed using `sheet_name='Sheet1'` or use `sheet_name=None` for all sheets
    df = pd.read_excel(buffer)

    # Display the DataFrame
    print(df)
    result = fsd_db.upload_file(df,file_data.subject_id)
    
    # response = {
    #     "data" : result
    # }
    # return json.dumps(response)
    # print(excel_base64)
    print(file_data.subject_id)
    return "success"
