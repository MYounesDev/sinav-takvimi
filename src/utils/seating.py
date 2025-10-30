"""
Seating Plan Generator
"""

from typing import List, Dict
from src.database.db_manager import db_manager
import random

class SeatingPlanGenerator:
    """Generate seating arrangements for exams"""
    
    def __init__(self, exam_id: int):
        self.exam_id = exam_id
        
    def generate_seating(self) -> bool:
        """
        Generate seating plan for an exam
        
        Returns:
            True if successful, False otherwise
        """
        exam_query = """
            SELECT e.*, c.code as course_code
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            WHERE e.id = ?
        """
        exam_result = db_manager.execute_query(exam_query, (self.exam_id,))
        
        if not exam_result:
            return False
        
        exam = exam_result[0]
        
        students_query = """
            SELECT s.id, s.student_no, s.name
            FROM students s
            JOIN student_courses sc ON s.id = sc.student_id
            WHERE sc.course_id = ?
            ORDER BY s.student_no
        """
        students = list(db_manager.execute_query(students_query, (exam['course_id'],)))
        
        if not students:
            return False
        
        classrooms_query = """
            SELECT cl.*
            FROM classrooms cl
            JOIN exam_classrooms ec ON cl.id = ec.classroom_id
            WHERE ec.exam_id = ?
            ORDER BY cl.capacity DESC
        """
        classrooms = list(db_manager.execute_query(classrooms_query, (self.exam_id,)))
        
        if not classrooms:
            return False
        
        db_manager.execute_update("DELETE FROM exam_seating WHERE exam_id = ?", (self.exam_id,))
        
        random.shuffle(students)
        
        student_idx = 0
        
        for classroom in classrooms:
            if student_idx >= len(students):
                break
            
            total_seats = classroom['rows'] * classroom['cols'] * classroom['seats_per_desk']
            
            for row in range(classroom['rows']):
                for col in range(classroom['cols']):
                    for seat_pos in range(1, classroom['seats_per_desk'] + 1):
                        if student_idx >= len(students):
                            break
                        
                        student = students[student_idx]
                        
                        query = """
                            INSERT INTO exam_seating 
                            (exam_id, student_id, classroom_id, row, col, seat_position)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """
                        db_manager.execute_update(query, (
                            self.exam_id,
                            student['id'],
                            classroom['id'],
                            row,
                            col,
                            seat_pos
                        ))
                        
                        student_idx += 1
        
        return True
    
    def get_seating_by_classroom(self, classroom_id: int) -> Dict:
        """
        Get seating arrangement for a specific classroom
        
        Args:
            classroom_id: Classroom ID
            
        Returns:
            Dictionary with classroom info and seating grid
        """
        classroom_query = "SELECT * FROM classrooms WHERE id = ?"
        classroom_result = db_manager.execute_query(classroom_query, (classroom_id,))
        
        if not classroom_result:
            return None
        
        classroom = dict(classroom_result[0])
        
        seating_query = """
            SELECT es.*, s.student_no, s.name
            FROM exam_seating es
            JOIN students s ON es.student_id = s.id
            WHERE es.exam_id = ? AND es.classroom_id = ?
            ORDER BY es.row, es.col, es.seat_position
        """
        seating = list(db_manager.execute_query(seating_query, (self.exam_id, classroom_id)))
        
        grid = {}
        for seat in seating:
            key = (seat['row'], seat['col'], seat['seat_position'])
            grid[key] = {
                'student_no': seat['student_no'],
                'name': seat['name']
            }
        
        classroom['seating_grid'] = grid
        classroom['total_students'] = len(seating)
        
        return classroom

