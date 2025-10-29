# Veritabanı Güncellemeleri - display_id ve CASCADE DELETE

## 📋 Özet

Bu dokümantasyon, Sınav Takvimi projesindeki veritabanı yapısının güncellenmesini detaylandırır. İki ana iyileştirme yapıldı:

1. **display_id Sistemi**: Kullanıcıya gösterilen ID'lerin yeniden kullanılabilmesi
2. **CASCADE DELETE**: Bir kayıt silindiğinde ilişkili tüm kayıtların otomatik silinmesi

## ✨ Yapılan Değişiklikler

### 1. display_id Sistemi

#### Sorun
- SQLite'da silinen ID'ler tekrar kullanılamıyordu
- Kullanıcılar için ID boşlukları oluşuyordu
- ID'ler sürekli artıyordu

#### Çözüm
Her tabloya iki ID alanı eklendi:
- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT): Dahili, değişmez, ilişkiler için
- **`display_id`** (INTEGER): Kullanıcıya gösterilen, yeniden kullanılabilen ID

#### Kapsam
Display_id eklenen tablolar:
- ✅ `departments` - Global benzersiz
- ✅ `users` - Global benzersiz
- ✅ `classrooms` - Bölüm başına benzersiz
- ✅ `courses` - Bölüm başına benzersiz
- ✅ `students` - Bölüm başına benzersiz
- ✅ `exams` - Bölüm başına benzersiz

#### Nasıl Çalışır?

**1. Silme İşlemi:**
```sql
-- Kullanıcı bir department siler
DELETE FROM departments WHERE id = 5;

-- Trigger otomatik çalışır:
CREATE TRIGGER before_delete_department
BEFORE DELETE ON departments
BEGIN
    INSERT OR IGNORE INTO deleted_ids (table_name, display_id)
    VALUES ('departments', OLD.display_id);
END;
```

**2. Yeni Kayıt Oluşturma:**
```python
# get_next_display_id() metodu:
# 1. Önce deleted_ids tablosunu kontrol et
# 2. Silinen bir ID varsa onu kullan ve deleted_ids'den sil
# 3. Yoksa MAX(display_id) + 1 kullan

display_id = db_manager.get_next_display_id('departments')
```

**3. deleted_ids Tablosu:**
```sql
CREATE TABLE deleted_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    display_id INTEGER NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(table_name, display_id)
);
```

### 2. CASCADE DELETE Sistemi

#### Sorun
- Bir bölüm silindiğinde, bağlı kayıtları manuel silmek gerekiyordu
- UI'da gereksiz kontroller yapılıyordu
- Hata riski yüksekti

#### Çözüm
Tüm foreign key ilişkilerine `ON DELETE CASCADE` eklendi.

#### Cascade İlişkileri

```
departments (Ana Tablo)
    ├─> users (CASCADE)
    ├─> classrooms (CASCADE)
    ├─> courses (CASCADE)
    │       └─> student_courses (CASCADE)
    │       └─> exams (CASCADE)
    │               ├─> exam_classrooms (CASCADE)
    │               └─> exam_seating (CASCADE)
    └─> students (CASCADE)
            └─> student_courses (CASCADE)
            └─> exam_seating (CASCADE)
```

**Örnek:**
```sql
-- Bir department silindiğinde:
DELETE FROM departments WHERE id = 2;

-- Otomatik olarak silinir:
-- ✓ O bölümdeki tüm users
-- ✓ O bölümdeki tüm classrooms
-- ✓ O bölümdeki tüm courses
-- ✓ O bölümdeki tüm students
-- ✓ İlgili tüm student_courses
-- ✓ İlgili tüm exams
-- ✓ İlgili tüm exam_classrooms
-- ✓ İlgili tüm exam_seating
```

## 🔧 Teknik Detaylar

### Veritabanı Şeması Değişiklikleri

**Örnek: departments tablosu**
```sql
-- ÖNCE:
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,  -- AUTOINCREMENT yok
    name TEXT UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SONRA:
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- AUTOINCREMENT eklendi
    display_id INTEGER UNIQUE NOT NULL,     -- YENİ: Kullanıcıya gösterilen ID
    name TEXT UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Örnek: students tablosu (bölüm-scoped)**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_id INTEGER NOT NULL,  -- Bölüm başına benzersiz
    department_id INTEGER NOT NULL,
    student_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    class_level INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    UNIQUE(department_id, display_id)  -- Bölüm + display_id benzersiz
);
```

### UI Değişiklikleri

**Örnek: departments_view.py**

```python
# ÖNCE:
def load_departments(self):
    query = "SELECT id, name, code FROM departments"
    for row, dept in enumerate(departments):
        self.table.setItem(row, 0, QTableWidgetItem(str(dept['id'])))

# SONRA:
def load_departments(self):
    query = "SELECT id, display_id, name, code FROM departments"
    for row, dept in enumerate(departments):
        # Kullanıcıya display_id göster
        self.table.setItem(row, 0, QTableWidgetItem(str(dept['display_id'])))
        # Dahili id'yi gizli data olarak sakla
        self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, dept['id'])
```

**Edit/Delete işlemlerinde:**
```python
# Dahili ID'yi gizli datadan al
internal_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
# Query'lerde dahili ID kullan
query = "DELETE FROM departments WHERE id = ?"
db_manager.execute_update(query, (internal_id,))
```

### db_manager.py Yeni Metot

```python
def get_next_display_id(self, table_name: str, department_id: Optional[int] = None) -> int:
    """
    Get the next available display_id for a table.
    Reuses deleted IDs if available, otherwise returns max + 1.
    For department-scoped tables, display_id is unique per department.
    
    Args:
        table_name: Name of the table
        department_id: Optional department ID for department-scoped tables
        
    Returns:
        Next available display_id
    """
    # 1. Check for recycled IDs first
    # 2. If found, remove from deleted_ids and return
    # 3. Otherwise, return MAX(display_id) + 1
```

## 📝 Migration Adımları

### 1. Mevcut Veritabanını Backup Al
```bash
python migrate_to_display_id.py
# Otomatik backup: exam_scheduler_backup_YYYYMMDD_HHMMSS.db
```

### 2. display_id Kolonlarını Ekle
```bash
# migrate_to_display_id.py
# - Tüm tablolara display_id ekler
# - Mevcut kayıtlara display_id = id atar
# - deleted_ids tablosunu oluşturur
# - Trigger'ları oluşturur
```

### 3. CASCADE DELETE'i Düzelt
```bash
python fix_cascade_delete.py
# - Tüm tabloları yeniden oluşturur
# - ON DELETE CASCADE ekler
# - Verileri geri yükler
```

### 4. db_manager.py'yi Güncelle
```bash
# Eski db_manager.py → db_manager_old.py
# Yeni db_manager_new.py → db_manager.py
```

### 5. UI Dosyalarını Güncelle
- ✅ departments_view.py
- ✅ users_view.py
- ⏳ classrooms_view.py
- ⏳ courses_view.py
- ⏳ students_view.py
- ⏳ exam_schedule_view.py

## 🧪 Test Sonuçları

```bash
python test_comprehensive.py
```

**Test 1: display_id Sistemi**
- ✅ Yeni kayıt oluşturma
- ✅ Kayıt silme ve deleted_ids'e ekleme
- ✅ Silinen ID'yi yeniden kullanma

**Test 2: CASCADE DELETE**
- ✅ Department silindiğinde tüm ilişkili kayıtlar siliniyor
- ✅ Foreign key constraint'ler çalışıyor

**Test 3: Department-Scoped display_id**
- ✅ Farklı bölümlerde aynı display_id kullanılabiliyor

## 🎯 Kullanım Örnekleri

### Örnek 1: Department Silme
```python
# Kullanıcı arayüzünde:
# - "Bilgisayar Mühendisliği" bölümünü sil

# Otomatik olarak silinir:
# - 150 öğrenci
# - 25 ders
# - 5 sınıf
# - 2 koordinatör
# - 40 sınav
# - İlgili tüm oturma planları
```

### Örnek 2: Yeni Department Ekleme
```python
# Kullanıcı yeni bölüm ekler: "Makine Mühendisliği"
# display_id otomatik atanır:
# - Eğer daha önce silinmiş bir ID varsa (örn: 3) → display_id = 3
# - Yoksa → display_id = max(display_id) + 1
```

### Örnek 3: Student Ekleme (Bölüm-Scoped)
```python
# Bilgisayar Müh. bölümüne öğrenci ekle → display_id = 1
# Yazılım Müh. bölümüne öğrenci ekle → display_id = 1
# Her iki öğrenci de "1" ID'sine sahip (kendi bölümlerinde)
```

## ⚠️ Önemli Notlar

1. **Backup**: Her migration öncesi otomatik backup alınır
2. **Foreign Keys**: SQLite'da foreign key'ler varsayılan olarak kapalı, açılması gerekir:
   ```python
   conn.execute("PRAGMA foreign_keys = ON")
   ```
3. **Display ID Scope**:
   - `departments`, `users`: Global benzersiz
   - `classrooms`, `courses`, `students`, `exams`: Bölüm başına benzersiz
4. **Silme Uyarıları**: UI'da CASCADE DELETE uyarısı gösterilir

## 🔍 Debugging

**Foreign key'leri kontrol et:**
```bash
python check_schema.py
```

**Manuel test:**
```sql
-- Foreign key'leri aktif et
PRAGMA foreign_keys = ON;

-- Test CASCADE DELETE
DELETE FROM departments WHERE id = 1;

-- İlişkili kayıtları kontrol et
SELECT COUNT(*) FROM students WHERE department_id = 1;  -- 0 olmalı
```

## 📚 Dosya Yapısı

```
sinav-takvimi/
├── src/
│   └── database/
│       ├── db_manager.py          # YENİ: display_id destekli
│       └── db_manager_old.py      # ESKİ: yedek
├── migrate_to_display_id.py       # Migration scripti
├── fix_cascade_delete.py          # CASCADE düzeltme scripti
├── test_comprehensive.py          # Kapsamlı test suite
├── check_schema.py                # Şema kontrol aracı
└── database/
    ├── exam_scheduler.db          # Ana veritabanı
    └── *.db                       # Backup dosyaları
```

## ✅ Tamamlanan İşler

- [x] display_id sistemi tasarlandı ve uygulandı
- [x] deleted_ids tablosu ve trigger'lar oluşturuldu
- [x] CASCADE DELETE tüm tablolara eklendi
- [x] Migration scriptleri hazırlandı
- [x] db_manager.py güncellendi
- [x] departments_view.py güncellendi
- [x] users_view.py güncellendi
- [x] Test suite oluşturuldu
- [x] Dokümantasyon hazırlandı

## 🚀 Devam Eden İşler

- [ ] classrooms_view.py'yi güncelle
- [ ] courses_view.py'yi güncelle
- [ ] students_view.py'yi güncelle
- [ ] exam_schedule_view.py'yi güncelle
- [ ] seating_plan_view.py'yi kontrol et (display_id gerekli mi?)

## 💡 Best Practices

1. **Her zaman dahili `id` kullan**: İlişkilerde ve query'lerde
2. **Kullanıcıya `display_id` göster**: UI'da sadece display_id
3. **CASCADE DELETE kullan**: Manuel silme işlemleri yapma
4. **Foreign key'leri aktif et**: Her connection'da `PRAGMA foreign_keys = ON`
5. **Backup al**: Migration öncesi mutlaka

## 🆘 Sorun Giderme

**Sorun: CASCADE DELETE çalışmıyor**
```bash
python check_schema.py  # Foreign key'leri kontrol et
python fix_cascade_delete.py  # Düzelt
```

**Sorun: display_id duplicate hatası**
```python
# get_next_display_id() kullandığınızdan emin olun
display_id = db_manager.get_next_display_id('students', department_id)
```

**Sorun: Migration sonrası veri kaybı**
```bash
# Backup'tan geri yükle
cp database/exam_scheduler_backup_*.db database/exam_scheduler.db
```

---

**Hazırlayan**: GitHub Copilot  
**Tarih**: 29 Ekim 2025  
**Versiyon**: 2.0
