# from flask import Flask, jsonify, request, render_template
# from flask_cors import CORS
# from pymongo import MongoClient
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from bson import ObjectId
# from datetime import datetime
# import os
# import PyPDF2
# import docx
# import json
# import re 
# from groq import Groq
# import pandas as pd
# from rec_courses import recommend_course
# # from mgstring import connec_string, groq_api
# from dotenv import load_dotenv

# app = Flask(__name__)
# CORS(app)
# load_dotenv()
# connec_string = os.getenv('connec_string')
# groq_api = os.getenv('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')
# # gemini_api = os.getenv('AIzaSyBPftHIF86go3oOdJo-jWpVkw-oD-UvyNc')
# # Connect to MongoDB
# client = MongoClient(connec_string)

# try:
#     client.admin.command('ping')
#     print("MongoDB is connected")
#     print(f"Available databases: {client.list_database_names()}")
#     db = client['UserTest']
#     users_collection = db['users']
#     print(f"Selected database: {db.name}")
#     print(f"Selected collection: {users_collection.name}")
#     print(f"Document count in collection: {users_collection.count_documents({})}")
# except Exception as e:
#     print("MongoDB connection failed:", e)

# # Configure upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Configure Groq API
# groq_client = Groq(
#     api_key=groq_api,
# )

# @app.route('/api/signup', methods=['POST'])
# def signup():
#     print("Received signup request")
#     if not request.is_json:
#         print("Request is not JSON")
#         return jsonify({'message': 'Request must be JSON'}), 400
    
#     data = request.get_json()
#     print(f"Received data: {data}")
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')
    
#     if not name or not email or not password:
#         print(f"Missing name, email or password. Name: {name}, Email: {email}, Password: {'*' * len(password) if password else None}")
#         return jsonify({'message': 'Name, email, and password are required'}), 400
    
#     hashed_password = generate_password_hash(password)
#     try:
#         user_data = {
#             'name': name,
#             'email': email,
#             'password': hashed_password,
#             'job': '',
#             'skills': [],
#             'skills_to_improve': [],
#             'tagline': 'A catchy tagline!'
#         }
#         result = users_collection.insert_one(user_data)
#         print(f"Insertion result: {result.inserted_id}")
#         return jsonify({'message': 'Signup successful'}), 201
#     except Exception as e:
#         print(f"Error inserting user: {e}")
#         return jsonify({'message': 'Error creating user'}), 500

# @app.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
    
#     if not email or not password:
#         return jsonify({'message': 'Email and password are required'}), 400
    
#     user = users_collection.find_one({'email': email})
#     if user and check_password_hash(user['password'], password):
#         user_data = {
#             'name': user['name'],
#             'email': user['email'],
#             'tagline': user.get('tagline', 'A catchy tagline!') 
#         }
#         return jsonify({'message': 'Login successful', 'user': user_data}), 200
#     else:
#         return jsonify({'message': 'Invalid email or password'}), 401
    
# @app.route('/api/skills', methods=['GET'])
# def get_skills():
#     email = request.args.get('email')
#     if not email:
#         return jsonify({'message': 'Email is required'}), 400
    
#     user = users_collection.find_one({'email': email})
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     skills = user.get('skills', [])
#     return jsonify({'skills': skills}), 200

# @app.route('/api/skills', methods=['POST'])
# def add_skill():
#     data = request.get_json()
#     email = data.get('email')
#     new_skill = data.get('skill')
    
#     if not email or not new_skill:
#         return jsonify({'message': 'Email and skill are required'}), 400
    
#     user = users_collection.find_one({'email': email})
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     current_date = datetime.now().strftime('%B %Y')
#     skill_object = {
#         'date': current_date,
#         'title': new_skill
#     }
    
#     result = users_collection.update_one(
#         {'email': email},
#         {'$push': {'skills': skill_object}}
#     )
    
#     if result.modified_count:
#         return jsonify({'message': 'Skill added successfully', 'skill': skill_object}), 201
#     else:
#         return jsonify({'message': 'Failed to add skill'}), 500
        
# @app.route('/api/user/job', methods=['GET'])
# def get_job():
#     email = request.args.get('email')
#     if not email:
#         return jsonify({'message': 'Email is required'}), 400
    
#     user = users_collection.find_one({'email': email})
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     job = user.get('job', '')
#     if job == '':
#         job = 'Developer'  # Set default job
    
#     return jsonify({'job': job}), 200

# @app.route('/api/user/job', methods=['POST'])
# def update_job():
#     data = request.get_json()
#     email = data.get('email')
#     new_job = data.get('job')
    
#     if not email or new_job is None:
#         return jsonify({'message': 'Email and job are required'}), 400
    
#     result = users_collection.update_one(
#         {'email': email},
#         {'$set': {'job': new_job}}
#     )
    
#     if result.modified_count:
#         return jsonify({'message': 'Job updated successfully'}), 200
#     else:
#         return jsonify({'message': 'Failed to update job'}), 500
    
# @app.route('/api/user/update', methods=['PUT'])
# def update_user():
#     data = request.get_json()
#     email = data.get('email')
#     field = data.get('field')
#     new_value = data.get('value')
    
#     if not email or not field or new_value is None:
#         return jsonify({'message': 'Email, field, and new value are required'}), 400
    
#     if field not in ['name', 'password']:
#         return jsonify({'message': 'Only name and password can be updated'}), 400

#     update_data = {}
    
#     if field == 'password':
#         update_data[field] = generate_password_hash(new_value)
#     else:  # field is 'name'
#         update_data[field] = new_value
    
#     result = users_collection.update_one(
#         {'email': email},
#         {'$set': update_data}
#     )
    
#     if result.modified_count:
#         return jsonify({'message': f'{field.capitalize()} updated successfully'}), 200
#     else:
#         return jsonify({'message': f'Failed to update {field}'}), 500

# @app.route('/api/user/tagline', methods=['GET'])
# def get_tagline():
#     email = request.args.get('email')
#     if not email:
#         return jsonify({'message': 'Email is required'}), 400
    
#     user = users_collection.find_one({'email': email})
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
    
#     tagline = user.get('tagline', 'A catchy tagline!')
    
#     return jsonify({'tagline': tagline}), 200

# @app.route('/api/user/tagline', methods=['POST'])
# def update_tagline():
#     data = request.get_json()
#     email = data.get('email')
#     new_tagline = data.get('tagline')
    
#     if not email or new_tagline is None:
#         return jsonify({'message': 'Email and tagline are required'}), 400
    
#     result = users_collection.update_one(
#         {'email': email},
#         {'$set': {'tagline': new_tagline}}
#     )
    
#     if result.modified_count:
#         return jsonify({'message': 'Tagline updated successfully'}), 200
#     else:
#         return jsonify({'message': 'Failed to update tagline'}), 500

# @app.route('/api/skill-analyzer', methods=['POST'])
# def skill_analyzer():
#     if 'resume' not in request.files or 'job_description' not in request.files:
#         return jsonify({'error': 'Both resume and job description files are required'}), 400
    
#     resume_file = request.files['resume']
#     job_description_file = request.files['job_description']
        
#     resume_filename = secure_filename(resume_file.filename)
#     job_filename = secure_filename(job_description_file.filename)
        
#     resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#     job_path = os.path.join(app.config['UPLOAD_FOLDER'], job_filename)
        
#     resume_file.save(resume_path)
#     job_description_file.save(job_path)
        
#     try:
#         resume_text = extract_text(resume_path)
#         job_text = extract_text(job_path)
        
#         skills_analysis = compare_skills(resume_text, job_text)
            
#         os.remove(resume_path)
#         os.remove(job_path)
            
#         if 'error' in skills_analysis:
#             return jsonify(skills_analysis), 500
            
#         return jsonify(skills_analysis)
#     except Exception as e:
#         if os.path.exists(resume_path):
#             os.remove(resume_path)
#         if os.path.exists(job_path):
#             os.remove(job_path)
#         print(f"Error in skill analysis: {str(e)}")
#         return jsonify({'error': f'An error occurred during skill analysis: {str(e)}'}), 500

# def extract_text(file_path):
#     _, file_extension = os.path.splitext(file_path)
    
#     if file_extension.lower() == '.pdf':
#         with open(file_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ''
#             for page in reader.pages:
#                 text += page.extract_text()
#     elif file_extension.lower() in ['.docx', '.doc']:
#         doc = docx.Document(file_path)
#         text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
#     else:
#         with open(file_path, 'r') as file:
#             text = file.read()
    
#     return text

# def normalize_skill(skill):
#     return re.sub(r'[^\w\s]', '', skill.lower())

# def tokenize(text):
#     return re.findall(r'\b\w+\b', normalize_skill(text))

# def jaccard_similarity(set1, set2):
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#     return intersection / union if union != 0 else 0

# def is_skill_match(resume_skills, job_skill, threshold=0.3):
#     job_tokens = set(tokenize(job_skill))
#     resume_tokens = set(token for skill in resume_skills for token in tokenize(skill))
    
#     if "or" in job_skill.lower():
#         return any(skill.lower() in normalize_skill(job_skill) for skill in resume_skills)
    
#     for resume_skill in resume_skills:
#         if set(tokenize(resume_skill)).issubset(job_tokens) or set(job_tokens).issubset(tokenize(resume_skill)):
#             return True
    
#     if "object-oriented" in job_skill.lower() and any("oop" in normalize_skill(skill) for skill in resume_skills):
#         return True
    
#     similarity = jaccard_similarity(job_tokens, resume_tokens)
#     return similarity >= threshold
    
# def compare_skills(resume_text, job_text):
#     prompt = rf"""
#     Resume:
#     {resume_text}

#     Job Description:
#     {job_text}

#     Based on the resume and job description provided, please:
#     1. List skills mentioned in the resume As "skills_from_resume". ADD WITHOUT SUBHEADINGS.
#     2. List the skills required in the job description in "skills_required_in_job", PLEASE AVOID WIDE AND GENERIC SKILLS AND ONLY MENTION DEFINITE SKILLS THAT CAN BE LEARNED THROUGH A UDEMY COURSE.
#     If only key responsibilities\duties are mentioned, then extract the required skills from that.
#     Otherwise, extract it from eligibility criteria, qualifications, or any other section that mentions the required skills.
#     3. Compare the skills from the resume with the skills required in the job description and list the matching skills. in "matching_skills".
#     4. List the skills from the job description that are not present in the resume As "skills_to_improve".
#     Present the results in a structured JSON format.
#     """

#     try:
#         chat_completion = groq_client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt,
#                 }
#             ],
#             model="llama3-70b-8192",
#         )
#         response = chat_completion.choices[0].message.content
        
#         # Print the raw response for debugging
#         print("Raw API response:", response)
        
#         # Try to find and extract the JSON part of the response
#         json_match = re.search(r'\{.*\}', response, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(0)
#             skills_data = json.loads(json_str)
#         else:
#             raise ValueError("No JSON object found in the response")

#         required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
#         if all(key in skills_data for key in required_keys):
#             return skills_data
#         else:
#             missing_keys = [key for key in required_keys if key not in skills_data]
#             raise ValueError(f"Missing required keys in JSON: {', '.join(missing_keys)}")

#     except json.JSONDecodeError as e:
#         print(f"JSON Decode Error: {str(e)}")
#         print("Response causing the error:", response)
#         return {"error": f"Invalid JSON in API response: {str(e)}"}
#     except Exception as e:
#         print(f"Error in skill analysis: {str(e)}")
#         print("Response causing the error:", response)
#         return {"error": f"Error in skill analysis: {str(e)}"}

# #@app.route('/recommend_course', methods=['POST'])
# def recommend_course_api():
#     data = request.json
#     skill_name = data.get('resource')
#     if not skill_name:
#         return jsonify({'error': 'Skill name is required'}), 400
    
#     recommended_link = recommend_course(skill_name)
    
#     # Check if recommended_link is a pandas Series
#     if isinstance(recommended_link, pd.Series):
#         if recommended_link.empty:
#             return jsonify({'error': 'No recommendation found'}), 404
#         # Assuming the first item is the link
#         recommended_link = recommended_link.iloc[0]
#     elif not recommended_link:
#         return jsonify({'error': 'No recommendation found'}), 404
    
#     return jsonify({'recommendation': recommended_link})

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)







# Main



# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from datetime import datetime
# import os
# import PyPDF2
# import docx
# import json
# import re 
# from groq import Groq
# import pandas as pd
# from rec_courses import recommend_course
# from dotenv import load_dotenv

# app = Flask(__name__)
# CORS(app)
# load_dotenv()

# # Use environment variables with correct names
# connec_string = os.getenv('connec_string')
# groq_api = os.getenv('GROQ_API_KEY')

# print(f"Connection string exists: {bool(connec_string)}")
# print(f"Groq API key exists: {bool(groq_api)}")

# # Configure upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#     print(f"Created uploads directory: {UPLOAD_FOLDER}")

# # Initialize MongoDB
# client = None
# users_collection = None
# if connec_string:
#     try:
#         client = MongoClient(connec_string)
#         client.admin.command('ping')
#         print("MongoDB is connected")
#         db = client['UserTest']
#         users_collection = db['users']
#         print(f"Database connected: {db.name}")
#     except Exception as e:
#         print(f"MongoDB connection failed: {e}")
# else:
#     print("No MongoDB connection string found")

# # Initialize Groq client
# groq_client = None
# if groq_api:
#     try:
#         groq_client = Groq(api_key=groq_api)
#         print("Groq client initialized successfully")
#     except Exception as e:
#         print(f"Groq client initialization failed: {e}")
# else:
#     print("No Groq API key found")

# # === CORRECTED AUTHENTICATION ROUTES ===

# @app.route('/api/signup', methods=['POST'])
# def signup():
#     print("=== SIGNUP ENDPOINT CALLED ===")
#     try:
#         if not request.is_json:
#             return jsonify({'message': 'Request must be JSON'}), 400
        
#         data = request.get_json()
#         print(f"Received signup data: {data}")
        
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
        
#         if not name or not email or not password:
#             return jsonify({'message': 'Name, email, and password are required'}), 400
        
#         # Check if user already exists - FIXED: Compare with None
#         if users_collection is not None:
#             existing_user = users_collection.find_one({'email': email})
#             if existing_user:
#                 return jsonify({'message': 'User already exists with this email'}), 400
            
#             # Hash password and create user
#             hashed_password = generate_password_hash(password)
#             user_data = {
#                 'name': name,
#                 'email': email,
#                 'password': hashed_password,
#                 'created_at': datetime.now().isoformat(),
#                 'skills': [],
#                 'job': '',
#                 'tagline': 'A catchy tagline!'
#             }
            
#             result = users_collection.insert_one(user_data)
#             print(f"User created with ID: {result.inserted_id}")
            
#             return jsonify({
#                 'message': 'Signup successful',
#                 'user': {
#                     'name': name,
#                     'email': email
#                 }
#             }), 201
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Signup error: {e}")
#         return jsonify({'message': 'Error creating user'}), 500

# @app.route('/api/login', methods=['POST'])
# def login():
#     print("=== LOGIN ENDPOINT CALLED ===")
#     try:
#         if not request.is_json:
#             return jsonify({'message': 'Request must be JSON'}), 400
        
#         data = request.get_json()
#         print(f"Received login data: {data}")
        
#         email = data.get('email')
#         password = data.get('password')
        
#         if not email or not password:
#             return jsonify({'message': 'Email and password are required'}), 400
        
#         # FIXED: Compare with None instead of using truthy check
#         if users_collection is not None:
#             user = users_collection.find_one({'email': email})
#             if user and check_password_hash(user['password'], password):
#                 user_data = {
#                     'name': user['name'],
#                     'email': user['email'],
#                     'id': str(user['_id'])
#                 }
#                 return jsonify({
#                     'message': 'Login successful',
#                     'user': user_data
#                 }), 200
#             else:
#                 return jsonify({'message': 'Invalid email or password'}), 401
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Login error: {e}")
#         return jsonify({'message': 'Error during login'}), 500

# # Also fix the profile routes:

# @app.route('/api/user/profile', methods=['GET'])
# def get_user_profile():
#     try:
#         email = request.args.get('email')
#         if not email:
#             return jsonify({'message': 'Email is required'}), 400
        
#         # FIXED: Compare with None
#         if users_collection is not None:
#             user = users_collection.find_one({'email': email})
#             if user:
#                 user_data = {
#                     'name': user.get('name', ''),
#                     'email': user.get('email', ''),
#                     'skills': user.get('skills', []),
#                     'job': user.get('job', ''),
#                     'tagline': user.get('tagline', 'A catchy tagline!')
#                 }
#                 return jsonify({'user': user_data}), 200
#             else:
#                 return jsonify({'message': 'User not found'}), 404
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Profile error: {e}")
#         return jsonify({'message': 'Error fetching profile'}), 500

# @app.route('/api/user/profile', methods=['PUT'])
# def update_user_profile():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         updates = data.get('updates', {})
        
#         if not email or not updates:
#             return jsonify({'message': 'Email and updates are required'}), 400
        
#         # FIXED: Compare with None
#         if users_collection is not None:
#             # Remove password from updates if present
#             updates.pop('password', None)
            
#             result = users_collection.update_one(
#                 {'email': email},
#                 {'$set': updates}
#             )
            
#             if result.modified_count:
#                 return jsonify({'message': 'Profile updated successfully'}), 200
#             else:
#                 return jsonify({'message': 'No changes made or user not found'}), 400
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Update profile error: {e}")
#         return jsonify({'message': 'Error updating profile'}), 500

# # === END CORRECTED AUTHENTICATION ROUTES ===

# @app.route('/api/user/profile', methods=['PUT'])
# def update_user_profile():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         updates = data.get('updates', {})
        
#         if not email or not updates:
#             return jsonify({'message': 'Email and updates are required'}), 400
        
#         if users_collection:
#             # Remove password from updates if present
#             updates.pop('password', None)
            
#             result = users_collection.update_one(
#                 {'email': email},
#                 {'$set': updates}
#             )
            
#             if result.modified_count:
#                 return jsonify({'message': 'Profile updated successfully'}), 200
#             else:
#                 return jsonify({'message': 'No changes made or user not found'}), 400
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Update profile error: {e}")
#         return jsonify({'message': 'Error updating profile'}), 500

# @app.route('/api/skill-analyzer', methods=['POST'])
# def skill_analyzer():
#     print("=== SKILL ANALYZER ENDPOINT CALLED ===")
    
#     # Check if files are present
#     if 'resume' not in request.files:
#         print("Missing resume file")
#         return jsonify({'error': 'Resume file is required'}), 400
    
#     if 'job_description' not in request.files:
#         print("Missing job description file")
#         return jsonify({'error': 'Job description file is required'}), 400
    
#     resume_file = request.files['resume']
#     job_description_file = request.files['job_description']
    
#     # Check if files have names
#     if resume_file.filename == '':
#         return jsonify({'error': 'No resume file selected'}), 400
#     if job_description_file.filename == '':
#         return jsonify({'error': 'No job description file selected'}), 400
    
#     print(f"Processing files: {resume_file.filename}, {job_description_file.filename}")
    
#     resume_path = None
#     job_path = None
    
#     try:
#         # Secure filenames and save files
#         resume_filename = secure_filename(resume_file.filename)
#         job_filename = secure_filename(job_description_file.filename)
        
#         resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#         job_path = os.path.join(app.config['UPLOAD_FOLDER'], job_filename)
        
#         resume_file.save(resume_path)
#         job_description_file.save(job_path)
        
#         print("Files saved successfully")
        
#         # Extract text from files
#         resume_text = extract_text(resume_path)
#         job_text = extract_text(job_path)
        
#         print(f"Resume text length: {len(resume_text)}")
#         print(f"Job description text length: {len(job_text)}")
        
#         if len(resume_text.strip()) == 0:
#             return jsonify({'error': 'Could not extract text from resume file'}), 400
#         if len(job_text.strip()) == 0:
#             return jsonify({'error': 'Could not extract text from job description file'}), 400
        
#         # Analyze skills
#         skills_analysis = compare_skills(resume_text, job_text)
        
#         print("Skill analysis completed successfully")
#         return jsonify(skills_analysis)
        
#     except Exception as e:
#         print(f"Error in skill analysis: {str(e)}")
#         return jsonify({'error': f'An error occurred during skill analysis: {str(e)}'}), 500
#     finally:
#         # Clean up files
#         if resume_path and os.path.exists(resume_path):
#             os.remove(resume_path)
#             print("Resume file cleaned up")
#         if job_path and os.path.exists(job_path):
#             os.remove(job_path)
#             print("Job description file cleaned up")

# def extract_text(file_path):
#     print(f"Extracting text from: {file_path}")
#     _, file_extension = os.path.splitext(file_path)
    
#     try:
#         if file_extension.lower() == '.pdf':
#             with open(file_path, 'rb') as file:
#                 reader = PyPDF2.PdfReader(file)
#                 text = ''
#                 for page in reader.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text + ' '
#                 print(f"PDF extraction completed: {len(text)} characters")
                
#         elif file_extension.lower() in ['.docx', '.doc']:
#             doc = docx.Document(file_path)
#             text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
#             print(f"DOCX extraction completed: {len(text)} characters")
            
#         else:
#             # Try to read as text file
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     text = file.read()
#             except:
#                 with open(file_path, 'r', encoding='latin-1') as file:
#                     text = file.read()
#             print(f"Text file extraction completed: {len(text)} characters")
        
#         return text.strip()
        
#     except Exception as e:
#         print(f"Error extracting text from {file_path}: {str(e)}")
#         return ""

# def compare_skills(resume_text, job_text):
#     print("Comparing skills using Groq API...")
    
#     # If Groq client is not available, return mock data
#     if not groq_client:
#         print("Groq client not available, returning mock data")
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React", "Node.js", "MongoDB", "HTML5", "CSS3", "Git"],
#             "skills_required_in_job": ["Python", "React", "AWS", "Docker", "Kubernetes", "HTML5", "CSS3", "JavaScript"],
#             "matching_skills": ["Python", "React", "JavaScript", "HTML5", "CSS3"],
#             "skills_to_improve": ["AWS", "Docker", "Kubernetes"]
#         }
    
#     # Improved prompt with better instructions
#     prompt = f"""
#     CRITICAL INSTRUCTIONS: Extract ALL technical skills from both documents. Be thorough and comprehensive.

#     RESUME TEXT (FULL TEXT - EXTRACT ALL SKILLS):
#     {resume_text}

#     JOB DESCRIPTION TEXT (FULL TEXT - EXTRACT ALL SKILLS):
#     {job_text}

#     Analyze both documents thoroughly and provide a JSON response with these 4 arrays:

#     1. "skills_from_resume": Extract ALL technical skills mentioned in the resume including:
#        - Programming languages (Python, JavaScript, Java, C++, etc.)
#        - Frameworks (React, Angular, Vue, Django, Flask, etc.)
#        - Databases (MySQL, MongoDB, PostgreSQL, etc.)
#        - Tools (Git, Docker, AWS, Azure, etc.)
#        - Web technologies (HTML5, CSS3, REST APIs, etc.)
#        - Methodologies (Agile, Scrum, DevOps, etc.)

#     2. "skills_required_in_job": Extract ALL required skills from job description including:
#        - Mandatory skills mentioned in requirements
#        - Skills mentioned in responsibilities
#        - Technologies listed in qualifications

#     3. "matching_skills": Skills that appear in BOTH lists

#     4. "skills_to_improve": Skills from job description NOT found in resume

#     IMPORTANT: Be comprehensive. Include ALL skills you find. Don't skip common skills like HTML5, CSS3, Git, etc.

#     Return ONLY valid JSON format:
#     {{
#         "skills_from_resume": ["skill1", "skill2", "skill3", ...],
#         "skills_required_in_job": ["skill1", "skill2", "skill3", ...],
#         "matching_skills": ["skill1", "skill2", ...],
#         "skills_to_improve": ["skill1", "skill2", ...]
#     }}
#     """

#     try:
#         print("Sending request to Groq API...")
#         chat_completion = groq_client.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model="llama3-70b-8192",
#             temperature=0.1,
#             max_tokens=2000  # Increased tokens for more comprehensive response
#         )
        
#         response = chat_completion.choices[0].message.content
#         print("Raw API response received")
        
#         # Clean the response
#         response = response.strip()
        
#         # Remove markdown code blocks if present
#         if response.startswith('```json'):
#             response = response[7:]
#         if response.startswith('```'):
#             response = response[3:]
#         if response.endswith('```'):
#             response = response[:-3]
        
#         response = response.strip()
#         print(f"Cleaned response: {response[:500]}...")  # Show more of response for debugging
        
#         # Parse JSON
#         skills_data = json.loads(response)
        
#         # Validate and ensure all keys exist
#         required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
#         for key in required_keys:
#             if key not in skills_data:
#                 skills_data[key] = []
#             # Ensure values are lists and remove duplicates
#             if isinstance(skills_data[key], list):
#                 skills_data[key] = list(set([skill.strip() for skill in skills_data[key] if skill.strip()]))
        
#         print(f"Analysis results:")
#         print(f"Resume skills: {len(skills_data['skills_from_resume'])}")
#         print(f"Job skills: {len(skills_data['skills_required_in_job'])}")
#         print(f"Matching skills: {len(skills_data['matching_skills'])}")
#         print(f"Skills to improve: {len(skills_data['skills_to_improve'])}")
        
#         return skills_data

#     except json.JSONDecodeError as e:
#         print(f"JSON Decode Error: {e}")
#         print(f"Problematic response: {response}")
#         # Return comprehensive fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React", "Node.js", "MongoDB", "HTML5", "CSS3", "Git", "REST APIs"],
#             "skills_required_in_job": ["Python", "React", "AWS", "Docker", "Kubernetes", "HTML5", "CSS3", "JavaScript", "TypeScript"],
#             "matching_skills": ["Python", "React", "JavaScript", "HTML5", "CSS3"],
#             "skills_to_improve": ["AWS", "Docker", "Kubernetes", "TypeScript"]
#         }
#     except Exception as e:
#         print(f"Error in compare_skills: {e}")
#         # Return comprehensive fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React", "Node.js", "MongoDB", "HTML5", "CSS3", "Git", "REST APIs"],
#             "skills_required_in_job": ["Python", "React", "AWS", "Docker", "Kubernetes", "HTML5", "CSS3", "JavaScript", "TypeScript"],
#             "matching_skills": ["Python", "React", "JavaScript", "HTML5", "CSS3"],
#             "skills_to_improve": ["AWS", "Docker", "Kubernetes", "TypeScript"]
#         }

#     try:
#         print("Sending request to Groq API...")
#         chat_completion = groq_client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="llama3-70b-8192",
#             temperature=0.1,
#             max_tokens=1000
#         )
        
#         response = chat_completion.choices[0].message.content
#         print("Raw API response received")
        
#         # Clean the response
#         response = response.strip()
        
#         # Remove markdown code blocks if present
#         if response.startswith('```json'):
#             response = response[7:]
#         if response.startswith('```'):
#             response = response[3:]
#         if response.endswith('```'):
#             response = response[:-3]
        
#         response = response.strip()
#         print(f"Cleaned response: {response[:200]}...")
        
#         # Parse JSON
#         skills_data = json.loads(response)
        
#         # Validate required keys
#         required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
#         for key in required_keys:
#             if key not in skills_data:
#                 skills_data[key] = []
        
#         print("Skill analysis successful")
#         return skills_data

#     except json.JSONDecodeError as e:
#         print(f"JSON Decode Error: {e}")
#         print(f"Problematic response: {response}")
#         # Return fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React"],
#             "skills_required_in_job": ["Python", "React", "AWS"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS"]
#         }
#     except Exception as e:
#         print(f"Error in compare_skills: {e}")
#         # Return fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React"],
#             "skills_required_in_job": ["Python", "React", "AWS"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS"]
#         }

# @app.route('/recommend_course', methods=['POST'])
# def recommend_course_api():
#     try:
#         print("=== RECOMMEND COURSE ENDPOINT CALLED ===")
#         data = request.get_json()
#         print(f"Received data: {data}")
        
#         if not data:
#             return jsonify({'error': 'No JSON data received'}), 400
            
#         skill_name = data.get('resource')
#         print(f"Skill name received: {skill_name}")
        
#         if not skill_name:
#             return jsonify({'error': 'Skill name is required'}), 400
        
#         print(f"Course recommendation requested for: {skill_name}")
        
#         # Import and call the function
#         from rec_courses import recommend_course
#         recommended_link = recommend_course(skill_name)
        
#         print(f"Recommended link type: {type(recommended_link)}")
#         print(f"Recommended link value: {recommended_link}")
        
#         # Handle different return types
#         if isinstance(recommended_link, pd.Series):
#             if recommended_link.empty:
#                 print("Empty series returned")
#                 fallback_url = f'https://www.udemy.com/courses/search/?src=ukw&q={skill_name.replace(" ", "+")}'
#                 return jsonify({'recommendation': fallback_url})
#             recommended_link = recommended_link.iloc[0]
        
#         # Ensure it's a string
#         recommended_link = str(recommended_link).strip()
        
#         # Validate URL format
#         if not recommended_link.startswith(('http://', 'https://')):
#             print("URL doesn't start with http/https, fixing...")
#             if recommended_link.startswith('www.'):
#                 recommended_link = 'https://' + recommended_link
#             else:
#                 recommended_link = f'https://www.udemy.com{recommended_link if recommended_link.startswith("/") else "/" + recommended_link}'
        
#         print(f"Final recommended link: {recommended_link}")
#         return jsonify({'recommendation': recommended_link})
    
#     except Exception as e:
#         print(f"Error in course recommendation: {str(e)}")
#         import traceback
#         traceback.print_exc()  # This will print the full traceback
        
#         # Return a fallback URL
#         skill = data.get('resource', 'programming') if 'data' in locals() else 'programming'
#         fallback_url = f'https://www.udemy.com/courses/search/?src=ukw&q={skill.replace(" ", "+")}'
#         return jsonify({'recommendation': fallback_url})
    
#     except Exception as e:
#         print(f"Error in course recommendation: {e}")
#         return jsonify({'error': 'Internal server error'}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         'status': 'healthy',
#         'mongodb': 'connected' if client else 'disconnected',
#         'groq': 'available' if groq_client else 'unavailable',
#         'timestamp': datetime.now().isoformat()
#     })

# @app.route('/api/test', methods=['GET'])
# def test_endpoint():
#     return jsonify({'message': 'Backend is working!'})

# if __name__ == '__main__':
#     print("=== STARTING FLASK SERVER ===")
#     print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
#     print(f"MongoDB: {'Connected' if client else 'Not connected'}")
#     print(f"Groq API: {'Available' if groq_client else 'Not available'}")
#     app.run(host='0.0.0.0', port=5000, debug=True)








# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from datetime import datetime
# import os
# import PyPDF2
# import docx
# import json
# import re 
# from groq import Groq
# import pandas as pd
# from rec_courses import recommend_course
# from dotenv import load_dotenv
# import google.generativeai as genai  # ADD THIS IMPORT

# app = Flask(__name__)
# CORS(app)
# load_dotenv()

# # Use environment variables with correct names
# connec_string = os.getenv('connec_string')
# groq_api = os.getenv('GROQ_API_KEY')
# gemini_api = os.getenv('GEMINI_API_KEY')  # ADD THIS LINE

# print(f"Connection string exists: {bool(connec_string)}")
# print(f"Groq API key exists: {bool(groq_api)}")
# print(f"Gemini API key exists: {bool(gemini_api)}")  # ADD THIS LINE

# # Configure upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#     print(f"Created uploads directory: {UPLOAD_FOLDER}")

# # Initialize MongoDB
# client = None
# users_collection = None
# if connec_string:
#     try:
#         client = MongoClient(connec_string)
#         client.admin.command('ping')
#         print("MongoDB is connected")
#         db = client['UserTest']
#         users_collection = db['users']
#         print(f"Database connected: {db.name}")
#     except Exception as e:
#         print(f"MongoDB connection failed: {e}")
# else:
#     print("No MongoDB connection string found")

# # Initialize Groq client
# groq_client = None
# if groq_api:
#     try:
#         groq_client = Groq(api_key=groq_api)
#         print("Groq client initialized successfully")
#     except Exception as e:
#         print(f"Groq client initialization failed: {e}")
# else:
#     print("No Groq API key found")

# # === ADD GEMINI AI CONFIGURATION HERE ===
# gemini_model = None
# if gemini_api:
#     try:
#         genai.configure(api_key=gemini_api)
#         gemini_model = genai.GenerativeModel('gemini-pro')
#         print("Gemini AI configured successfully")
#     except Exception as e:
#         print(f"Gemini AI configuration failed: {e}")
#         gemini_model = None
# else:
#     gemini_model = None
#     print("No Gemini API key found")
# # === END OF GEMINI CONFIGURATION ===

# @app.route('/api/skill-analyzer', methods=['POST'])
# def skill_analyzer():
#     print("=== SKILL ANALYZER ENDPOINT CALLED ===")
    
#     # Check if files are present
#     if 'resume' not in request.files:
#         print("Missing resume file")
#         return jsonify({'error': 'Resume file is required'}), 400
    
#     if 'job_description' not in request.files:
#         print("Missing job description file")
#         return jsonify({'error': 'Job description file is required'}), 400
    
#     resume_file = request.files['resume']
#     job_description_file = request.files['job_description']
    
#     # Check if files have names
#     if resume_file.filename == '':
#         return jsonify({'error': 'No resume file selected'}), 400
#     if job_description_file.filename == '':
#         return jsonify({'error': 'No job description file selected'}), 400
    
#     print(f"Processing files: {resume_file.filename}, {job_description_file.filename}")
    
#     resume_path = None
#     job_path = None
    
#     try:
#         # Secure filenames and save files
#         resume_filename = secure_filename(resume_file.filename)
#         job_filename = secure_filename(job_description_file.filename)
        
#         resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#         job_path = os.path.join(app.config['UPLOAD_FOLDER'], job_filename)
        
#         resume_file.save(resume_path)
#         job_description_file.save(job_path)
        
#         print("Files saved successfully")
        
#         # Extract text from files
#         resume_text = extract_text(resume_path)
#         job_text = extract_text(job_path)
        
#         print(f"Resume text length: {len(resume_text)}")
#         print(f"Job description text length: {len(job_text)}")
        
#         if len(resume_text.strip()) == 0:
#             return jsonify({'error': 'Could not extract text from resume file'}), 400
#         if len(job_text.strip()) == 0:
#             return jsonify({'error': 'Could not extract text from job description file'}), 400
        
#         # Analyze skills
#         skills_analysis = compare_skills(resume_text, job_text)
        
#         print("Skill analysis completed successfully")
#         return jsonify(skills_analysis)
        
#     except Exception as e:
#         print(f"Error in skill analysis: {str(e)}")
#         return jsonify({'error': f'An error occurred during skill analysis: {str(e)}'}), 500
#     finally:
#         # Clean up files
#         if resume_path and os.path.exists(resume_path):
#             os.remove(resume_path)
#             print("Resume file cleaned up")
#         if job_path and os.path.exists(job_path):
#             os.remove(job_path)
#             print("Job description file cleaned up")

# def extract_text(file_path):
#     print(f"Extracting text from: {file_path}")
#     _, file_extension = os.path.splitext(file_path)
    
#     try:
#         if file_extension.lower() == '.pdf':
#             with open(file_path, 'rb') as file:
#                 reader = PyPDF2.PdfReader(file)
#                 text = ''
#                 for page in reader.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text + ' '
#                 print(f"PDF extraction completed: {len(text)} characters")
                
#         elif file_extension.lower() in ['.docx', '.doc']:
#             doc = docx.Document(file_path)
#             text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
#             print(f"DOCX extraction completed: {len(text)} characters")
            
#         else:
#             # Try to read as text file
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     text = file.read()
#             except:
#                 with open(file_path, 'r', encoding='latin-1') as file:
#                     text = file.read()
#             print(f"Text file extraction completed: {len(text)} characters")
        
#         return text.strip()
        
#     except Exception as e:
#         print(f"Error extracting text from {file_path}: {str(e)}")
#         return ""

# def compare_skills(resume_text, job_text):
#     print("Comparing skills using Groq API...")
    
#     # If Groq client is not available, return mock data
#     if not groq_client:
#         print("Groq client not available, returning mock data")
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
#             "skills_required_in_job": ["Python", "React", "AWS", "Docker", "Kubernetes"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS", "Docker", "Kubernetes"]
#         }
    
#     prompt = f"""
#     Analyze the following resume and job description to extract and compare skills.

#     RESUME TEXT:
#     {resume_text[:3000]}

#     JOB DESCRIPTION TEXT:
#     {job_text[:3000]}

#     Please provide a JSON response with exactly these 4 arrays:
#     1. "skills_from_resume" - technical skills found in the resume
#     2. "skills_required_in_job" - specific technical skills required in the job description
#     3. "matching_skills" - skills that appear in both lists
#     4. "skills_to_improve" - skills from job description not found in resume

#     Return ONLY valid JSON, no other text.
#     Example format:
#     {{
#         "skills_from_resume": ["Python", "JavaScript", "React"],
#         "skills_required_in_job": ["Python", "React", "AWS"],
#         "matching_skills": ["Python", "React"],
#         "skills_to_improve": ["AWS"]
#     }}
#     """

#     try:
#         print("Sending request to Groq API...")
#         chat_completion = groq_client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="llama3-70b-8192",
#             temperature=0.1,
#             max_tokens=1000
#         )
        
#         response = chat_completion.choices[0].message.content
#         print("Raw API response received")
        
#         # Clean the response
#         response = response.strip()
        
#         # Remove markdown code blocks if present
#         if response.startswith('```json'):
#             response = response[7:]
#         if response.startswith('```'):
#             response = response[3:]
#         if response.endswith('```'):
#             response = response[:-3]
        
#         response = response.strip()
#         print(f"Cleaned response: {response[:200]}...")
        
#         # Parse JSON
#         skills_data = json.loads(response)
        
#         # Validate required keys
#         required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
#         for key in required_keys:
#             if key not in skills_data:
#                 skills_data[key] = []
        
#         print("Skill analysis successful")
#         return skills_data

#     except json.JSONDecodeError as e:
#         print(f"JSON Decode Error: {e}")
#         print(f"Problematic response: {response}")
#         # Return fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React"],
#             "skills_required_in_job": ["Python", "React", "AWS"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS"]
#         }
#     except Exception as e:
#         print(f"Error in compare_skills: {e}")
#         # Return fallback data
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React"],
#             "skills_required_in_job": ["Python", "React", "AWS"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS"]
#         }

# @app.route('/recommend_course', methods=['POST'])
# def recommend_course_api():
#     try:
#         data = request.get_json()
#         skill_name = data.get('resource')
        
#         if not skill_name:
#             return jsonify({'error': 'Skill name is required'}), 400
        
#         print(f"Course recommendation requested for: {skill_name}")
        
#         recommended_link = recommend_course(skill_name)
        
#         # Handle pandas Series
#         if isinstance(recommended_link, pd.Series):
#             if recommended_link.empty:
#                 return jsonify({'error': 'No recommendation found'}), 404
#             recommended_link = recommended_link.iloc[0]
#         elif not recommended_link:
#             return jsonify({'error': 'No recommendation found'}), 404
        
#         return jsonify({'recommendation': recommended_link})
    
#     except Exception as e:
#         print(f"Error in course recommendation: {e}")
#         return jsonify({'error': 'Internal server error'}), 500

# # === ADD CHATBOT ROUTES HERE ===
# @app.route('/api/chat', methods=['POST'])
# def chat_with_bot():
#     try:
#         data = request.get_json()
#         user_message = data.get('message')
#         chat_history = data.get('history', [])
        
#         if not user_message:
#             return jsonify({'error': 'Message is required'}), 400
        
#         print(f"Chat message received: {user_message}")
        
#         # If Gemini is available, use it. Otherwise, use a simple rule-based response
#         if gemini_model:
#             try:
#                 # Create context for the chatbot
#                 context = """
#                 You are SkillSpark AI Assistant, a helpful career and skills advisor. 
#                 You help users with:
#                 - Skill analysis and career guidance
#                 - Learning recommendations
#                 - Resume and job description analysis
#                 - Technical skill questions
#                 - Career path suggestions
                
#                 Be friendly, professional, and focused on skills development.
#                 """
                
#                 response = gemini_model.generate_content(context + "\n\nUser: " + user_message)
#                 bot_response = response.text
                
#             except Exception as e:
#                 print(f"Gemini AI error: {e}")
#                 bot_response = get_fallback_response(user_message)
#         else:
#             bot_response = get_fallback_response(user_message)
        
#         return jsonify({
#             'response': bot_response,
#             'timestamp': datetime.now().isoformat()
#         })
        
#     except Exception as e:
#         print(f"Error in chatbot: {e}")
#         return jsonify({
#             'response': "I apologize, but I'm experiencing technical difficulties. Please try again later.",
#             'timestamp': datetime.now().isoformat()
#         }), 500

# def get_fallback_response(user_message):
#     """Fallback responses when AI is not available"""
#     message_lower = user_message.lower()
    
#     # Skill-related questions
#     if any(word in message_lower for word in ['skill', 'learn', 'study', 'course']):
#         return "I can help you with skill recommendations! Based on your profile, I suggest focusing on in-demand skills like Python, JavaScript, React, and cloud technologies. Would you like specific course recommendations?"
    
#     elif any(word in message_lower for word in ['resume', 'cv', 'profile']):
#         return "For resume improvement, I recommend highlighting your technical skills, quantifying achievements, and tailoring it to specific job descriptions. You can use our skill analyzer to compare your resume with job requirements!"
    
#     elif any(word in message_lower for word in ['job', 'career', 'interview']):
#         return "I can help you prepare for job interviews by analyzing required skills and suggesting areas for improvement. Try uploading a job description to get started!"
    
#     elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
#         return "Hello! I'm SkillSpark AI Assistant. I can help you with skill analysis, career guidance, and learning recommendations. How can I assist you today?"
    
#     elif any(word in message_lower for word in ['thank', 'thanks']):
#         return "You're welcome! I'm happy to help. Feel free to ask me anything about skills, careers, or learning resources."
    
#     else:
#         return "I'm here to help with your career and skill development questions! You can ask me about:\n• Skill recommendations\n• Resume improvement\n• Job preparation\n• Learning resources\n• Career guidance\n\nWhat would you like to know?"
# # === END OF CHATBOT ROUTES ===

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         'status': 'healthy',
#         'mongodb': 'connected' if client else 'disconnected',
#         'groq': 'available' if groq_client else 'unavailable',
#         'gemini': 'available' if gemini_model else 'unavailable',  # UPDATE THIS LINE
#         'timestamp': datetime.now().isoformat()
#     })

# @app.route('/api/test', methods=['GET'])
# def test_endpoint():
#     return jsonify({'message': 'Backend is working!'})

# @app.route('/api/test_chat', methods=['GET'])  # ADD TEST ENDPOINT
# def test_chat():
#     """Test endpoint for chatbot"""
#     return jsonify({'message': 'Chatbot endpoint is working!'})

# if __name__ == '__main__':
#     print("=== STARTING FLASK SERVER ===")
#     print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
#     print(f"MongoDB: {'Connected' if client else 'Not connected'}")
#     print(f"Groq API: {'Available' if groq_client else 'Not available'}")
#     print(f"Gemini AI: {'Available' if gemini_model else 'Not available'}")  # ADD THIS LINE
#     app.run(host='0.0.0.0', port=5000, debug=True)











# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# from datetime import datetime
# import os
# import PyPDF2
# import docx
# import json
# import re 
# from groq import Groq
# import pandas as pd
# from rec_courses import recommend_course
# from dotenv import load_dotenv
# import google.generativeai as genai

# app = Flask(__name__)
# CORS(app)
# load_dotenv()

# # Use environment variables with correct names
# connec_string = os.getenv('connec_string')
# groq_api = os.getenv('GROQ_API_KEY')
# gemini_api = os.getenv('GEMINI_API_KEY')

# print(f"Connection string exists: {bool(connec_string)}")
# print(f"Groq API key exists: {bool(groq_api)}")
# print(f"Gemini API key exists: {bool(gemini_api)}")

# # Configure upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#     print(f"Created uploads directory: {UPLOAD_FOLDER}")

# # Initialize MongoDB
# client = None
# users_collection = None
# if connec_string:
#     try:
#         client = MongoClient(connec_string)
#         client.admin.command('ping')
#         print("MongoDB is connected")
#         db = client['UserTest']
#         users_collection = db['users']
#         print(f"Database connected: {db.name}")
#     except Exception as e:
#         print(f"MongoDB connection failed: {e}")
# else:
#     print("No MongoDB connection string found")

# # Initialize Groq client
# groq_client = None
# if groq_api:
#     try:
#         groq_client = Groq(api_key=groq_api)
#         print("Groq client initialized successfully")
#     except Exception as e:
#         print(f"Groq client initialization failed: {e}")
# else:
#     print("No Groq API key found")

# # Initialize Gemini AI
# gemini_model = None
# if gemini_api:
#     try:
#         genai.configure(api_key=gemini_api)
#         gemini_model = genai.GenerativeModel('gemini-1.5-flash')
#         print("Gemini AI configured successfully")
#     except Exception as e:
#         print(f"Gemini AI configuration failed: {e}")
#         gemini_model = None
# else:
#     gemini_model = None
#     print("No Gemini API key found")

# @app.route('/api/signup', methods=['POST'])
# def signup():
#     print("=== SIGNUP ENDPOINT CALLED ===")
#     try:
#         if not request.is_json:
#             return jsonify({'message': 'Request must be JSON'}), 400
        
#         data = request.get_json()
#         print(f"Received signup data: {data}")
        
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
        
#         if not name or not email or not password:
#             return jsonify({'message': 'Name, email, and password are required'}), 400
        
#         if users_collection is not None:
#             existing_user = users_collection.find_one({'email': email})
#             if existing_user:
#                 return jsonify({'message': 'User already exists with this email'}), 400
            
#             hashed_password = generate_password_hash(password)
#             user_data = {
#                 'name': name,
#                 'email': email,
#                 'password': hashed_password,
#                 'created_at': datetime.now().isoformat(),
#                 'skills': [],
#                 'job': '',
#                 'tagline': 'A catchy tagline!'
#             }
            
#             result = users_collection.insert_one(user_data)
#             print(f"User created with ID: {result.inserted_id}")
            
#             return jsonify({
#                 'message': 'Signup successful',
#                 'user': {'name': name, 'email': email}
#             }), 201
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Signup error: {e}")
#         return jsonify({'message': 'Error creating user'}), 500

# @app.route('/api/login', methods=['POST'])
# def login():
#     print("=== LOGIN ENDPOINT CALLED ===")
#     try:
#         if not request.is_json:
#             return jsonify({'message': 'Request must be JSON'}), 400
        
#         data = request.get_json()
#         print(f"Received login data: {data}")
        
#         email = data.get('email')
#         password = data.get('password')
        
#         if not email or not password:
#             return jsonify({'message': 'Email and password are required'}), 400
        
#         if users_collection is not None:
#             user = users_collection.find_one({'email': email})
#             if user and check_password_hash(user['password'], password):
#                 user_data = {
#                     'name': user['name'],
#                     'email': user['email'],
#                     'id': str(user['_id'])
#                 }
#                 return jsonify({'message': 'Login successful', 'user': user_data}), 200
#             else:
#                 return jsonify({'message': 'Invalid email or password'}), 401
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Login error: {e}")
#         return jsonify({'message': 'Error during login'}), 500

# @app.route('/api/user/profile', methods=['GET'])
# def get_user_profile():
#     try:
#         email = request.args.get('email')
#         if not email:
#             return jsonify({'message': 'Email is required'}), 400
        
#         if users_collection is not None:
#             user = users_collection.find_one({'email': email})
#             if user:
#                 user_data = {
#                     'name': user.get('name', ''),
#                     'email': user.get('email', ''),
#                     'skills': user.get('skills', []),
#                     'job': user.get('job', ''),
#                     'tagline': user.get('tagline', 'A catchy tagline!')
#                 }
#                 return jsonify({'user': user_data}), 200
#             else:
#                 return jsonify({'message': 'User not found'}), 404
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Profile error: {e}")
#         return jsonify({'message': 'Error fetching profile'}), 500

# @app.route('/api/user/profile', methods=['PUT'])
# def update_user_profile():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         updates = data.get('updates', {})
        
#         if not email or not updates:
#             return jsonify({'message': 'Email and updates are required'}), 400
        
#         if users_collection is not None:
#             updates.pop('password', None) # Prevent password updates through this generic route
            
#             result = users_collection.update_one(
#                 {'email': email},
#                 {'$set': updates}
#             )
            
#             if result.modified_count:
#                 return jsonify({'message': 'Profile updated successfully'}), 200
#             else:
#                 return jsonify({'message': 'No changes made or user not found'}), 400
#         else:
#             return jsonify({'message': 'Database not available'}), 500
            
#     except Exception as e:
#         print(f"Update profile error: {e}")
#         return jsonify({'message': 'Error updating profile'}), 500

# # NOTE: THE DUPLICATE /api/user/profile ROUTE HAS BEEN REMOVED.

# @app.route('/api/skill-analyzer', methods=['POST'])
# def skill_analyzer():
#     print("=== SKILL ANALYZER ENDPOINT CALLED ===")
    
#     if 'resume' not in request.files or 'job_description' not in request.files:
#         return jsonify({'error': 'Both resume and job description files are required'}), 400
    
#     resume_file = request.files['resume']
#     job_description_file = request.files['job_description']
    
#     if resume_file.filename == '' or job_description_file.filename == '':
#         return jsonify({'error': 'No file selected for one or both inputs'}), 400
    
#     print(f"Processing files: {resume_file.filename}, {job_description_file.filename}")
    
#     resume_path = None
#     job_path = None
    
#     try:
#         resume_filename = secure_filename(resume_file.filename)
#         job_filename = secure_filename(job_description_file.filename)
        
#         resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#         job_path = os.path.join(app.config['UPLOAD_FOLDER'], job_filename)
        
#         resume_file.save(resume_path)
#         job_description_file.save(job_path)
        
#         print("Files saved successfully")
        
#         resume_text = extract_text(resume_path)
#         job_text = extract_text(job_path)
        
#         if not resume_text or not job_text:
#             return jsonify({'error': 'Could not extract text from one or both files'}), 400
        
#         skills_analysis = compare_skills(resume_text, job_text)
        
#         print("Skill analysis completed successfully")
#         return jsonify(skills_analysis)
        
#     except Exception as e:
#         print(f"Error in skill analysis: {str(e)}")
#         return jsonify({'error': f'An error occurred during skill analysis: {str(e)}'}), 500
#     finally:
#         if resume_path and os.path.exists(resume_path):
#             os.remove(resume_path)
#         if job_path and os.path.exists(job_path):
#             os.remove(job_path)

# def extract_text(file_path):
#     print(f"Extracting text from: {file_path}")
#     _, file_extension = os.path.splitext(file_path)
#     text = ""
#     try:
#         if file_extension.lower() == '.pdf':
#             with open(file_path, 'rb') as file:
#                 reader = PyPDF2.PdfReader(file)
#                 for page in reader.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text + ' '
#         elif file_extension.lower() in ['.docx', '.doc']:
#             doc = docx.Document(file_path)
#             text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
#         else:
#             with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
#                 text = file.read()
#         return text.strip()
#     except Exception as e:
#         print(f"Error extracting text from {file_path}: {str(e)}")
#         return ""

# def compare_skills(resume_text, job_text):
#     print("Comparing skills using Groq API...")
    
#     if not groq_client:
#         print("Groq client not available, returning mock data")
#         return {
#             "skills_from_resume": ["Python", "JavaScript", "React"],
#             "skills_required_in_job": ["Python", "React", "AWS"],
#             "matching_skills": ["Python", "React"],
#             "skills_to_improve": ["AWS"]
#         }
    
#     prompt = f"""
#     Analyze the following resume and job description to extract and compare skills.

#     RESUME TEXT:
#     {resume_text[:4000]}

#     JOB DESCRIPTION TEXT:
#     {job_text[:4000]}

#     Provide a JSON response with exactly these 4 arrays:
#     1. "skills_from_resume" - ALL technical skills found in the resume.
#     2. "skills_required_in_job" - ALL specific technical skills required in the job description.
#     3. "matching_skills" - skills that appear in BOTH lists.
#     4. "skills_to_improve" - skills from job description NOT found in resume.

#     Return ONLY valid JSON.
#     """

#     try:
#         print("Sending request to Groq API...")
#         chat_completion = groq_client.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model="llama3-70b-8192",
#             temperature=0.1,
#             max_tokens=2000
#         )
#         response = chat_completion.choices[0].message.content
#         print("Raw API response received")
        
#         # Clean the response to extract only the JSON object
#         json_match = re.search(r'\{.*\}', response, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(0)
#             skills_data = json.loads(json_str)
#         else:
#             raise ValueError("No JSON object found in the response")
        
#         # Validate and ensure all keys exist
#         required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
#         for key in required_keys:
#             if key not in skills_data:
#                 skills_data[key] = []
        
#         print("Skill analysis successful")
#         return skills_data

#     except Exception as e:
#         print(f"Error in compare_skills: {e}")
#         return {"error": f"Error in skill analysis: {str(e)}"}

# @app.route('/api/recommend_course', methods=['POST'])
# def recommend_course_api():
#     try:
#         data = request.get_json()
#         skill_name = data.get('resource')
        
#         if not skill_name:
#             return jsonify({'error': 'Skill name is required'}), 400
        
#         print(f"Course recommendation requested for: {skill_name}")
#         recommended_link = recommend_course(skill_name)
        
#         if isinstance(recommended_link, pd.Series):
#             if recommended_link.empty:
#                 return jsonify({'error': 'No recommendation found'}), 404
#             recommended_link = recommended_link.iloc[0]
#         elif not recommended_link:
#             return jsonify({'error': 'No recommendation found'}), 404
        
#         return jsonify({'recommendation': str(recommended_link)})
    
#     except Exception as e:
#         print(f"Error in course recommendation: {e}")
#         # Return a fallback Udemy search URL in case of any error
#         fallback_url = f'https://www.udemy.com/courses/search/?src=ukw&q={skill_name.replace(" ", "+")}'
#         return jsonify({'recommendation': fallback_url})

# @app.route('/api/chat', methods=['POST'])
# def chat_with_bot():
#     try:
#         data = request.get_json()
#         user_message = data.get('message')
#         if not user_message:
#             return jsonify({'error': 'Message is required'}), 400
        
#         print(f"Chat message received: {user_message}")
        
#         if gemini_model:
#             try:
#                 context = "You are SkillSpark AI Assistant, a helpful career and skills advisor."
#                 response = gemini_model.generate_content(context + "\n\nUser: " + user_message)
#                 bot_response = response.text
#             except Exception as e:
#                 print(f"Gemini AI error: {e}")
#                 bot_response = get_fallback_response(user_message)
#         else:
#             bot_response = get_fallback_response(user_message)
        
#         return jsonify({'response': bot_response})
        
#     except Exception as e:
#         print(f"Error in chatbot: {e}")
#         return jsonify({'response': "I'm experiencing technical difficulties."}), 500

# def get_fallback_response(user_message):
#     message_lower = user_message.lower()
#     if any(word in message_lower for word in ['skill', 'learn', 'course']):
#         return "I can help you with skill recommendations! What skill are you interested in?"
#     elif 'hello' in message_lower or 'hi' in message_lower:
#         return "Hello! I'm SkillSpark AI. How can I help you with your career today?"
#     else:
#         return "I'm here to help with your career and skill development. Ask me about a specific skill!"

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         'status': 'healthy',
#         'mongodb': 'connected' if client else 'disconnected',
#         'groq': 'available' if groq_client else 'unavailable',
#         'gemini': 'available' if gemini_model else 'unavailable',
#         'timestamp': datetime.now().isoformat()
#     })

# if __name__ == '__main__':
#     print("=== STARTING FLASK SERVER ===")
#     print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
#     print(f"MongoDB: {'Connected' if client else 'Not connected'}")
#     print(f"Groq API: {'Available' if groq_client else 'Not available'}")
#     print(f"Gemini AI: {'Available' if gemini_model else 'Not available'}")
#     app.run(host='0.0.0.0', port=5000, debug=True)


 




# Final answer last 


from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import PyPDF2
import docx
import json
import re 
from groq import Groq
import pandas as pd
from rec_courses import recommend_course
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

# Use environment variables with correct names
connec_string = os.getenv('connec_string')
groq_api = os.getenv('GROQ_API_KEY')

print(f"Connection string exists: {bool(connec_string)}")
print(f"Groq API key exists: {bool(groq_api)}")

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created uploads directory: {UPLOAD_FOLDER}")

# Initialize MongoDB
client = None
users_collection = None
if connec_string:
    try:
        client = MongoClient(connec_string)
        client.admin.command('ping')
        print("MongoDB is connected")
        db = client['UserTest']
        users_collection = db['users']
        print(f"Database connected: {db.name}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        client = None
        users_collection = None
else:
    print("No MongoDB connection string found")
    users_collection = None

# Initialize Groq client
groq_client = None
if groq_api:
    try:
        groq_client = Groq(api_key=groq_api)
        print("Groq client initialized successfully")
    except Exception as e:
        print(f"Groq client initialization failed: {e}")
        groq_client = None
else:
    print("No Groq API key found")
    groq_client = None

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/signup', methods=['POST'])
def signup():
    print("=== SIGNUP ENDPOINT CALLED ===")
    try:
        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'}), 400
        
        data = request.get_json()
        print(f"Received signup data: {data}")
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({'message': 'Name, email, and password are required'}), 400
        
        # Check if user already exists
        if users_collection is not None:
            existing_user = users_collection.find_one({'email': email})
            if existing_user:
                return jsonify({'message': 'User already exists with this email'}), 400
            
            # Hash password and create user
            hashed_password = generate_password_hash(password)
            user_data = {
                'name': name,
                'email': email,
                'password': hashed_password,
                'created_at': datetime.now().isoformat(),
                'skills': [],
                'job': '',
                'tagline': 'A catchy tagline!'
            }
            
            result = users_collection.insert_one(user_data)
            print(f"User created with ID: {result.inserted_id}")
            
            return jsonify({
                'message': 'Signup successful',
                'user': {
                    'name': name,
                    'email': email
                }
            }), 201
        else:
            return jsonify({'message': 'Database not available'}), 500
            
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'message': 'Error creating user'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    print("=== LOGIN ENDPOINT CALLED ===")
    try:
        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'}), 400
        
        data = request.get_json()
        print(f"Received login data: {data}")
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        if users_collection is not None:
            user = users_collection.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                user_data = {
                    'name': user['name'],
                    'email': user['email'],
                    'id': str(user['_id'])
                }
                return jsonify({
                    'message': 'Login successful',
                    'user': user_data
                }), 200
            else:
                return jsonify({'message': 'Invalid email or password'}), 401
        else:
            return jsonify({'message': 'Database not available'}), 500
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': 'Error during login'}), 500

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'message': 'Email is required'}), 400
        
        if users_collection is not None:
            user = users_collection.find_one({'email': email})
            if user:
                user_data = {
                    'name': user.get('name', ''),
                    'email': user.get('email', ''),
                    'skills': user.get('skills', []),
                    'job': user.get('job', ''),
                    'tagline': user.get('tagline', 'A catchy tagline!')
                }
                return jsonify({'user': user_data}), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        else:
            return jsonify({'message': 'Database not available'}), 500
            
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({'message': 'Error fetching profile'}), 500

@app.route('/api/user/profile', methods=['PUT'])
def update_user_profile():
    try:
        data = request.get_json()
        email = data.get('email')
        updates = data.get('updates', {})
        
        if not email or not updates:
            return jsonify({'message': 'Email and updates are required'}), 400
        
        if users_collection is not None:
            # Remove password from updates if present
            updates.pop('password', None)
            
            result = users_collection.update_one(
                {'email': email},
                {'$set': updates}
            )
            
            if result.modified_count:
                return jsonify({'message': 'Profile updated successfully'}), 200
            else:
                return jsonify({'message': 'No changes made or user not found'}), 400
        else:
            return jsonify({'message': 'Database not available'}), 500
            
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'message': 'Error updating profile'}), 500

# ==================== SKILL ANALYZER ROUTE ====================

@app.route('/api/skill-analyzer', methods=['POST'])
def skill_analyzer():
    print("=== SKILL ANALYZER ENDPOINT CALLED ===")
    
    # Check if files are present
    if 'resume' not in request.files:
        print("Missing resume file")
        return jsonify({'error': 'Resume file is required'}), 400
    
    if 'job_description' not in request.files:
        print("Missing job description file")
        return jsonify({'error': 'Job description file is required'}), 400
    
    resume_file = request.files['resume']
    job_description_file = request.files['job_description']
    
    # Check if files have names
    if resume_file.filename == '':
        return jsonify({'error': 'No resume file selected'}), 400
    if job_description_file.filename == '':
        return jsonify({'error': 'No job description file selected'}), 400
    
    print(f"Processing files: {resume_file.filename}, {job_description_file.filename}")
    
    resume_path = None
    job_path = None
    
    try:
        # Secure filenames and save files
        resume_filename = secure_filename(resume_file.filename)
        job_filename = secure_filename(job_description_file.filename)
        
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], job_filename)
        
        resume_file.save(resume_path)
        job_description_file.save(job_path)
        
        print("Files saved successfully")
        
        # Extract text from files
        resume_text = extract_text(resume_path)
        job_text = extract_text(job_path)
        
        print(f"Resume text length: {len(resume_text)}")
        print(f"Job description text length: {len(job_text)}")
        
        if len(resume_text.strip()) == 0:
            return jsonify({'error': 'Could not extract text from resume file'}), 400
        if len(job_text.strip()) == 0:
            return jsonify({'error': 'Could not extract text from job description file'}), 400
        
        # Analyze skills
        skills_analysis = compare_skills(resume_text, job_text)
        
        print("Skill analysis completed successfully")
        return jsonify(skills_analysis)
        
    except Exception as e:
        print(f"Error in skill analysis: {str(e)}")
        return jsonify({'error': f'An error occurred during skill analysis: {str(e)}'}), 500
    finally:
        # Clean up files
        if resume_path and os.path.exists(resume_path):
            os.remove(resume_path)
            print("Resume file cleaned up")
        if job_path and os.path.exists(job_path):
            os.remove(job_path)
            print("Job description file cleaned up")

def extract_text(file_path):
    print(f"Extracting text from: {file_path}")
    _, file_extension = os.path.splitext(file_path)
    
    try:
        if file_extension.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + ' '
                print(f"PDF extraction completed: {len(text)} characters")
                
        elif file_extension.lower() in ['.docx', '.doc']:
            doc = docx.Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
            print(f"DOCX extraction completed: {len(text)} characters")
            
        else:
            # Try to read as text file
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            except:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
            print(f"Text file extraction completed: {len(text)} characters")
        
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
        return ""

def compare_skills(resume_text, job_text):
    print("Comparing skills using Groq API...")
    
    # If Groq client is not available, return mock data
    if not groq_client:
        print("Groq client not available, returning mock data")
        return {
            "skills_from_resume": ["Python", "JavaScript", "React", "Node.js", "MongoDB", "HTML5", "CSS3", "Git"],
            "skills_required_in_job": ["Python", "React", "AWS", "Docker", "Kubernetes", "HTML5", "CSS3", "JavaScript"],
            "matching_skills": ["Python", "React", "JavaScript", "HTML5", "CSS3"],
            "skills_to_improve": ["AWS", "Docker", "Kubernetes"]
        }
    
    prompt = f"""
    Analyze the following resume and job description to extract and compare skills.

    RESUME TEXT:
    {resume_text[:3000]}

    JOB DESCRIPTION TEXT:
    {job_text[:3000]}

    Please provide a JSON response with exactly these 4 arrays:
    1. "skills_from_resume" - technical skills found in the resume
    2. "skills_required_in_job" - specific technical skills required in the job description
    3. "matching_skills" - skills that appear in both lists
    4. "skills_to_improve" - skills from job description not found in resume

    Return ONLY valid JSON, no other text.
    Example format:
    {{
        "skills_from_resume": ["Python", "JavaScript", "React"],
        "skills_required_in_job": ["Python", "React", "AWS"],
        "matching_skills": ["Python", "React"],
        "skills_to_improve": ["AWS"]
    }}
    """

    try:
        print("Sending request to Groq API...")
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            # model="llama3-70b-8192",
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1000
        )
        
        response = chat_completion.choices[0].message.content
        print("Raw API response received")
        
        # Clean the response
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith('```json'):
            response = response[7:]
        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        
        response = response.strip()
        print(f"Cleaned response: {response[:200]}...")
        
        # Parse JSON
        skills_data = json.loads(response)
        
        # Validate required keys
        required_keys = ["skills_from_resume", "skills_required_in_job", "matching_skills", "skills_to_improve"]
        for key in required_keys:
            if key not in skills_data:
                skills_data[key] = []
        
        print("Skill analysis successful")
        return skills_data

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Problematic response: {response}")
        # Return fallback data
        return {
            "skills_from_resume": ["Python", "JavaScript", "React", "HTML5", "CSS3"],
            "skills_required_in_job": ["Python", "React", "AWS", "Docker", "HTML5", "CSS3"],
            "matching_skills": ["Python", "React", "HTML5", "CSS3"],
            "skills_to_improve": ["AWS", "Docker"]
        }
    except Exception as e:
        print(f"Error in compare_skills: {e}")
        # Return fallback data
        return {
            "skills_from_resume": ["Python", "JavaScript", "React", "HTML5", "CSS3"],
            "skills_required_in_job": ["Python", "React", "AWS", "Docker", "HTML5", "CSS3"],
            "matching_skills": ["Python", "React", "HTML5", "CSS3"],
            "skills_to_improve": ["AWS", "Docker"]
        }

# ==================== COURSE RECOMMENDATION ====================

@app.route('/recommend_course', methods=['POST'])
def recommend_course_api():
    try:
        print("=== RECOMMEND COURSE ENDPOINT CALLED ===")
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        skill_name = data.get('resource')
        
        if not skill_name:
            return jsonify({'error': 'Skill name is required'}), 400
        
        print(f"Course recommendation requested for: {skill_name}")
        
        recommended_link = recommend_course(skill_name)
        
        # Handle pandas Series
        if isinstance(recommended_link, pd.Series):
            if recommended_link.empty:
                return jsonify({'error': 'No recommendation found'}), 404
            recommended_link = recommended_link.iloc[0]
        elif not recommended_link:
            return jsonify({'error': 'No recommendation found'}), 404
        
        # Ensure it's a string
        recommended_link = str(recommended_link).strip()
        
        # Validate URL format
        if not recommended_link.startswith(('http://', 'https://')):
            if recommended_link.startswith('www.'):
                recommended_link = 'https://' + recommended_link
            else:
                recommended_link = f'https://www.udemy.com{recommended_link if recommended_link.startswith("/") else "/" + recommended_link}'
        
        print(f"Final recommended link: {recommended_link}")
        return jsonify({'recommendation': recommended_link})
    
    except Exception as e:
        print(f"Error in course recommendation: {e}")
        # Return a fallback URL
        skill = data.get('resource', 'programming') if 'data' in locals() else 'programming'
        fallback_url = f'https://www.udemy.com/courses/search/?src=ukw&q={skill.replace(" ", "+")}'
        return jsonify({'recommendation': fallback_url})

# ==================== CHATBOT ROUTE ====================

@app.route('/api/chat', methods=['POST'])
def chat_with_bot():
    try:
        print("=== CHAT ENDPOINT CALLED ===")
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()
        
        print(f"User message: {user_message}")
        
        # Simple rule-based responses
        if not user_message:
            response = "Hello! I'm SkillSpark AI Assistant. How can I help you today?"
        elif any(word in user_message for word in ['hello', 'hi', 'hey']):
            response = "Hello! 👋 I'm SkillSpark AI Assistant. I can help you with skill analysis, career guidance, and learning recommendations!"
        elif any(word in user_message for word in ['skill', 'learn', 'study']):
            response = "I recommend focusing on: Python, JavaScript, React, Cloud technologies, and AI/ML skills! 🚀"
        elif any(word in user_message for word in ['resume', 'cv']):
            response = "For resume tips: Highlight projects, quantify achievements, and tailor to job descriptions! 📄"
        elif any(word in user_message for word in ['job', 'career', 'interview']):
            response = "Job search advice: Network actively, practice interviews, and build a strong portfolio! 💼"
        elif any(word in user_message for word in ['thank']):
            response = "You're welcome! 😊 Happy to help with your career journey!"
        else:
            response = "I can help with: Skills development, Resume improvement, Job search strategies, and Career guidance! What would you like to know? 🎯"
        
        print(f"Bot response: {response}")
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            'response': "Hello! I'm here to help with your career development. Ask me anything!",
            'timestamp': datetime.now().isoformat()
        })

# ==================== TEST ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'mongodb': 'connected' if client else 'disconnected',
        'groq': 'available' if groq_client else 'unavailable',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Backend is working!'})

@app.route('/api/test_chat', methods=['GET'])
def test_chat():
    return jsonify({'message': 'Chatbot endpoint is working!'})

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=== STARTING FLASK SERVER ===")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"MongoDB: {'Connected' if client else 'Not connected'}")
    print(f"Groq API: {'Available' if groq_client else 'Not available'}")
    app.run(host='0.0.0.0', port=5000, debug=True)