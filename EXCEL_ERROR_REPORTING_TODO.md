# Excel Error Reporting Enhancement - Implementation Guide

## Objective
Improve Excel import error handling to show exactly which row or sheet contains errors when importing students or courses from Excel files.

## Current Behavior
When an error occurs during Excel import:
- Generic error message is shown
- Users don't know which specific row or sheet caused the problem
- Difficult to debug and fix Excel files

## Desired Behavior
When an error occurs during Excel import:
- Show the specific sheet name where error occurred
- Show the specific row number (Excel row, not 0-indexed)
- Show what the error is (missing column, invalid data, etc.)
- Allow import to continue for valid rows (optional)

## Files to Modify

### 1. `src/ui/students_view.py`
**Method:** `import_from_excel()`

**Current Error Handling Areas:**
1. Line ~270-280: Initial Excel file reading
2. Line ~320-340: Turkish format normalization
3. Line ~360-400: Student data processing loop
4. Line ~400-420: Course enrollment processing

**Enhancement Needed:**
```python
# Track errors with details
errors = []
success_count = 0

try:
    # Wrap operations in try-except with row tracking
    for idx, row in df.iterrows():
        excel_row = idx + 2  # +2 for header and 0-indexing
        try:
            # Process row
            success_count += 1
        except Exception as e:
            errors.append(f"Row {excel_row}: {str(e)}")

    # Show summary
    if errors:
        error_msg = f"Import completed with {success_count} successes and {len(errors)} errors:\n\n"
        error_msg += "\n".join(errors[:10])  # Show first 10 errors
        if len(errors) > 10:
            error_msg += f"\n\n... and {len(errors) - 10} more errors"
        QMessageBox.warning(self, "Import Errors", error_msg)
    else:
        QMessageBox.information(self, "Success", f"Successfully imported {success_count} students")
```

### 2. `src/ui/courses_view.py`
**Method:** `import_from_excel()`

**Current Error Handling Areas:**
1. Line ~250-260: Initial Excel file reading
2. Line ~270-290: Sheet reading loop
3. Line ~300-350: Course data processing loop

**Enhancement Needed:**
```python
# Track errors by sheet
errors_by_sheet = {}
success_count = 0

for sheet_name in xls.sheet_names:
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        for idx, row in df.iterrows():
            excel_row = idx + 2  # +2 for header and 0-indexing
            try:
                # Process row
                success_count += 1
            except Exception as e:
                if sheet_name not in errors_by_sheet:
                    errors_by_sheet[sheet_name] = []
                errors_by_sheet[sheet_name].append(f"Row {excel_row}: {str(e)}")
    
    except Exception as e:
        errors_by_sheet[sheet_name] = [f"Sheet error: {str(e)}"]

# Show summary by sheet
if errors_by_sheet:
    error_msg = f"Import completed with {success_count} successes and errors in {len(errors_by_sheet)} sheet(s):\n\n"
    for sheet, errors in errors_by_sheet.items():
        error_msg += f"\n{sheet}:\n"
        error_msg += "\n".join(errors[:5])  # Show first 5 per sheet
        if len(errors) > 5:
            error_msg += f"\n  ... and {len(errors) - 5} more errors"
    QMessageBox.warning(self, "Import Errors", error_msg)
```

## Common Error Types to Handle

### 1. Missing Required Columns
```python
required_columns = ['student_no', 'name']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {', '.join(missing)}")
```

### 2. Invalid Data Types
```python
try:
    class_level = int(row['class_level'])
except ValueError:
    raise ValueError(f"Invalid class level: '{row['class_level']}' must be a number")
```

### 3. Empty Required Fields
```python
if pd.isna(row['student_no']) or str(row['student_no']).strip() == '':
    raise ValueError("Student number cannot be empty")
```

### 4. Duplicate Student Numbers
```python
if student_no in seen_students:
    raise ValueError(f"Duplicate student number: {student_no}")
seen_students.add(student_no)
```

### 5. Invalid Course References
```python
course = db_manager.execute_query("SELECT id FROM courses WHERE code = ?", (course_code,))
if not course:
    raise ValueError(f"Course not found: {course_code}")
```

## Error Message Format Examples

### Good Error Messages
```
Sheet: "Computer Engineering"
  Row 15: Student number cannot be empty
  Row 23: Invalid class level: 'abc' must be a number
  Row 45: Duplicate student number: 12345

Sheet: "Electrical Engineering"
  Row 8: Course not found: EE501
  Row 12: Missing required column: 'name'
```

### Bad Error Messages (Current)
```
Error importing Excel file
An error occurred
Invalid data
```

## Implementation Steps

1. **Phase 1: Add row tracking**
   - Wrap DataFrame iteration with row counter
   - Convert pandas index to Excel row number (+2)
   - Store row number with each error

2. **Phase 2: Add sheet tracking**
   - Track current sheet name
   - Group errors by sheet
   - Include sheet name in error messages

3. **Phase 3: Add validation helpers**
   - Create validation functions for common checks
   - Return clear error messages
   - Validate before database operations

4. **Phase 4: Add error accumulation**
   - Don't stop on first error
   - Collect all errors
   - Show summary at end

5. **Phase 5: Add success reporting**
   - Count successful imports
   - Show both successes and failures
   - Give user clear feedback

## Testing Scenarios

1. **Empty Excel file**: Should report no data found
2. **Missing columns**: Should report which columns are missing
3. **Invalid data types**: Should report row and what's invalid
4. **Duplicate entries**: Should report duplicate value and row
5. **Missing courses**: Should report course code and row
6. **Mixed valid/invalid**: Should import valid rows, report invalid ones
7. **Multiple sheets with errors**: Should group by sheet
8. **Turkish column names**: Should work with normalized names

## Example Enhanced Import Method Structure

```python
def import_from_excel(self):
    """Import students/courses from Excel with detailed error reporting"""
    
    # File selection
    excel_file, _ = QFileDialog.getOpenFileName(...)
    if not excel_file:
        return
    
    # Initialize tracking
    errors = []
    success_count = 0
    
    # Progress dialog
    progress = QProgressDialog(...)
    
    try:
        # Read Excel
        df = pd.read_excel(excel_file)
        
        # Validate columns
        required = ['column1', 'column2']
        missing = [c for c in required if c not in df.columns]
        if missing:
            QMessageBox.critical(self, "Error", f"Missing columns: {', '.join(missing)}")
            return
        
        # Process rows
        for idx, row in df.iterrows():
            excel_row = idx + 2  # Excel row number
            
            try:
                # Validate row
                validate_row(row, excel_row)
                
                # Insert to database
                insert_row(row)
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"Row {excel_row}: {str(e)}")
            
            progress.setValue(idx + 1)
            if progress.wasCanceled():
                break
        
        # Show results
        show_import_results(success_count, errors)
        
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to read Excel file: {str(e)}")
    
    finally:
        progress.close()
        self.load_data()

def validate_row(row, excel_row):
    """Validate a single row, raise ValueError with clear message"""
    if pd.isna(row['required_field']):
        raise ValueError("Required field cannot be empty")
    # More validations...

def show_import_results(success_count, errors):
    """Show import summary with successes and errors"""
    if not errors:
        QMessageBox.information(self, "Success", 
            f"Successfully imported {success_count} records")
    else:
        msg = f"Imported {success_count} records with {len(errors)} errors:\n\n"
        msg += "\n".join(errors[:10])
        if len(errors) > 10:
            msg += f"\n\n... and {len(errors) - 10} more errors"
        QMessageBox.warning(self, "Import Completed with Errors", msg)
```

## Priority Level
**Medium** - Nice to have for better user experience, but not blocking

## Estimated Effort
- 2-3 hours for both files
- Additional 1 hour for testing

## Dependencies
- None (standalone improvement)

## Related Issues
- Users currently struggle to fix Excel files when errors occur
- Support burden could be reduced with better error messages
