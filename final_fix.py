import os
import re

fixes = {
    'labmanual': 'label',
    'Labmanual': 'Label',
    'dmanualete': 'delete',
    'Dmanualete': 'Delete',
    'dmanualeted': 'deleted',
    'cancmanual': 'cancel',
    'Cancmanual': 'Cancel',
    'whwith': 'while',
    'kaydedwithmedi': 'could not be saved',
    'kaydedwith': 'saved',
    'eklendi': 'added',
    'silindi': 'deleted',
    'Tüm': 'All',
    'Courselik': 'Classroom',
    'courselik': 'classroom',
    'Lütfen': 'Please',
    'için bir': 'to',
    'düzenlemek': 'edit',
    'seçin': 'select',
    'Kod:': 'Code:',
    'Ad:': 'Name:',
    'Doğrulama Errorsı': 'Validation Error',
    'boş olamaz': 'cannot be empty',
    'adı': 'name',
    'Previewsi': 'Preview',
    'heacourse': 'headers',
    'Labmanuals': 'Labels',
    'Fawithd': 'Failed',
    'bilgwithr': 'information',
    'kontrol edin': 'check',
    'bulunamadı': 'not found',
    'oluşturulamadı': 'could not be created',
    'Levmanual': 'Level',
    'seat_labmanual': 'seat_label',
    'icon_labmanual': 'icon_label',
    'title_labmanual': 'title_label',
    'value_labmanual': 'value_label',
    'welcome_labmanual': 'welcome_label',
    'stats_labmanual': 'stats_label',
    'status_labmanual': 'status_label',
    'email_labmanual': 'email_label',
    'password_labmanual': 'password_label',
    'user_labmanual': 'user_label',
    'info_labmanual': 'info_label',
    'get_pdf_labmanual': 'get_pdf_label',
    'get_excel_labmanual': 'get_excel_label',
}

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for wrong, correct in sorted(fixes.items(), key=lambda x: len(x[0]), reverse=True):
            content = content.replace(wrong, correct)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")
        return False

def main():
    fixed = 0
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith('.py'):
                if fix_file(os.path.join(root, file)):
                    fixed += 1
    
    print(f"\n✅ Fixed {fixed} files")

if __name__ == "__main__":
    main()
