"""
Seating Plan View - Generate and visualize seating arrangements
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                             QComboBox, QMessageBox, QDialog, QGridLayout, QFrame,
                             QScrollArea, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.database.db_manager import db_manager
from src.utils.auth import get_current_user
from src.utils.seating import SeatingPlanGenerator
from src.utils.styles import Styles, configure_table_widget
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
        
        top_bar = QHBoxLayout()
        
        title = QLabel("Seating Plan")
        title.setStyleSheet(Styles.SUBTITLE_LABEL)
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        exam_label = QLabel("Select Exam:")
        exam_label.setStyleSheet(Styles.NORMAL_LABEL)
        top_bar.addWidget(exam_label)
        
        self.exam_combo = QComboBox()
        self.exam_combo.setStyleSheet(Styles.COMBO_BOX)
        self.exam_combo.setMinimumWidth(300)
        self.exam_combo.currentIndexChanged.connect(self.on_exam_selected)
        top_bar.addWidget(self.exam_combo)
        
        layout.addLayout(top_bar)
        
        action_bar = QHBoxLayout()
        action_bar.addStretch()
        
        generate_btn = QPushButton("⚙️ Generate Seating")
        generate_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_btn.clicked.connect(self.generate_seating)
        action_bar.addWidget(generate_btn)
        
        view_btn = QPushButton("👁️ View Layout")
        view_btn.setStyleSheet(Styles.SECONDARY_BUTTON)
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(self.view_layout)
        action_bar.addWidget(view_btn)
        
        export_btn = QPushButton("📄 Export to PDF")
        export_btn.setStyleSheet(Styles.SUCCESS_BUTTON)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self.export_to_pdf)
        action_bar.addWidget(export_btn)
        
        layout.addLayout(action_bar)
        
        self.table = QTableWidget()
        user = get_current_user()
        headers = ["Student No", "Name", "Classroom", "Row", "Seat"]
        if user and user['role'] == 'admin':
            headers.insert(2, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(Styles.TABLE_WIDGET)
        
        # Configure table for proper visibility and scrolling
        configure_table_widget(self.table, min_row_height=38, min_total_height=450)
        
        layout.addWidget(self.table)
        
        self.load_exams()
    
    def load_exams(self):
        """Load scheduled exams into combo box"""
        user = get_current_user()
        if not user:
            return
        
        current_exam_id = self.current_exam_id
        
        try:
            self.exam_combo.currentIndexChanged.disconnect()
        except:
            pass  
        
        if user['role'] == 'admin':
            dept_filter = ""
            params = ()
        else:
            dept_filter = "WHERE e.department_id = ?"
            params = (user['department_id'],)

        query = f"""
            SELECT e.id, e.date, e.start_time, c.code, c.name
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            {dept_filter}
            ORDER BY e.date, e.start_time
        """
        
        exams = db_manager.execute_query(query, params)
        
        self.exam_combo.clear()
        
        for exam in exams:
            display_text = f"{exam['date']} {exam['start_time']} - {exam['code']} {exam['name']}"
            self.exam_combo.addItem(display_text, exam['id'])
        
        self.exam_combo.currentIndexChanged.connect(self.on_exam_selected)
        
        if exams:
            if current_exam_id:
                for i in range(self.exam_combo.count()):
                    if self.exam_combo.itemData(i) == current_exam_id:
                        self.exam_combo.setCurrentIndex(i)
                        self.on_exam_selected(i)
                        return
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
        
        user = get_current_user()
        
        headers = ["Student No", "Name", "Classroom", "Row", "Seat"]
        if user and user['role'] == 'admin':
            headers.insert(2, "Department")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        query = """
            SELECT s.student_no, s.name, cl.name as classroom_name, 
                   es.row, es.col, es.seat_position,
                   d.name as department_name, d.code as department_code
            FROM exam_seating es
            JOIN students s ON es.student_id = s.id
            JOIN classrooms cl ON es.classroom_id = cl.id
            LEFT JOIN departments d ON s.department_id = d.id
            WHERE es.exam_id = ?
            ORDER BY cl.name, es.row, es.col, es.seat_position
        """
        
        seating = db_manager.execute_query(query, (self.current_exam_id,))
        
        self.table.setRowCount(len(seating))
        
        for row, seat in enumerate(seating):
            col_idx = 0
            self.table.setItem(row, col_idx, QTableWidgetItem(seat['student_no']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(seat['name']))
            col_idx += 1
            
            if user and user['role'] == 'admin':
                dept_name = seat['department_name'] or 'N/A'
                dept_code = seat['department_code'] or ''
                self.table.setItem(row, col_idx, QTableWidgetItem(f"{dept_name} ({dept_code})"))
                col_idx += 1
            
            self.table.setItem(row, col_idx, QTableWidgetItem(seat['classroom_name']))
            col_idx += 1
            self.table.setItem(row, col_idx, QTableWidgetItem(f"Row {seat['row'] + 1}"))
            col_idx += 1
            
            seat_label = f"Col {seat['col'] + 1}"
            if seat['seat_position'] > 1:
                seat_label += f" ({seat['seat_position']})"
            self.table.setItem(row, col_idx, QTableWidgetItem(seat_label))
        
        # Ensure all rows are visible with proper height
        self.table.verticalHeader().setDefaultSectionSize(38)
    
    def generate_seating(self):
        """Generate seating plan for selected exam"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
        exam_query = """
            SELECT e.*, c.code as course_code, c.name as course_name
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            WHERE e.id = ?
        """
        exam_result = db_manager.execute_query(exam_query, (self.current_exam_id,))
        
        if not exam_result:
            QMessageBox.critical(self, "Error", "❌ Seçilen sınav bulunamadı!")
            return
        
        exam = exam_result[0]
        
        students_query = """
            SELECT COUNT(*) as count
            FROM students s
            JOIN student_courses sc ON s.id = sc.student_id
            WHERE sc.course_id = ?
        """
        students_count_result = db_manager.execute_query(students_query, (exam['course_id'],))
        students_count = students_count_result[0]['count'] if students_count_result else 0
        
        if students_count == 0:
            QMessageBox.warning(
                self, 
                "Uyarı", 
                f"❌ Bu derse kayıtlı öğrenci bulunamadı!\n\nDers: {exam['course_code']} - {exam['course_name']}"
            )
            return
        
        classrooms_query = """
            SELECT cl.*, 
                   (cl.rows * cl.cols * cl.seats_per_desk) as capacity
            FROM classrooms cl
            JOIN exam_classrooms ec ON cl.id = ec.classroom_id
            WHERE ec.exam_id = ?
        """
        classrooms = list(db_manager.execute_query(classrooms_query, (self.current_exam_id,)))
        
        if not classrooms:
            QMessageBox.warning(
                self,
                "Uyarı",
                "❌ Derslik bulunamadı!\n\nBu sınav için henüz derslik atanmamış."
            )
            return
        
        total_capacity = sum(cl['capacity'] for cl in classrooms)
        
        if total_capacity < students_count:
            classroom_list = "\n".join([f"  • {cl['name']}: {cl['capacity']} kişi" for cl in classrooms])
            QMessageBox.critical(
                self,
                "Kapasite Yetersiz",
                f"❌ Sınıf kapasitesi yetersiz!\n\n"
                f"Toplam Öğrenci: {students_count}\n"
                f"Toplam Kapasite: {total_capacity}\n"
                f"Eksik: {students_count - total_capacity} kişi\n\n"
                f"Atanmış Derslikler:\n{classroom_list}\n\n"
                f"Lütfen daha fazla derslik ekleyin veya daha büyük derslikler seçin."
            )
            return
        
        conflicts_query = """
            SELECT s.student_no, s.name, 
                   GROUP_CONCAT(c.code || ' - ' || c.name, ', ') as courses
            FROM students s
            JOIN student_courses sc ON s.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            JOIN exams e ON c.id = e.course_id
            WHERE e.date = ? AND e.start_time = ? AND e.id != ?
            GROUP BY s.id, s.student_no, s.name
            HAVING COUNT(DISTINCT e.id) > 1
        """
        conflicts = list(db_manager.execute_query(conflicts_query, (exam['date'], exam['start_time'], self.current_exam_id)))
        
        if conflicts:
            conflict_list = "\n".join([f"  • {c['student_no']} - {c['name']}: {c['courses']}" for c in conflicts[:5]])
            warning_msg = f"⚠️ Öğrencilerin dersleri çakışıyor!\n\n"
            warning_msg += f"{len(conflicts)} öğrencinin bu sınavla aynı zamanda başka sınavı var:\n\n"
            warning_msg += conflict_list
            if len(conflicts) > 5:
                warning_msg += f"\n  ... ve {len(conflicts) - 5} öğrenci daha"
            warning_msg += "\n\nDevam etmek istiyor musunuz?"
            
            reply = QMessageBox.question(
                self,
                "Çakışma Uyarısı",
                warning_msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        reply = QMessageBox.question(
            self, 
            "Oturma Planı Oluştur",
            f"📋 Oturma planı oluşturulacak:\n\n"
            f"Ders: {exam['course_code']} - {exam['course_name']}\n"
            f"Tarih: {exam['date']} {exam['start_time']}\n"
            f"Öğrenci Sayısı: {students_count}\n"
            f"Derslik Sayısı: {len(classrooms)}\n"
            f"Toplam Kapasite: {total_capacity}\n\n"
            f"Bu işlem mevcut oturma planını silecektir. Devam edilsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                generator = SeatingPlanGenerator(self.current_exam_id)
                
                if generator.generate_seating():
                    QMessageBox.information(
                        self, 
                        "Başarılı", 
                        f"✅ Oturma planı başarıyla oluşturuldu!\n\n"
                        f"{students_count} öğrenci {len(classrooms)} dersliğe yerleştirildi."
                    )
                    self.load_seating()
                else:
                    QMessageBox.critical(
                        self, 
                        "Hata", 
                        "❌ Oturma planı oluşturulamadı!\n\nLütfen sınav bilgilerini kontrol edin."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Hata",
                    f"❌ Oturma planı oluşturulurken hata oluştu:\n\n{str(e)}"
                )
    
    def view_layout(self):
        """View classroom layout with seating"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
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
        
        for classroom in classrooms:
            dialog = SeatingLayoutDialog(self, self.current_exam_id, classroom['id'], classroom['name'])
            dialog.exec()
    
    def export_to_pdf(self):
        """Export seating plan to PDF"""
        if not self.current_exam_id:
            QMessageBox.warning(self, "No Exam", "Please select an exam first")
            return
        
        exam = db_manager.execute_query(
            "SELECT c.code, e.date, e.start_time FROM exams e JOIN courses c ON e.course_id = c.id WHERE e.id = ?",
            (self.current_exam_id,)
        )
        
        default_filename = "seating_plan.pdf"
        if exam:
            course_code = exam[0]['code'].replace('/', '_').replace('\\', '_')
            exam_date = exam[0]['date'].replace('-', '_')
            exam_time = exam[0]['start_time'].replace(':', '-')
            default_filename = f"seating_plan_{course_code}_{exam_date}_{exam_time}.pdf"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Seating Plan PDF",
            default_filename,
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not file_path:  
            return
        
        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'
        
        try:
            filename = export_seating_plan_pdf(self.current_exam_id, file_path)
            QMessageBox.information(self, "Success", f"Seating plan exported to:\n{filename}")
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
        
        title = QLabel(f"Classroom: {self.classroom_name}")
        title.setStyleSheet(Styles.TITLE_LABEL)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Styles.SCROLL_AREA)
        
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        
        generator = SeatingPlanGenerator(self.exam_id)
        classroom_data = generator.get_seating_by_classroom(self.classroom_id)
        
        if classroom_data:
            grid = classroom_data['seating_grid']
            rows = classroom_data['rows']
            cols = classroom_data['cols']
            seats_per_desk = classroom_data['seats_per_desk']
            
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
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(Styles.PRIMARY_BUTTON)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

