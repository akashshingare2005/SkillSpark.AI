import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def recommend_course(input_skill, num_of_rec=1):
    try:
        # Check if dataset exists
        if not os.path.exists("sampled_data.csv"):
            print("Dataset file not found. Using fallback recommendations.")
            return get_fallback_course(input_skill)
        
        # Load your dataset
        df = pd.read_csv("sampled_data.csv")
        
        # Check if dataset has required columns
        if 'title' not in df.columns or 'course_url' not in df.columns:
            print("Dataset missing required columns. Using fallback recommendations.")
            return get_fallback_course(input_skill)
        
        # Clean the course titles
        df['cleaned_title'] = df['title'].apply(nfx.remove_stopwords)
        df['cleaned_title'] = df['cleaned_title'].apply(nfx.remove_special_characters)

        # Vectorize the cleaned titles using TfidfVectorizer
        tfidf_vect = TfidfVectorizer()
        tfidf_mat = tfidf_vect.fit_transform(df['cleaned_title'])

        # Clean the input skill
        cleaned_input_skill = nfx.remove_stopwords(input_skill)
        cleaned_input_skill = nfx.remove_special_characters(cleaned_input_skill)
        
        # Vectorize the input skill using the same vectorizer
        input_vec = tfidf_vect.transform([cleaned_input_skill])
        
        # Calculate cosine similarity of the input skill with all titles in the dataset
        cosine_sim_scores = cosine_similarity(input_vec, tfidf_mat).flatten()
        
        # Get indices of courses sorted by similarity
        sorted_indices = cosine_sim_scores.argsort()[::-1][:num_of_rec]
        
        # Check if we have any recommendations
        if len(sorted_indices) == 0 or cosine_sim_scores[sorted_indices[0]] < 0.1:
            print(f"No good matches found for '{input_skill}'. Using fallback.")
            return get_fallback_course(input_skill)
        
        # Get the top recommendation
        top_course_index = sorted_indices[0]
        course_url = df.iloc[top_course_index]['course_url']
        similarity_score = cosine_sim_scores[top_course_index]
        
        print(f"Recommended course for '{input_skill}': {df.iloc[top_course_index]['title']}")
        print(f"Similarity score: {similarity_score:.3f}")
        
        # Ensure the URL is properly formatted
        if pd.isna(course_url) or course_url == '':
            return get_fallback_course(input_skill)
            
        # Make sure the URL is complete
        if not str(course_url).startswith('http'):
            if str(course_url).startswith('/'):
                course_url = 'https://www.udemy.com' + str(course_url)
            else:
                course_url = 'https://www.udemy.com/' + str(course_url)
        
        return str(course_url).strip()
        
    except Exception as e:
        print(f"Error in course recommendation for '{input_skill}': {e}")
        return get_fallback_course(input_skill)

def get_fallback_course(skill_name):
    """Fallback course recommendations when dataset is not available"""
    fallback_courses = {
        'python': 'https://www.udemy.com/course/python-the-complete-python-developer-course/',
        'javascript': 'https://www.udemy.com/course/the-complete-javascript-course/',
        'react': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/',
        'html': 'https://www.udemy.com/course/html5-fundamentals-for-beginners/',
        'html5': 'https://www.udemy.com/course/html5-fundamentals-for-beginners/',
        'css': 'https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/',
        'css3': 'https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/',
        'node': 'https://www.udemy.com/course/the-complete-nodejs-developer-course-2/',
        'node.js': 'https://www.udemy.com/course/the-complete-nodejs-developer-course-2/',
        'mongodb': 'https://www.udemy.com/course/mongodb-the-complete-developers-guide/',
        'aws': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate/',
        'docker': 'https://www.udemy.com/course/docker-mastery/',
        'kubernetes': 'https://www.udemy.com/course/kubernetesmastery/',
        'git': 'https://www.udemy.com/course/git-complete/',
        'typescript': 'https://www.udemy.com/course/typescript-the-complete-developers-guide/',
        'rest': 'https://www.udemy.com/course/rest-api-flask-and-python/',
        'api': 'https://www.udemy.com/course/rest-api-flask-and-python/',
        'java': 'https://www.udemy.com/course/java-the-complete-java-developer-course/',
        'angular': 'https://www.udemy.com/course/the-complete-guide-to-angular-2/',
        'vue': 'https://www.udemy.com/course/vuejs-2-the-complete-guide/',
        'django': 'https://www.udemy.com/course/python-django-the-complete-guide/',
        'flask': 'https://www.udemy.com/course/python-flask-for-beginners/',
        'mysql': 'https://www.udemy.com/course/mysql-for-beginners-course/',
        'postgresql': 'https://www.udemy.com/course/postgresql-for-beginners/',
        'sql': 'https://www.udemy.com/course/sql-for-beginners-course/',
        'azure': 'https://www.udemy.com/course/azure-az-900-azure-fundamentals/',
        'agile': 'https://www.udemy.com/course/agile-scrum-foundations/',
        'scrum': 'https://www.udemy.com/course/scrum-master-certification/',
        'devops': 'https://www.udemy.com/course/decodingdevops/',
        'machine learning': 'https://www.udemy.com/course/machinelearning/',
        'ml': 'https://www.udemy.com/course/machinelearning/',
        'ai': 'https://www.udemy.com/course/artificial-intelligence-az/',
        'data science': 'https://www.udemy.com/course/data-science-course/'
    }
    
    skill_lower = skill_name.lower().strip()
    
    # Exact match
    if skill_lower in fallback_courses:
        return fallback_courses[skill_lower]
    
    # Partial match
    for skill, url in fallback_courses.items():
        if skill in skill_lower:
            return url
    
    # Final fallback - Google search
    return f'https://www.google.com/search?q={skill_name.replace(" ", "+")}+online+course'

# Test function
if __name__ == "__main__":
    # Test the function
    test_skills = ["python", "react", "HTML5", "CSS3", "machine learning"]
    for skill in test_skills:
        result = recommend_course(skill)
        print(f"{skill}: {result}")