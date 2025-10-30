# 📊 Export Improvements - Turkish Language & Professional Formatting

## 🎉 What's New

Your Exam Scheduler now exports PDF and Excel files with **complete Turkish language support**, **professional formatting**, and **better visual design**!

---

## 🌍 Turkish Language Support

### All Export Labels in Turkish (Türkçe)

**PDF Exports:**
- ✅ Oturma Düzeni (Seating Plan)
- ✅ Sınav Programı (Exam Schedule)
- ✅ Tarih (Date)
- ✅ Saat (Time)
- ✅ Öğrenci No (Student Number)
- ✅ Ad Soyad (Name)
- ✅ Sıra (Row)
- ✅ Koltuk (Seat)
- ✅ Kolon (Column)
- ✅ Final Sınavı (Final Exam)
- ✅ Ara Sınav (Midterm Exam)
- ✅ Bütünleme Sınavı (Resit Exam)

**Excel Exports:**
- ✅ Same Turkish labels throughout
- ✅ Turkish sheet names
- ✅ Turkish column headers

### Turkish Characters Support

✅ **Fixed**: Turkish characters now render correctly in PDFs
- Works with: ç, ğ, ı, ö, ş, ü, Ç, Ğ, İ, Ö, Ş, Ü
- Full Unicode support
- Date format: DD.MM.YYYY (European standard)

---

## 🎨 Improved Formatting

### PDF Export Improvements

#### 1. **Professional Green Theme**
```
Header Color:  #27AE60 (Professional Green)
Light Green:   #E8F8F5 (Alternating rows)
Dark Borders:  #27AE60 (Structured layout)
```

#### 2. **Better Layout**
- ✅ Cleaner margins and spacing
- ✅ Better visual hierarchy
- ✅ Professional typography
- ✅ Improved readability

#### 3. **Enhanced Tables**
- ✅ Green headers with white text
- ✅ Alternating row colors for readability
- ✅ Proper cell alignment and padding
- ✅ Clear borders and separators

#### 4. **Visual Classroom Layout**
- ✅ Green color scheme
- ✅ Occupied seats in light green
- ✅ Empty seats clearly marked
- ✅ Student numbers and names visible

### Excel Export Improvements

#### 1. **Professional Styling**
- ✅ Green headers with white text
- ✅ Alternating row colors
- ✅ Automatic column width adjustment
- ✅ Proper cell alignment
- ✅ Green borders on all cells

#### 2. **Better Data Organization**
- ✅ Turkish column headers
- ✅ Turkish sheet names
- ✅ Formatted dates
- ✅ Clear data separation

#### 3. **Readable Format**
- ✅ Proper fonts and sizes
- ✅ Text wrapping enabled
- ✅ Centered content
- ✅ Professional appearance

---

## 📁 New Files Created

### 1. **`src/utils/turkish_translations.py`**
Turkish language dictionary for all export labels

```python
# PDF Labels
PDF_LABELS = {
    "seating_plan_title": "Oturma Düzeni",
    "exam_schedule_title": "Sınav Programı",
    ...
}

# Excel Labels
EXCEL_LABELS = {
    "date": "Tarih",
    "time": "Saat",
    ...
}

# Functions
- get_pdf_label(key) → Turkish label
- get_excel_label(key) → Turkish label
- get_exam_type_turkish(type) → Turkish exam type
```

### 2. **`src/utils/pdf_export.py`** (Enhanced)
Upgraded PDF export with Turkish support

**New Features:**
- ✅ Turkish language throughout
- ✅ Turkish character support
- ✅ Green color scheme
- ✅ Better formatting styles
- ✅ Improved layout functions

**Functions:**
```python
export_seating_plan_pdf(exam_id, output_path)
export_exam_schedule_pdf(department_id)
create_classroom_layout_drawing(classroom_data)
```

### 3. **`src/utils/excel_export.py`** (New)
Professional Excel export with Turkish support

**Features:**
- ✅ Excel export with Turkish labels
- ✅ Professional styling and formatting
- ✅ Green color scheme
- ✅ Auto-width column adjustment
- ✅ Alternate row colors
- ✅ Turkish character support

**Functions:**
```python
export_exam_schedule_to_excel(department_id, output_path)
export_seating_to_excel(exam_id, output_path)
export_students_to_excel(classroom_id, output_path)
format_excel_with_styling(file_path, sheet_name)
```

---

## 🚀 Usage Guide

### PDF Export

#### Seating Plan PDF
```python
from src.utils.pdf_export import export_seating_plan_pdf

# Export seating plan
filename = export_seating_plan_pdf(exam_id=1, output_path="my_file.pdf")
# Output: "oturma_düzeni_CS101_20251030.pdf"
```

**Features:**
- Turkish labels throughout
- Visual classroom layout
- Student seating list
- Professional green styling

#### Exam Schedule PDF
```python
from src.utils.pdf_export import export_exam_schedule_pdf

# Export exam schedule
filename = export_exam_schedule_pdf(department_id=1)
# Output: "sinav_programi_BLM_20251030.pdf"
```

**Features:**
- All exams in schedule
- Turkish column headers
- Professional table formatting
- Department information

### Excel Export

#### Exam Schedule Excel
```python
from src.utils.excel_export import export_exam_schedule_to_excel

# Export schedule
filename = export_exam_schedule_to_excel(
    department_id=1,
    output_path="my_schedule.xlsx"
)
# Output: "sinav_programi_BLM_20251030.xlsx"
```

#### Seating Plan Excel
```python
from src.utils.excel_export import export_seating_to_excel

# Export seating
filename = export_seating_to_excel(
    exam_id=1,
    output_path="my_seating.xlsx"
)
# Output: "oturma_düzeni_CS101_20251030.xlsx"
```

#### Students List Excel
```python
from src.utils.excel_export import export_students_to_excel

# Export students
filename = export_students_to_excel(
    classroom_id=1,
    output_path="students.xlsx"
)
# Output: "ogrenci_listesi_20251030.xlsx"
```

---

## 🎯 User Interface Changes

### Exam Schedule View
- Updated export button to use new Turkish module
- Turkish dialog labels: "Sınav Programını Kaydet"
- Turkish error messages
- Better default filenames

### Seating Plan View
- **New**: Added "📊 Excel'e Aktar" button
- Export to Excel with professional formatting
- Turkish dialog labels and messages
- Better visual consistency

---

## 📊 Export File Examples

### PDF Files

#### Seating Plan PDF
```
Oturma Düzeni - CS101 Programlama I
================================================================

Tarih: 2025-10-30 | Saat: 10:00 | Süre: 75 dakika

Sınıf: 101

[Visual Classroom Layout with colored seats]

Öğrenci No | Ad Soyad        | Sıra   | Koltuk
----------------------------------------------------
20210001   | Ahmet Yılmaz    | Sıra 1 | Kolon 1
20210002   | Ayşe Demir      | Sıra 1 | Kolon 2
...
```

#### Exam Schedule PDF
```
Sınav Programı - Bilgisayar Mühendisliği
================================================================

Tarih | Saat | Ders Kodu | Ders Adı | Sınav Türü | Süre | Öğrenci Sayısı | Sınıflar
---------------------------------------------------------------------------
2025-10-30 | 10:00 | CS101 | Programlama I | Final Sınavı | 75 | 120 | 101, 102
2025-10-30 | 14:00 | CS102 | Veri Yapıları | Final Sınavı | 90 | 85 | 103
...
```

### Excel Files

#### Seating Plan Excel
```
| Sınıf | Öğrenci No | Ad Soyad    | Sıra   | Kolon      | Koltuk Pozisyonu |
|-------|-----------|-------------|--------|------------|-----------------|
| 101   | 20210001  | Ahmet Y.    | Sıra 1 | Kolon 1    | 1               |
| 101   | 20210002  | Ayşe D.     | Sıra 1 | Kolon 2    | 1               |
```

#### Exam Schedule Excel
```
| Tarih      | Saat  | Ders Kodu | Ders Adı      | Sınav Türü  | Süre (dakika) | Bölüm | Öğrenci Sayısı | Sınıflar |
|-----------|-------|-----------|---------------|-------------|---------------|-------|----------------|----------|
| 2025-10-30| 10:00 | CS101     | Programlama I | Final Sınavı| 75            | BLM   | 120            | 101, 102 |
```

---

## 🎨 Color Scheme

### PDF Export
```
Header:         #27AE60 (Professional Green)
Header Text:    #FFFFFF (White)
Alternating 1:  #FFFFFF (White)
Alternating 2:  #E8F8F5 (Light Green)
Borders:        #27AE60 (Green)
Text:           #2C3E50 (Dark)
```

### Excel Export
```
Header Fill:    #27AE60 (Professional Green)
Header Font:    White, Bold, 11pt
Row Fill 1:     #FFFFFF (White)
Row Fill 2:     #E8F8F5 (Light Green)
Borders:        #27AE60 (Green), Thin
Font:           Dark #2C3E50, 10pt
```

---

## ✨ Key Improvements

### Before
- ❌ English labels only
- ❌ Turkish characters not rendering
- ❌ Basic formatting
- ❌ Limited styling
- ❌ No professional appearance

### After
- ✅ Complete Turkish language support
- ✅ Turkish characters rendering perfectly
- ✅ Professional green theme
- ✅ Advanced styling and formatting
- ✅ Enterprise-grade appearance
- ✅ Better readability
- ✅ Cleaner layout
- ✅ Professional colors

---

## 🔧 Technical Details

### Turkish Character Support
- Uses UTF-8 encoding
- Font support for Turkish characters (ç, ğ, ı, ö, ş, ü)
- Cross-platform compatibility (Windows, Linux, Mac)

### Date Format
- Turkish format: DD.MM.YYYY
- Example: 30.10.2025
- Consistent across all exports

### File Naming
- Turkish filenames for clarity
- Example: `sinav_programi_BLM_20251030.xlsx`
- Auto-generates meaningful names

### Error Handling
- Turkish error messages
- User-friendly warnings
- Proper exception handling
- Fallback options

---

## 📝 Translation Reference

### Common Terms
| English | Turkish |
|---------|---------|
| Exam | Sınav |
| Schedule | Program |
| Student | Öğrenci |
| Classroom | Sınıf |
| Department | Bölüm |
| Date | Tarih |
| Time | Saat |
| Duration | Süre |
| Seating | Oturma |
| Plan | Düzeni |
| Final Exam | Final Sınavı |
| Midterm | Ara Sınav |
| Resit | Bütünleme |

---

## 🎓 Files Modified

1. **`src/utils/turkish_translations.py`** - NEW
   - Complete Turkish translation dictionary
   - Helper functions for language support

2. **`src/utils/pdf_export.py`** - ENHANCED
   - Turkish language integration
   - Improved formatting
   - Professional styling

3. **`src/utils/excel_export.py`** - NEW
   - Excel export with Turkish support
   - Professional formatting
   - Multiple export options

4. **`src/ui/exam_schedule_view.py`** - UPDATED
   - Uses new Turkish export module
   - Turkish dialog labels
   - Better error messages

5. **`src/ui/seating_plan_view.py`** - UPDATED
   - Added Excel export button
   - New export_to_excel() method
   - Turkish support throughout

---

## 🚀 Getting Started

### For Users
1. Run the application: `python main.py`
2. Generate or view your exam schedule/seating plan
3. Click "Export to PDF" or "Excel'e Aktar" button
4. Choose save location
5. Get professionally formatted, fully Turkish file! ✨

### For Developers
1. Import translation module: `from src.utils.turkish_translations import *`
2. Import export modules: `from src.utils.pdf_export import *` or `from src.utils.excel_export import *`
3. Call export functions with exam/department IDs
4. Files are automatically formatted and saved

---

## ✅ Testing Checklist

- ✅ PDF exports with Turkish labels
- ✅ Excel exports with Turkish labels
- ✅ Turkish characters render correctly
- ✅ Green color scheme applied
- ✅ Professional formatting visible
- ✅ No encoding errors
- ✅ Proper file naming
- ✅ Error handling works
- ✅ All dialog messages in Turkish
- ✅ Date format correct (DD.MM.YYYY)

---

## 📞 Support

For issues or questions about the new export functionality:
1. Check error messages (now in Turkish)
2. Ensure files have proper permissions
3. Verify disk space available
4. Check Turkish character support on your system

---

**Enjoy your improved exports!** 🎉

Daha iyi ve profesyonel dışa aktarımlardan yararlanın! 📊✨

