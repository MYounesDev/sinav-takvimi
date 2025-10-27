"""
PDF Export Utilities
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from src.database.db_manager import db_manager


def export_seating_plan_pdf(exam_id: int) -> str:
    """
    Export seating plan to PDF
    
    Args:
        exam_id: Exam ID
        
    Returns:
        Generated filename
    """
    # Get exam details
    exam_query = """
        SELECT e.*, c.code as course_code, c.name as course_name
        FROM exams e
        JOIN courses c ON e.course_id = c.id
        WHERE e.id = ?
    """
    exam_result = db_manager.execute_query(exam_query, (exam_id,))
    
    if not exam_result:
        raise ValueError("Exam not found")
    
    exam = exam_result[0]
    
    # Get seating data
    seating_query = """
        SELECT s.student_no, s.name, cl.name as classroom_name,
               es.row, es.col, es.seat_position
        FROM exam_seating es
        JOIN students s ON es.student_id = s.id
        JOIN classrooms cl ON es.classroom_id = cl.id
        WHERE es.exam_id = ?
        ORDER BY cl.name, es.row, es.col, es.seat_position
    """
    seating = list(db_manager.execute_query(seating_query, (exam_id,)))
    
    if not seating:
        raise ValueError("No seating plan found for this exam")
    
    # Generate filename
    filename = f"seating_plan_{exam['course_code']}_{exam['date'].replace('-', '')}.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    title = Paragraph(f"Seating Plan - {exam['course_code']} {exam['course_name']}", title_style)
    elements.append(title)
    
    # Exam info
    info_style = styles['Normal']
    info_text = f"Date: {exam['date']} | Time: {exam['start_time']} | Duration: {exam['duration']} minutes"
    info = Paragraph(info_text, info_style)
    elements.append(info)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Seating table
    table_data = [['Student No', 'Name', 'Classroom', 'Row', 'Seat']]
    
    for seat in seating:
        seat_label = f"Col {seat['col'] + 1}"
        if seat['seat_position'] > 1:
            seat_label += f" ({seat['seat_position']})"
        
        table_data.append([
            seat['student_no'],
            seat['name'],
            seat['classroom_name'],
            f"Row {seat['row'] + 1}",
            seat_label
        ])
    
    table = Table(table_data, colWidths=[1.5*inch, 3*inch, 2*inch, 1*inch, 1.5*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} | Kocaeli University Exam Scheduler"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    return filename


def export_exam_schedule_pdf(department_id: int) -> str:
    """
    Export exam schedule to PDF
    
    Args:
        department_id: Department ID
        
    Returns:
        Generated filename
    """
    # Get department name
    dept_query = "SELECT name, code FROM departments WHERE id = ?"
    dept_result = db_manager.execute_query(dept_query, (department_id,))
    
    if not dept_result:
        raise ValueError("Department not found")
    
    dept = dept_result[0]
    
    # Get exams
    exams_query = """
        SELECT e.date, e.start_time, c.code as course_code, c.name as course_name,
               e.duration, 
               (SELECT COUNT(*) FROM student_courses sc WHERE sc.course_id = e.course_id) as students,
               GROUP_CONCAT(cl.name, ', ') as classrooms
        FROM exams e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN exam_classrooms ec ON e.id = ec.exam_id
        LEFT JOIN classrooms cl ON ec.classroom_id = cl.id
        WHERE e.department_id = ?
        GROUP BY e.id
        ORDER BY e.date, e.start_time
    """
    exams = list(db_manager.execute_query(exams_query, (department_id,)))
    
    if not exams:
        raise ValueError("No exams scheduled")
    
    # Generate filename
    filename = f"exam_schedule_{dept['code']}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1
    )
    
    title = Paragraph(f"Exam Schedule - {dept['name']}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Table
    table_data = [['Date', 'Time', 'Course Code', 'Course Name', 'Duration', 'Students', 'Classrooms']]
    
    for exam in exams:
        table_data.append([
            exam['date'],
            exam['start_time'],
            exam['course_code'],
            exam['course_name'],
            f"{exam['duration']} min",
            str(exam['students']),
            exam['classrooms'] or 'N/A'
        ])
    
    table = Table(table_data, colWidths=[1*inch, 0.8*inch, 1*inch, 2.5*inch, 0.8*inch, 0.8*inch, 2*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} | Kocaeli University Exam Scheduler"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    doc.build(elements)
    
    return filename


