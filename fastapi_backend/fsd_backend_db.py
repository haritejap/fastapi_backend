import psycopg2
import json
import psycopg2.extras
from datetime import datetime

def connection():
    conn = psycopg2.connect(
            database="fsd_project", user='fsd_user', password='12345678', host='127.0.0.1', port= '5432'
    )
    return conn

def upload_image(image_data):
    conn = connection()
    cursor = conn.cursor()
    try:

        QUERY = '''
                UPDATE fsd_schema.students_info
                SET profile_image = '{}'
                WHERE registration_number = '{}' 
                '''.format(
                    image_data.image,
                    image_data.reg_number
                )
        cursor.execute(QUERY)
        conn.commit()

    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return "Success"

def save_user_registration_details(request_data,user_type):
    print(user_type)
    
    conn = connection()
    cursor = conn.cursor()
    try:
        if (user_type == "student"):
            QUERY = '''
                    SELECT shortname FROM fsd_schema.courses 
                    WHERE course_id = {}
                    '''.format(
                        int(request_data['branch'])
                    )
            result = cursor.execute(QUERY)
            records = cursor.fetchall()
            current_year = datetime.now().year
            last_two_digits = str(current_year % 100) 

            for row in records:
                short_form = row[0] 
        
            QUERY1 = '''
                    SELECT count(registration_number) FROM fsd_schema.students_info 
                    WHERE course_id = {}
                    '''.format(
                        int(request_data['branch'])
                    )
        
            reg_result = cursor.execute(QUERY1)
            reg_records = cursor.fetchall()

            for row in reg_records:
                no_of_students = row[0]

            student_reg_no = ''
            if(no_of_students < 9):
                student_reg_no = last_two_digits + short_form + '00' + str(no_of_students+1)
            elif(no_of_students < 99):
                student_reg_no = last_two_digits + short_form + '0' + str(no_of_students+1)
            else:
                student_reg_no = last_two_digits + short_form + str(no_of_students+1)
            print(student_reg_no)
            
            #User Registration Section Start
    
            INSERT_QUERY = '''
                    INSERT INTO fsd_schema.students_info(
                    registration_number,
                    first_name,
                    last_name,  
                    year_of_study_id,
                    course_id,
                    admission_date,
                    date_of_birth,
                    email,
                    mobile_no
                    ) 
                    VALUES('{}','{}', '{}','{}','{}','{}','{}','{}','{}')'''.format(
                        student_reg_no,
                        request_data['first_name'],
                        request_data['last_name'],
                        request_data['year_of_study'],
                        request_data['branch'],
                        request_data['admission_date'],
                        request_data['dob'],
                        request_data['email'],
                        request_data['mobile_no']
                    )
            print(INSERT_QUERY)
            cursor.execute(INSERT_QUERY)
            conn.commit()
            #User Registration Section End
            #User Login Section Start
            userPassword = str(request_data['dob'])[:4] + str(request_data['mobile_no'])[5:]
            # print(userPassword)
            print(request_data['mobile_no'], request_data['dob'])

            INSERT_QUERY1 = '''
                    INSERT INTO fsd_schema.students_login(
                    registration_number,
                    user_name,
                    user_password) 
                    VALUES('{}','{}','{}')'''.format(
                        student_reg_no,
                        request_data['email'],
                        userPassword
                    )
            cursor.execute(INSERT_QUERY1)
            conn.commit()
            #User Login Section End

        elif(user_type == "faculty"):
            QUERY = '''
                    SELECT shortname FROM fsd_schema.courses 
                    WHERE course_id = {}
                    '''.format(
                        int(request_data['branch'])
                    )
            result = cursor.execute(QUERY)
            records = cursor.fetchall()
            current_year = datetime.now().year
            last_two_digits = str(current_year % 100) 

            for row in records:
                short_form = row[0] 
        
            QUERY1 = '''
                    SELECT count(registration_number) FROM fsd_schema.faculty_info 
                    WHERE branch = {}
                    '''.format(
                        int(request_data['branch'])
                    )
        
            reg_result = cursor.execute(QUERY1)
            reg_records = cursor.fetchall()

            for row in reg_records:
                no_of_faculty = row[0]

            faculty_reg_no = ''
            if(no_of_faculty < 9):
                faculty_reg_no = 'F' + last_two_digits + short_form + '00' + str(no_of_faculty+1)
            elif(no_of_faculty < 99):
                faculty_reg_no = 'F' + last_two_digits + short_form + '0' + str(no_of_faculty+1)
            else:
                faculty_reg_no = 'F' + last_two_digits + short_form + str(no_of_faculty+1)
            print(faculty_reg_no)
            current_date = datetime.now().date()
            formatted_date = current_date.strftime('%Y-%m-%d')
            print("formmatted date" ,formatted_date )
            #User Registration Section Start
    
            INSERT_QUERY = '''
                    INSERT INTO fsd_schema.faculty_info(
                    registration_number,
                    first_name,
                    last_name,  
                    branch,
                    joining_date,
                    date_of_birth,
                    email,
                    mobile_no
                    ) 
                    VALUES('{}','{}', '{}','{}','{}','{}','{}','{}')'''.format(
                        faculty_reg_no,
                        request_data['first_name'],
                        request_data['last_name'],
                        request_data['branch'],
                        formatted_date,
                        request_data['dob'],
                        request_data['email'],
                        request_data['mobile_no']
                    )
            print(INSERT_QUERY)
            cursor.execute(INSERT_QUERY)
            conn.commit()
            #User Registration Section End
            #User Login Section Start
            userPassword = str(request_data['dob'])[:4] + str(request_data['mobile_no'])[5:]
            # print(userPassword)
            print(request_data['mobile_no'], request_data['dob'])

            INSERT_QUERY1 = '''
                    INSERT INTO fsd_schema.faculty_login(
                    registration_number,
                    user_name,
                    user_password) 
                    VALUES('{}','{}','{}')'''.format(
                        faculty_reg_no,
                        request_data['email'],
                        userPassword
                    )
            cursor.execute(INSERT_QUERY1)
            conn.commit()
        # else:
        #     raise ValueError("Invalid user_type provided.")
    except Exception as e:
        print("Error", str(e), "Occurred")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return "Success"

def validate_login_details(login_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    valid_user = False
    print(login_data['user_login_type'])
    try:
        if(login_data['user_login_type'] == "student"):
            QUERY = ''' 
                    SELECT registration_number, user_password FROM fsd_schema.students_login
                    WHERE registration_number = '{}' 
                    '''.format(login_data['user_name'])
            reg_result = cursor.execute(QUERY)
            reg_records = cursor.fetchall()
            print(reg_records)
            for row in reg_records:
                user_password = row['user_password']
                registration_number = row['registration_number']
            print(user_password,registration_number)
            if(login_data['user_name'] == registration_number and login_data['password'] == user_password):
                valid_user = True
        elif(login_data['user_login_type'] == "faculty"):
            QUERY = ''' 
                    SELECT registration_number, user_password FROM fsd_schema.faculty_login
                    WHERE registration_number = '{}' 
                    '''.format(login_data['user_name'])
            reg_result = cursor.execute(QUERY)
            reg_records = cursor.fetchall()
            print(reg_records)
            for row in reg_records:
                user_password = row['user_password']
                registration_number = row['registration_number']
            print(user_password,registration_number)
            if(login_data['user_name'] == registration_number and login_data['password'] == user_password):
                valid_user = True
    except Exception as e:
        print("Error", str(e), "Occured")

    finally:
        if conn:
            cursor.close()
            conn.close()
    return valid_user

def get_user_registration_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT 
                s.registration_number,
                s.first_name,
                s.last_name,
                y.year_of_study_name,
                c.course_name,
                TO_CHAR(s.admission_date, 'DD-MON-YYYY') AS admission_date,
                TO_CHAR(s.date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                s.email,
                s.mobile_no,
                s.profile_image 
                FROM fsd_schema.students_info s
                INNER JOIN fsd_schema.courses c
                 ON s.course_id = c.course_id
                INNER JOIN fsd_schema.year_of_study y
                 ON s.year_of_study_id = y.year_of_study_id
                '''
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        # records[0]["profile_image"] = records[0]["profile_image"].tobytes().decode("utf-8")
        json_result = json.dumps(records,indent=4)
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result  

def get_about_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT * FROM fsd_schema.about
                ORDER BY about_id ASC 
                '''
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        json_result = json.dumps(records, indent=4)
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_subjects_and_courses_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT c.course_name as course_name,
                c.course_id as course_id,
                c.course_duration as course_duration,
                s.subject_name as subject_name
                FROM fsd_schema.courses c
                inner join fsd_schema.subjects s
                on s.course_id = c.course_id
                group by c.course_name,c.course_id,c.course_duration,s.subject_name
                '''
        
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        # columns = [desc[0] for desc in cursor.description]

        # # Convert the result into a list of dictionaries
        # result = [dict(zip(columns, row)) for row in records]

        # Convert the list of dictionaries to JSON
        json_result = json.dumps(records, indent=4)
        
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

# def get_student_subject_marks():
#     data = request.get_json()
#     enrollment_number = data.get('enrollmentNumber')
#     conn = connection()
#     cursor = conn.cursor()
#     query = '''SELECT * FROM students WHERE enrollment_number = %s'''
#     cursor.execute(query, (enrollment_number,))
#     result = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     if result:
#         marks = result[0]
#         return jsonify({'success': True, 'marks': marks})
#     else:
#         return jsonify({'success': False, 'message': 'Enrollment number not found'})

def get_profile_data(student_id):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        print(student_id)
        QUERY = '''
                SELECT s.registration_number,
				c.course_name,
                sm.semester_id,
				sm.semester_name,
                p.subject_id,
				p.subject_name,
				m.subject_marks,
                m.status,
                fsd_schema.validate_and_get_grade(m.subject_marks) AS grade
		        FROM fsd_schema.students_info s
		        INNER JOIN fsd_schema.student_marks m
		        on s.registration_number = m.registration_number
                INNER JOIN fsd_schema.subjects p
                on p.subject_id = m.subject_id
				INNER JOIN fsd_schema.semester_subject_mapping ssm
				on ssm.subject_id = p.subject_id
				INNER JOIN fsd_schema.semester sm
				on sm.semester_id = ssm.semester_id
				INNER JOIN fsd_schema.courses c
				on c.course_id = p.course_id
				WHERE s.registration_number = '{}'
                '''.format(str(student_id))
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        print(records)
        json_result = json.dumps(records)
        return json_result
    
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_marks_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT 
                record_id ,
                registration_number ,
                subject_id ,
                subject_marks
                from fsd_schema.student_marks
                '''
        
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        json_result = json.dumps(records)
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def post_user_registration_data(enrollment_number):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        print(enrollment_number)
        QUERY = '''
                SELECT 
                s.registration_number,
                s.first_name,
                s.last_name,
                y.year_of_study_name,
                c.course_name,
                TO_CHAR(s.admission_date, 'DD-MON-YYYY') AS admission_date,
                TO_CHAR(s.date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                s.email,
                s.mobile_no,
                s.profile_image
                FROM fsd_schema.students_info s
                INNER JOIN fsd_schema.courses c
                ON s.course_id = c.course_id
                INNER JOIN fsd_schema.year_of_study y
                ON s.year_of_study_id = y.year_of_study_id 
                WHERE registration_number = '{}'  
                '''.format(str(enrollment_number))
        print(QUERY)
        result = cursor.execute(QUERY)
        records = cursor.fetchall() 
        print(records)
        if  records[0]["profile_image"] != None:
            records[0]["profile_image"] = records[0]["profile_image"].tobytes().decode("utf-8")
        json_result = json.dumps(records,indent=2)
        
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_courses_semester_subjects_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT s.registration_number,
				c.course_name,
                sm.semester_id,
				sm.semester_name,
				p.subject_name,
				m.subject_marks,
                m.status
		        FROM fsd_schema.students_info s
		        INNER JOIN fsd_schema.student_marks m
		        on s.registration_number = m.registration_number
                INNER JOIN fsd_schema.subjects p
                on p.subject_id = m.subject_id
				INNER JOIN fsd_schema.semester_subject_mapping ssm
				on ssm.subject_id = p.subject_id
				INNER JOIN fsd_schema.semester sm
				on sm.semester_id = ssm.semester_id
				INNER JOIN fsd_schema.courses c
				on c.course_id = s.course_id
				WHERE s.registration_number = '{}'
                '''
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        json_result = json.dumps(records)
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_department_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT 
                department_id,
                department_name
                FROM fsd_schema.department
                '''
        
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        print(records)
        
        json_result = json.dumps(records,indent=4)
        
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_studying_year_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT 
                year_of_study_id,
                year_of_study_name
                FROM fsd_schema.year_of_study
                '''
        
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        print(records)
        
        json_result = json.dumps(records,indent=4)
        
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def get_year_semester_department_subjects_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT y.year_of_study_id,
	            y.year_of_study_name,
	            s.semester_id,
	            s.semester_name,
	            c.course_id,
	            c.course_name,
                c.shortname,
	            sub.subject_id,
	            sub.subject_name
	            FROM fsd_schema.semester_subject_mapping ssm
	            INNER JOIN fsd_schema.semester s
	            on ssm.semester_id = s.semester_id
                INNER JOIN fsd_schema.year_of_study y
	            on s.year_of_study_id = y.year_of_study_id	               
                INNER JOIN fsd_schema.subjects sub
                on ssm.subject_id = sub.subject_id
	            INNER JOIN fsd_schema.courses c
		        on sub.course_id = c.course_id 
                '''
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        json_result = json.dumps(records, indent=4)
        print(json_result)
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return json_result

def upload_file(file_data,subject_id):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # Get the maximum record_id from the database
        cursor.execute("SELECT MAX(record_id) AS max_record_id FROM fsd_schema.student_marks")
        result = cursor.fetchone()
        # Start from max_record_id + 1
        record_id = result['max_record_id'] + 1 if result['max_record_id'] is not None else 176
        print("Starting record_id:", record_id)
        print("Subject ID:", subject_id)
        for index,row in file_data.iterrows():
            print(record_id)
            print(row['registration_number'])
            print(row['first_name'])
            print(row['last_name'])
            print(row['subject_marks'])
            # Construct the INSERT query
            QUERY = '''
                INSERT INTO fsd_schema.student_marks(record_id, registration_number, subject_id, subject_marks)
                VALUES (%s, %s, %s, %s)
            '''
            # Execute the query with data
            cursor.execute(QUERY, (
                record_id,
                row['registration_number'],
                subject_id,
                row['subject_marks']
            ))
            record_id += 1  
        #Commit the changes to the database
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error", str(e), "Occurred")
        conn.rollback()  # Rollback in case of an error
    finally:
        if conn:
            cursor.close()
            conn.close()