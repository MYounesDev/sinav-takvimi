"""
Exam Scheduling Algorithm
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set
from src.database.db_manager import db_manager

class ExamScheduler:
    """Algorithm for scheduling exams with conflict prevention"""
    
    def __init__(self, department_id: int):
        self.department_id = department_id
        self.courses = []
        self.students = []
        self.classrooms = []
        self.student_courses = {}  
        self.course_students = {}  
        
    def load_data(self):
        """Load courses, students, and classrooms from database"""
        query = "SELECT * FROM courses WHERE department_id = ? AND isActive = 1"
        self.courses = list(db_manager.execute_query(query, (self.department_id,)))
        
        query = "SELECT * FROM classrooms WHERE department_id = ? ORDER BY capacity DESC"
        self.classrooms = list(db_manager.execute_query(query, (self.department_id,)))
        
        query = """
            SELECT s.id as student_id, c.id as course_id
            FROM students s
            JOIN student_courses sc ON s.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE s.department_id = ? AND c.isActive = 1
        """
        enrollments = db_manager.execute_query(query, (self.department_id,))
        
        self.student_courses = {}
        self.course_students = {}
        
        for enrollment in enrollments:
            student_id = enrollment['student_id']
            course_id = enrollment['course_id']
            
            if student_id not in self.student_courses:
                self.student_courses[student_id] = set()
            self.student_courses[student_id].add(course_id)
            
            if course_id not in self.course_students:
                self.course_students[course_id] = set()
            self.course_students[course_id].add(student_id)
    
    def schedule_exams(self, start_date: datetime, end_date: datetime, 
                      disabled_days: List[int], exam_duration: int = 75, 
                      break_time: int = 15, prevent_conflicts: bool = True) -> List[Dict]:
        """
        Generate exam schedule
        
        Args:
            start_date: Start date for exams
            end_date: End date for exams
            disabled_days: List of weekday numbers to skip (0=Monday, 6=Sunday)
            exam_duration: Exam duration in minutes
            break_time: Break time between exams in minutes
            prevent_conflicts: Whether to prevent student conflicts
            
        Returns:
            List of scheduled exams with room assignments
        """
        self.load_data()
        
        if not self.courses:
            return []
        
        if not self.classrooms:
            raise ValueError("No classrooms available. Please add classrooms first.")
        
        time_slots = self._generate_time_slots(start_date, end_date, disabled_days, 
                                               exam_duration, break_time)
        
        if not time_slots:
            raise ValueError("No valid time slots available in the given date range.")
        
        courses_with_count = []
        for course in self.courses:
            student_count = len(self.course_students.get(course['id'], set()))
            courses_with_count.append((course, student_count))
        
        courses_with_count.sort(key=lambda x: x[1], reverse=True)
        
        scheduled_exams = []
        scheduled_courses = set()
        
        slot_students = {i: set() for i in range(len(time_slots))}
        
        for course, student_count in courses_with_count:
            course_id = course['id']
            
            slot_index = None
            
            if prevent_conflicts:
                course_student_ids = self.course_students.get(course_id, set())
                
                for i, slot in enumerate(time_slots):
                    if not slot_students[i].intersection(course_student_ids):
                        slot_index = i
                        break
            else:
                slot_index = len(scheduled_exams) % len(time_slots)
            
            if slot_index is None:
                slot_index = len(scheduled_exams) % len(time_slots)
            
            slot = time_slots[slot_index]
            
            assigned_classrooms = self._assign_classrooms(student_count)
            
            if not assigned_classrooms:
                assigned_classrooms = [self.classrooms[0]['id']]
            
            exam = {
                'course_id': course_id,
                'course_code': course['code'],
                'course_name': course['name'],
                'date': slot['date'].strftime('%Y-%m-%d'),
                'start_time': slot['start_time'],
                'duration': exam_duration,
                'student_count': student_count,
                'classrooms': assigned_classrooms
            }
            
            scheduled_exams.append(exam)
            scheduled_courses.add(course_id)
            
            if prevent_conflicts:
                slot_students[slot_index].update(self.course_students.get(course_id, set()))
        
        return scheduled_exams
    
    def _generate_time_slots(self, start_date: datetime, end_date: datetime, 
                           disabled_days: List[int], exam_duration: int, 
                           break_time: int) -> List[Dict]:
        """Generate available time slots for exams"""
        time_slots = []
        
        session_times = [
            "09:00",
            "11:00",
            "14:00",
            "16:00"
        ]
        
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.weekday() not in disabled_days:
                for start_time in session_times:
                    time_slots.append({
                        'date': current_date,
                        'start_time': start_time
                    })
            
            current_date += timedelta(days=1)
        
        return time_slots
    
    def _assign_classrooms(self, student_count: int) -> List[int]:
        """
        Assign classroom(s) to accommodate students
        
        Args:
            student_count: Number of students
            
        Returns:
            List of classroom IDs
        """
        if student_count == 0:
            return [self.classrooms[0]['id']] if self.classrooms else []
        
        assigned = []
        remaining = student_count
        
        for classroom in self.classrooms:
            if remaining <= 0:
                break
            
            assigned.append(classroom['id'])
            remaining -= classroom['capacity']
        
        return assigned
    
    def save_schedule(self, scheduled_exams: List[Dict], exam_type: str = 'final') -> int:
        """
        Save scheduled exams to database
        
        Args:
            scheduled_exams: List of scheduled exam dictionaries
            exam_type: Type of exam (final, midterm, resit)
            
        Returns:
            Number of exams saved
        """
        db_manager.execute_update("DELETE FROM exams WHERE department_id = ?", 
                                 (self.department_id,))
        
        saved_count = 0
        
        for exam in scheduled_exams:
            display_id = db_manager.get_next_display_id('exams')
            
            query = """
                INSERT INTO exams (display_id, course_id, department_id, date, start_time, duration, exam_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            exam_id = db_manager.execute_update(query, (
                display_id,
                exam['course_id'],
                self.department_id,
                exam['date'],
                exam['start_time'],
                exam['duration'],
                exam_type
            ))
            
            for classroom_id in exam['classrooms']:
                query = """
                    INSERT INTO exam_classrooms (exam_id, classroom_id)
                    VALUES (?, ?)
                """
                db_manager.execute_update(query, (exam_id, classroom_id))
            
            saved_count += 1
        
        return saved_count

