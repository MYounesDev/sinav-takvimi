"""
Seating Plan View - Generate and visualize seating arrangements
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QComboBox, QMessageBox, QDialog, QGridLayout, QFrame,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.seating import SeatingPlanGenerator
from src.utils.styles import Styles
from src.utils.pdf_export import export_seating_plan_pdf
from config import COLORS


class SeatingPlanView(QWidget):
    """Seating plan management view"""
    
    def __init__(self):
        super().__init__()
        self.current_exam_id = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Top bar
        top_bar = QHBoxLayout()
        
        title = QLabel("Seating Plan")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        # Exam selector
        exam_label = QLabel("Select Exam:")
        exam_label.setStyleSheet(Styles.NORMAL_LABEL)
        top_bar.addWidget(exam_label)
        
        self.exam_combo = QComboBox()
        self.exam_combo.setStyleSheet(Styles.COMBO_BOX)
        self.exam_combo.setMinimumWidth(300)
        self.exam_combo.currentIndexChanged.connect(self.on_exam_selected)
        top_bar.addWidget(self.exam_combo)
        
        layout.addLayout(top_bar)
        
        # Action buttons
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        # Generate seating button
        generate_btn = QPushButton("⚙️ Generate Seating")
        generate_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_btn.clicked.connect(self.generate_seating)
        action_bar.addWidget(generate_btn)
        
        # View layout button
        view_btn = QPushButton("👁️ View Layout")
        view_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(self.view_layout)
        action_bar.addWidget(view_btn)
        
        # Export to PDF button
        export_btn = QPushButton("📄 Export to PDF")
        export_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self.export_to_pdf)
        action_bar.addWidget(export_btn)
        
        layout.addLayout(action_bar)
        
        # Seating table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Student No", "Name", "Classroom", "Row", "Seat"
        ])
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Load exams
        self.load_exams()
    
    def load_exams(self):
        """Load scheduled exams into combo box"""
        user = get_current_user()
        if not user:
            return
        
        query = """
            SELECT e.id, e.date, e.start_time, c.code, c.name
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            WHERE e.department_id = ?
            ORDER BY e.date, e.start_time
        """
        
        exams = db_manager.execute_query(query, (user['department_id'],))
        
        self.exam_combo.clear()
        
        for exam in exams:
            display_text = f"{exam['date']} {exam['start_time']} - {exam['code']} {exam['name']}"
            self.exam_combo.addItem(display_text, exam['id'])
        
        if exams:
            self.on_exam_selected(0)
    
    def on_exam_selected(self, index):
        """Handle exam selection"""
        if index < 0:
            return
        
        self.current_exam_id = self.exam_combo.itemData(index)
        self.load_seating()
    
    def load_seating(self):
        """Load seating plan for selected exam"""
        if not self.current_exam_id:
            return
        
        query = """
            SELECT s.student_no, s.name, cl.name as classroom_name, 
                   es.row, es.col, es.seat_position
            FROM exam_seating es
            JOIN students s ON es.student_id = s.id
            JOIN classrooms cl ON es.classroom_id = cl.id
            WHERE es.exam_id = ?
            ORDER BY cl.name, es.row, es.col, es.seat_position
        """
        
        seating = db_manager.execute_query(query, (self.current_exam_id,))
        
        self.table.setRowCount(len(seating))
        
        for row, seat in enumerate(seating):
            self.table.setItem(row, 0, QTableWidgetItem(seat['student_no']))
            self.table.setItem(row, 1, QTableWidgetItem(seat['name']))
            self.table.setItem(row, 2, QTableWidgetItem(seat['classroom_name']))
            self.table.setItem(row, 3, QTableWidgetItem(f"Row {seat['row'] + 1}"))
            
            seat_label = f"Col {seat['col'] + 1}"
            if seat['seat_position'] > 1:
                seat_label += f" ({seat['seat_position']})"
            self.table.setItem(row, 4, QTableWidgetItem(seat_label))
    
    def generate_seating(self):
        """Generate seating plan for selected exam"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Generation",
            "This will regenerate the seating plan. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            generator = SeatingPlanGenerator(self.current_exam_id)
            
            if generator.generate_seating():
                QMessageBox.information(self, "Success", "Seating plan generated successfully!")
                self.load_seating()
            else:
                QMessageBox.warning(self, "Error", "Failed to generate seating plan")
    
    def view_layout(self):
        """View classroom layout with seating"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
        # Get classrooms for this exam
        query = """
            SELECT cl.id, cl.name
            FROM classrooms cl
            JOIN exam_classrooms ec ON cl.id = ec.classroom_id
            WHERE ec.exam_id = ?
        """
        classrooms = db_manager.execute_query(query, (self.current_exam_id,))
        
        if not classrooms:
            QMessageBox.warning(self, "No Classrooms", "No classrooms assigned to this exam")
            return
        
        # Show layout for each classroom
        for classroom in classrooms:
            dialog = SeatingLayoutDialog(self, self.current_exam_id, classroom['id'], classroom['name'])
            dialog.exec()
    
    def export_to_pdf(self):
        """Export seating plan to PDF"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
        try:
            filename = export_seating_plan_pdf(self.current_exam_id)
            QMessageBox.information(self, "Success", f"Seating plan exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export PDF:\n{str(e)}")


class SeatingLayoutDialog(QDialog):
    """Dialog showing visual classroom layout"""
    
    def __init__(self, parent=None, exam_id=None, classroom_id=None, classroom_name=None):
        super().__init__(parent)
        self.exam_id = exam_id
        self.classroom_id = classroom_id
        self.classroom_name = classroom_name
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle(f"Seating Layout - {self.classroom_name}")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(f"Classroom: {self.classroom_name}")
        title.setStyleSheet(Styles.TITLE_LABEL)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Scroll area for grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Styles.SCROLL_AREA)
        
        # Grid container
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        
        # Load seating data
        generator = SeatingPlanGenerator(self.exam_id)
        classroom_data = generator.get_seating_by_classroom(self.classroom_id)
        
        if classroom_data:
            grid = classroom_data['seating_grid']
            rows = classroom_data['rows']
            cols = classroom_data['cols']
            seats_per_desk = classroom_data['seats_per_desk']
            
            # Create grid
            for row in range(rows):
                for col in range(cols):
                    desk_frame = QFrame()
                    desk_frame.setStyleSheet(f"""
                        QFrame {{
                            background-color: {COLORS['white']};
                            border: 2px solid {COLORS['border']};
                            border-radius: 8px;
                            padding: 10px;
                        }}
                    """)
                    
                    desk_layout = QVBoxLayout(desk_frame)
                    desk_layout.setSpacing(5)
                    
                    for seat_pos in range(1, seats_per_desk + 1):
                        key = (row, col, seat_pos)
                        if key in grid:
                            student = grid[key]
                            seat_label = QLabel(f"{student['student_no']}\n{student['name']}")
                            seat_label.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {COLORS['primary']};
                                    color: {COLORS['white']};
                                    padding: 8px;
                                    border-radius: 4px;
                                    font-size: 11px;
                                }}
                            """)
                        else:
                            seat_label = QLabel("Empty")
                            seat_label.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {COLORS['light']};
                                    color: {COLORS['text_light']};
                                    padding: 8px;
                                    border-radius: 4px;
                                    font-size: 11px;
                                }}
                            """)
                        
                        seat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        desk_layout.addWidget(seat_label)
                    
                    grid_layout.addWidget(desk_frame, row, col)
        
        scroll.setWidget(grid_widget)
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


