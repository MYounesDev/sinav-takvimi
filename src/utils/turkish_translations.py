
PDF_LABELS = {
    "seating_plan_title": "Oturma Düzeni",
    "date": "Tarih",
    "time": "Saat",
    "duration": "Süre",
    "minutes": "dakika",
    "classroom": "Sınıf",
    "student_no": "Öğrenci No",
    "name": "Ad Soyad",
    "row": "Sıra",
    "seat": "Koltuk",
    "empty": "Boş",
    "column": "Kolon",
    
    "exam_schedule_title": "Sınav Programı",
    "course_code": "Ders Kodu",
    "course_name": "Ders Adı",
    "exam_type": "Sınav Türü",
    "students": "Öğrenci Sayısı",
    "classrooms": "Sınıflar",
    "department": "Bölüm",
    
    "final_exam": "Final Sınavı",
    "midterm_exam": "Ara Sınav",
    "resit_exam": "Bütünleme Sınavı",
    
    "generated_on": "Oluşturulma Tarihi",
    "university": "Kocaeli Üniversitesi Sınav Planlama Sistemi",
    "page": "Sayfa",
}

EXCEL_LABELS = {
    "date": "Tarih",
    "time": "Saat",
    "course_code": "Ders Kodu",
    "course_name": "Ders Adı",
    "exam_type": "Sınav Türü",
    "duration": "Süre (dakika)",
    "students": "Öğrenci Sayısı",
    "classrooms": "Sınıflar",
    "department": "Bölüm",
    
    "student_no": "Öğrenci No",
    "name": "Ad Soyad",
    "row": "Sıra",
    "column": "Kolon",
    "seat_position": "Koltuk Pozisyonu",
    "classroom": "Sınıf",
}

EXAM_TYPES = {
    'final': 'Final Sınavı',
    'midterm': 'Ara Sınav',
    'resit': 'Bütünleme Sınavı'
}

DATE_FORMAT = "%d.%m.%Y"

MONTHS_TR = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}

DAYS_TR = {
    "Monday": "Pazartesi",
    "Tuesday": "Salı",
    "Wednesday": "Çarşamba",
    "Thursday": "Perşembe",
    "Friday": "Cuma",
    "Saturday": "Cumartesi",
    "Sunday": "Pazar"
}

MESSAGES = {
    "export_success": "Başarıyla dışa aktarıldı",
    "export_failed": "Dışa aktarma başarısız",
    "no_data": "Dışa aktarılacak veri not found",
    "select_exam": "Please bir sınav selectiz",
    "generating": "Oluşturuluyor...",
}

def get_pdf_label(key: str, default: str = "") -> str:
    return PDF_LABELS.get(key, default)

def get_excel_label(key: str, default: str = "") -> str:
    return EXCEL_LABELS.get(key, default)

def get_exam_type_turkish(exam_type: str) -> str:
    return EXAM_TYPES.get(exam_type, "Final Sınavı")

def get_message(key: str, default: str = "") -> str:
    return MESSAGES.get(key, default)

