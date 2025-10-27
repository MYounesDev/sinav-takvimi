"""
Create sample Excel files from CSV templates
Run this script to generate sample .xlsx files for testing
"""

import pandas as pd
import os

def create_sample_files():
    """Create sample Excel files from CSV"""
    
    # Ensure examples directory exists
    os.makedirs('examples', exist_ok=True)
    
    # Create sample courses Excel
    courses_data = {
        'code': ['CS101', 'CS102', 'CS201', 'CS202', 'CS301', 'CS302', 'CS303', 'CS401', 'CS402', 'CS403'],
        'name': [
            'Introduction to Programming',
            'Data Structures and Algorithms',
            'Object Oriented Programming',
            'Database Systems',
            'Operating Systems',
            'Computer Networks',
            'Software Engineering',
            'Artificial Intelligence',
            'Machine Learning',
            'Web Development'
        ],
        'instructor': [
            'Dr. Ahmet Yılmaz',
            'Dr. Ayşe Demir',
            'Dr. Mehmet Kaya',
            'Dr. Fatma Şahin',
            'Dr. Ali Özkan',
            'Dr. Zeynep Çelik',
            'Dr. Mustafa Arslan',
            'Prof. Dr. Esra Yıldız',
            'Prof. Dr. Can Öztürk',
            'Dr. Selin Koç'
        ],
        'class_level': [1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
        'type': ['mandatory', 'mandatory', 'mandatory', 'mandatory', 'mandatory', 
                'mandatory', 'mandatory', 'elective', 'elective', 'elective']
    }
    
    df_courses = pd.DataFrame(courses_data)
    df_courses.to_excel('examples/sample_courses.xlsx', index=False)
    print("✅ Created: examples/sample_courses.xlsx")
    
    # Create sample students Excel
    students_data = {
        'student_no': [
            '20210001', '20210002', '20210003', '20210004', '20210005',
            '20210006', '20210007', '20210008', '20210009', '20210010',
            '20210011', '20210012', '20210013', '20210014', '20210015'
        ],
        'name': [
            'Ahmet Yılmaz', 'Ayşe Demir', 'Mehmet Kaya', 'Fatma Şahin', 'Ali Özkan',
            'Zeynep Çelik', 'Mustafa Arslan', 'Esra Yıldız', 'Can Öztürk', 'Selin Koç',
            'Burak Aydın', 'Deniz Şen', 'Emre Güneş', 'Gül Yavuz', 'Hakan Polat'
        ],
        'class_level': [2, 2, 2, 1, 3, 3, 3, 4, 4, 4, 1, 1, 2, 2, 3],
        'course_codes': [
            'CS101,CS102,CS201',
            'CS101,CS102,CS201,CS202',
            'CS102,CS201,CS202',
            'CS101',
            'CS201,CS301,CS302,CS303',
            'CS301,CS302,CS303',
            'CS302,CS303',
            'CS401,CS402,CS403',
            'CS401,CS402',
            'CS402,CS403',
            'CS101',
            'CS101',
            'CS101,CS102,CS201',
            'CS102,CS201,CS202',
            'CS301,CS302'
        ]
    }
    
    df_students = pd.DataFrame(students_data)
    df_students.to_excel('examples/sample_students.xlsx', index=False)
    print("✅ Created: examples/sample_students.xlsx")
    
    print("\n✨ Sample Excel files created successfully!")
    print("📁 Location: examples/")
    print("\nYou can now import these files in the application:")
    print("  1. Import courses: examples/sample_courses.xlsx")
    print("  2. Import students: examples/sample_students.xlsx")


if __name__ == "__main__":
    create_sample_files()



