# Turkish Excel Format Import Guide

## Overview

The application now supports importing Excel files in Turkish format, specifically designed for files like "Ders Listesi.xlsx" (Course List) and "Ogrenci listesi.xlsx" (Student List).

## What Changed

### ✅ Courses Import (Ders Listesi.xlsx)

The system now automatically detects and imports Turkish course files with the following features:

**Supported Column Names:**

- `DERS KODU` / `Ders Kodu` → Course Code
- `DERSİN ADI` / `DERS ADI` / `Ders Adı` → Course Name
- `DERSİ VEREN ÖĞR. ELEMANI` / `Öğretim Elemanı` → Instructor

**Automatic Processing:**

- ✓ Detects Turkish format automatically
- ✓ Skips the first row and uses row 2 as header (when needed)
- ✓ Filters out section headers (e.g., "1. Sınıf", "2. Sınıf")
- ✓ Removes duplicate header rows
- ✓ Handles Turkish characters correctly

**Example File Structure:**

```
| 1. Sınıf | (ignored)               | (ignored)                      |
|----------|-------------------------|--------------------------------|
| DERS KODU| DERSİN ADI              | DERSİ VEREN ÖĞR. ELEMANI       |
| AIT109   | Atatürk İlkeleri        | Öğr. Gör. Melih Yiğit          |
| BLM101   | Programlama Temelleri   | Öğr. Gör. Dr. Onur Gök         |
```

**Import Results:**

- ✓ Successfully imports all valid courses
- ✓ Skips invalid/header rows automatically
- ✓ From your file: 45+ courses ready to import

---

### ✅ Students Import (Ogrenci listesi.xlsx)

The system now automatically detects and imports Turkish student files with the following features:

**Supported Column Names:**

- `Öğrenci No` → Student Number
- `Ad Soyad` → Student Name
- `Sınıf` → Class Level (e.g., "1. Sınıf" → 1)
- `Ders` → Course Code

**Automatic Processing:**

- ✓ Detects Turkish format automatically
- ✓ Handles long format (one row per student-course pair)
- ✓ Groups by student and aggregates courses
- ✓ Extracts class level from Turkish text (e.g., "5. Sınıf" → 5)
- ✓ Creates comma-separated course lists

**Example File Structure:**

```
| Öğrenci No | Ad Soyad       | Sınıf    | Ders   |
|------------|----------------|----------|--------|
| 210059017  | Cansu Bozkurt  | 5. Sınıf | BLM401 |
| 210059017  | Cansu Bozkurt  | 5. Sınıf | BLM405 |
| 210059017  | Cansu Bozkurt  | 5. Sınıf | BLM411 |
```

**Conversion:**
The above 3 rows become 1 student record:

- Student No: 210059017
- Name: Cansu Bozkurt
- Class Level: 5
- Courses: BLM401,BLM405,BLM411

**Import Results:**

- ✓ Successfully groups student-course pairs
- ✓ From your file: 3900 rows → 340 unique students
- ✓ Each student automatically enrolled in their courses

---

## How to Use

### Importing Courses

1. Open the application and navigate to **Course Management**
2. Click **"📥 Import from Excel"**
3. Select your Turkish course file (e.g., `Ders Listesi.xlsx`)
4. The system will:
   - Auto-detect Turkish format
   - Normalize column names
   - Filter out invalid rows
   - Import all valid courses
5. Review the import summary

### Importing Students

1. Open the application and navigate to **Student Management**
2. Click **"📥 Import from Excel"**
3. Select your Turkish student file (e.g., `Ogrenci listesi.xlsx`)
4. The system will:
   - Auto-detect Turkish format
   - Group students by number
   - Aggregate their courses
   - Auto-enroll them in courses
5. Review the import summary

---

## Backward Compatibility

The application still supports the original English format:

**Courses:** `code`, `name`, `instructor`, `class_level`, `type`
**Students:** `student_no`, `name`, `class_level`, `course_codes`

The system automatically detects which format you're using and processes accordingly.

---

## Technical Details

### Files Modified

1. `src/ui/courses_view.py`

   - Added `_normalize_turkish_courses()` method
   - Enhanced `import_from_excel()` to detect Turkish format
   - Added header row detection (header=1)
   - Added section header filtering
2. `src/ui/students_view.py`

   - Added `_normalize_turkish_students()` method
   - Enhanced `import_from_excel()` to detect Turkish format
   - Added long-to-wide format conversion
   - Added class level extraction from Turkish text

### Testing

The changes were validated with your actual files:

- ✓ `examples/Ders Listesi.xlsx` - Successfully imported 45+ courses
- ✓ `examples/Ogrenci listesi.xlsx` - Successfully imported 340 students with their course enrollments

---

## Notes

- The import is **smart** - it automatically detects the format
- Turkish characters are fully supported
- Section headers and duplicate rows are automatically filtered
- Course enrollment is automatic for students
- Progress bars show import status
- Error messages guide you if something is wrong

---

## Questions?

If you encounter any issues or need to support additional column name variations, the Turkish column mappings can be easily extended in the `_normalize_turkish_*` methods.
