import psycopg2
import json
import psycopg2.extras
from datetime import datetime

def connection():
    conn = psycopg2.connect(
            database="fsd_project", user='fsd_user', password='12345', host='127.0.0.1', port= '5432'
    )
    return conn

def save_user_registration_details(request_data):
    conn = connection()
    cursor = conn.cursor()
    try:
        
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
                mobile_number
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

        # userPassword = request_data['dob'] + str(request_data['mobile_no'][5:])
        # print(userPassword)

        # INSERT_QUERY1 = '''
        #         INSERT INTO fsd_schema.students_login(
        #         registration_number,
        #         user_name,
        #         user_password) 
        #         VALUES({},'{}', '{}')'''.format(
        #             student_reg_no,
        #             request_data['email'],
        #             userPassword
        #         )
        
        # cursor.execute(INSERT_QUERY1)
        # conn.commit()

        #User Login Section End

        
    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return "Success"

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

def get_students_data(enrollment_number):
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
                s.mobile_number 
                FROM fsd_schema.students_info s
                INNER JOIN fsd_schema.courses c
                 ON s.course_id = c.course_id
                INNER JOIN fsd_schema.year_of_study y
                 ON s.year_of_study_id = y.year_of_study_id 
                WHERE registration_number = '{}'  
        '''     .format(str(enrollment_number))
        
        result = cursor.execute(QUERY)
        records = cursor.fetchall()
        
       
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
                SELECT 
                about_id,
                about_type,
                about_info FROM fsd_schema.about
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

def get_profile_data(enrollment_number):
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
		        INNER JOIN fsd_schema.students_marks m
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
                '''.format(str(enrollment_number))
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

def get_course_data():
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        QUERY = '''
                SELECT 
                course_id,
                course_name
                FROM fsd_schema.courses
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