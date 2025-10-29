"""
PDF Export Utilities
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from datetime import datetime
from src.database.db_manager import db_manager
from src.utils.seating import SeatingPlanGenerator


def create_classroom_layout_drawing(classroom_data: dict, width: float = 7*inch, height: float = 5*inch) -> Drawing:
    """
    Create a visual drawing of classroom seating layout
    
    Args:
        classroom_data: Dictionary with classroom info and seating grid
        width: Drawing width
        height: Drawing height
        
    Returns:
        Drawing object
    """
    d = Drawing(width, height)
    
    if not classroom_data:
        return d
    
    grid = classroom_data.get('seating_grid', {})
    rows = classroom_data.get('rows', 0)
    cols = classroom_data.get('cols', 0)
    seats_per_desk = classroom_data.get('seats_per_desk', 1)
    
    if rows == 0 or cols == 0:
        return d
    
    # Calculate cell dimensions
    margin = 20
    available_width = width - 2 * margin
    available_height = height - 2 * margin
    
    cell_width = available_width / cols
    cell_height = available_height / rows
    
    # Draw grid
    for row in range(rows):
        for col in range(cols):
            x = margin + col * cell_width
            y = height - margin - (row + 1) * cell_height
            
            # Draw desk border
            desk_rect = Rect(x + 2, y + 2, cell_width - 4, cell_height - 4)
            desk_rect.strokeColor = colors.HexColor('#2C3E50')
            desk_rect.strokeWidth = 1
            desk_rect.fillColor = colors.HexColor('#ECF0F1')
            d.add(desk_rect)
            
            # Draw seats
            seat_height = (cell_height - 4) / seats_per_desk
            for seat_pos in range(1, seats_per_desk + 1):
                key = (row, col, seat_pos)
                seat_y = y + 2 + (seat_pos - 1) * seat_height
                
                if key in grid:
                    student = grid[key]
                    # Occupied seat
                    seat_rect = Rect(x + 4, seat_y + 2, cell_width - 8, seat_height - 4)
                    seat_rect.strokeColor = colors.HexColor('#3498DB')
                    seat_rect.strokeWidth = 1.5
                    seat_rect.fillColor = colors.HexColor('#3498DB')
                    d.add(seat_rect)
                    
                    # Student info
                    student_text = String(
                        x + cell_width / 2,
                        seat_y + seat_height / 2 + 8,
                        student['student_no'],
                        fontSize=8,
                        fillColor=colors.white,
                        textAnchor='middle'
                    )
                    d.add(student_text)
                    
                    name_text = String(
                        x + cell_width / 2,
                        seat_y + seat_height / 2 - 4,
                        student['name'][:15] + '...' if len(student['name']) > 15 else student['name'],
                        fontSize=6,
                        fillColor=colors.white,
                        textAnchor='middle'
                    )
                    d.add(name_text)
                else:
                    # Empty seat
                    seat_rect = Rect(x + 4, seat_y + 2, cell_width - 8, seat_height - 4)
                    seat_rect.strokeColor = colors.HexColor('#BDC3C7')
                    seat_rect.strokeWidth = 1
                    seat_rect.fillColor = colors.HexColor('#F8F9FA')
                    d.add(seat_rect)
                    
                    empty_text = String(
                        x + cell_width / 2,
                        seat_y + seat_height / 2,
                        'Empty',
                        fontSize=7,
                        fillColor=colors.HexColor('#95A5A6'),
                        textAnchor='middle'
                    )
                    d.add(empty_text)
    
    return d


def export_seating_plan_pdf(exam_id: int, output_path: str = None) -> str:
    """
    Export seating plan to PDF with visual classroom layouts
    
    Args:
        exam_id: Exam ID
        output_path: Optional output file path. If None, generates default filename
        
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
    
    # Get classrooms for this exam
    classrooms_query = """
        SELECT cl.id, cl.name
        FROM classrooms cl
        JOIN exam_classrooms ec ON cl.id = ec.classroom_id
        WHERE ec.exam_id = ?
        ORDER BY cl.name
    """
    classrooms = list(db_manager.execute_query(classrooms_query, (exam_id,)))
    
    if not classrooms:
        raise ValueError("No classrooms assigned to this exam")
    
    # Generate filename if not provided
    if output_path is None:
        filename = f"seating_plan_{exam['course_code']}_{exam['date'].replace('-', '')}.pdf"
    else:
        filename = output_path
    
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
        spaceAfter=20,
        alignment=1  # Center
    )
    
    title = Paragraph(f"Seating Plan - {exam['course_code']} {exam['course_name']}", title_style)
    elements.append(title)
    
    # Exam info
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=1
    )
    info_text = f"Date: {exam['date']} | Time: {exam['start_time']} | Duration: {exam['duration']} minutes"
    info = Paragraph(info_text, info_style)
    elements.append(info)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Create seating plan generator
    generator = SeatingPlanGenerator(exam_id)
    
    # For each classroom, add layout visualization
    for idx, classroom in enumerate(classrooms):
        # Classroom title
        classroom_title_style = ParagraphStyle(
            'ClassroomTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=15,
            alignment=1
        )
        
        classroom_title = Paragraph(f"Classroom: {classroom['name']}", classroom_title_style)
        elements.append(classroom_title)
        
        # Get classroom layout
        classroom_data = generator.get_seating_by_classroom(classroom['id'])
        
        if classroom_data:
            # Add visual layout
            layout_drawing = create_classroom_layout_drawing(classroom_data)
            elements.append(layout_drawing)
            elements.append(Spacer(1, 0.2 * inch))
            
            # Add student list table for this classroom
            seating_query = """
                SELECT s.student_no, s.name, es.row, es.col, es.seat_position
                FROM exam_seating es
                JOIN students s ON es.student_id = s.id
                WHERE es.exam_id = ? AND es.classroom_id = ?
                ORDER BY es.row, es.col, es.seat_position
            """
            seating = list(db_manager.execute_query(seating_query, (exam_id, classroom['id'])))
            
            if seating:
                table_data = [['Student No', 'Name', 'Row', 'Seat']]
                
                for seat in seating:
                    seat_label = f"Col {seat['col'] + 1}"
                    if seat['seat_position'] > 1:
                        seat_label += f" ({seat['seat_position']})"
                    
                    table_data.append([
                        seat['student_no'],
                        seat['name'],
                        f"Row {seat['row'] + 1}",
                        seat_label
                    ])
                
                table = Table(table_data, colWidths=[1.5*inch, 3.5*inch, 1*inch, 1.5*inch])
                
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                
                elements.append(table)
        
        # Add page break between classrooms (except for the last one)
        if idx < len(classrooms) - 1:
            elements.append(PageBreak())
    
    # Footer
    elements.append(Spacer(1, 0.3 * inch))
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


