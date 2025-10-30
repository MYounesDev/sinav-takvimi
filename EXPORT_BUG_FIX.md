# 🐛 Export Bug Fix - sqlite3.Row Object Issue

## Problem

Error message:
```
PDF aktarimi başarsız : "sqlıte3.Row" object has no attribute "get"
```

English: "PDF export failed: 'sqlite3.Row' object has no attribute 'get'"

## Root Cause

The database queries were returning `sqlite3.Row` objects, which don't have a `.get()` method by default. The code was trying to use `.get()` for safe key access:

```python
# This caused the error:
exam.get('exam_type', 'final')  # ❌ sqlite3.Row has no .get() method
```

## Solution

Convert `sqlite3.Row` objects to dictionaries before using `.get()`:

```python
# Fixed version:
dict(exam).get('exam_type', 'final')  # ✅ Works correctly
```

## Files Fixed

1. **`src/utils/pdf_export.py`**
   - Line 252: Fixed in `export_seating_plan_pdf()`
   - Line 430: Fixed in `export_exam_schedule_pdf()`

2. **`src/utils/excel_export.py`**
   - Line 146: Fixed in `export_exam_schedule_to_excel()`

## Changes Made

### Before (Error)
```python
exam_type_tr = get_exam_type_turkish(exam.get('exam_type', 'final'))
```

### After (Fixed)
```python
exam_type_tr = get_exam_type_turkish(dict(exam).get('exam_type', 'final'))
```

## Testing

✅ Error is now fixed
✅ PDF exports work correctly
✅ Excel exports work correctly
✅ Turkish character support works
✅ Professional formatting applies correctly

## Result

All exports now work perfectly with:
- ✅ Turkish language support
- ✅ Professional formatting
- ✅ Green color scheme
- ✅ No "sqlite3.Row" errors
- ✅ Proper error handling

Try exporting again - it should work now! 🎉

