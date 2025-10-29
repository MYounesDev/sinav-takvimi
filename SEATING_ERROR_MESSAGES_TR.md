# Oturma Planı Hata Mesajları - Kullanım Kılavuzu

## Hata Mesajları ve Çözümleri

### 1. ❌ "Seçilen sınav bulunamadı!"

**Ne zaman görülür:**
- Silinen veya var olmayan bir sınav için oturma planı oluşturulmaya çalışıldığında

**Çözüm:**
1. Exam Schedule sayfasından geçerli bir sınav seçin
2. Sınavın veritabanında olduğundan emin olun

---

### 2. ❌ "Bu derse kayıtlı öğrenci bulunamadı!"

**Ne zaman görülür:**
- Seçilen derste hiç öğrenci kayıtlı değilse

**Mesaj içeriği:**
```
❌ Bu derse kayıtlı öğrenci bulunamadı!

Ders: MAT101 - Matematik I
```

**Çözüm:**
1. Student Management sayfasına gidin
2. Excel'den öğrenci import edin veya manuel ekleyin
3. Öğrencilerin bu derse kayıtlı olduğundan emin olun

---

### 3. ❌ "Derslik bulunamadı!"

**Ne zaman görülür:**
- Sınav için hiç derslik atanmamışsa

**Mesaj içeriği:**
```
❌ Derslik bulunamadı!

Bu sınav için henüz derslik atanmamış.
```

**Çözüm:**
1. Exam Schedule sayfasına gidin
2. Sınavı seçin
3. "Assign Classrooms" butonuna tıklayın
4. Uygun derslikleri seçip kaydedin

---

### 4. ❌ "Sınıf kapasitesi yetersiz!"

**Ne zaman görülür:**
- Atanan dersliklerin toplam kapasitesi öğrenci sayısından az ise

**Mesaj içeriği:**
```
❌ Sınıf kapasitesi yetersiz!

Toplam Öğrenci: 120
Toplam Kapasite: 100
Eksik: 20 kişi

Atanmış Derslikler:
  • D201: 40 kişi
  • D202: 35 kişi
  • D203: 25 kişi

Lütfen daha fazla derslik ekleyin veya daha büyük derslikler seçin.
```

**Çözüm - Seçenek 1 (Daha fazla derslik ekle):**
1. Exam Schedule sayfasında sınavı seçin
2. "Assign Classrooms" butonuna tıklayın
3. Daha fazla derslik ekleyin
4. Toplam kapasite öğrenci sayısını geçene kadar

**Çözüm - Seçenek 2 (Daha büyük derslik seç):**
1. Mevcut küçük derslikleri kaldırın
2. Daha büyük kapasiteli derslikler seçin
3. Örnek: 3 küçük derslik yerine 2 büyük derslik

**Kapasite hesaplama:**
```
Derslik Kapasitesi = Satır × Sütun × Masa Başına Kişi

Örnek:
- 5 satır × 8 sütun × 2 kişi = 80 kişi
- 10 satır × 6 sütun × 1 kişi = 60 kişi
```

---

### 5. ⚠️ "Öğrencilerin dersleri çakışıyor!"

**Ne zaman görülür:**
- Bazı öğrencilerin aynı tarih ve saatte birden fazla sınavı varsa

**Mesaj içeriği:**
```
⚠️ Öğrencilerin dersleri çakışıyor!

5 öğrencinin bu sınavla aynı zamanda başka sınavı var:

  • 20210001 - Ahmet Yılmaz: MAT101 - Matematik I, FIZ101 - Fizik I
  • 20210002 - Ayşe Demir: MAT101 - Matematik I, KIM101 - Kimya I
  • 20210003 - Mehmet Kaya: MAT101 - Matematik I, ING101 - İngilizce I
  ... ve 2 öğrenci daha

Devam etmek istiyor musunuz?
```

**Bu bir uyarıdır, HATA DEĞİL:**
- "Yes" diyerek devam edebilirsiniz
- Program oturma planını oluşturur
- Ancak öğrenciler iki sınava birden giremez

**Çözüm - Seçenek 1 (Sınav saatini değiştir):**
1. Exam Schedule sayfasına gidin
2. Çakışan sınavlardan birinin tarih/saatini değiştirin
3. Tekrar oturma planı oluşturun

**Çözüm - Seçenek 2 (Devam et):**
1. "Yes" butonuna tıklayın
2. Çakışan öğrencileri not alın
3. Manuel olarak alternatif sınav ayarlayın

**Çözüm - Seçenek 3 (İptal et):**
1. "No" butonuna tıklayın
2. Sınav programını düzenleyin
3. Çakışmaları giderin
4. Tekrar deneyin

---

### 6. ✅ "Oturma planı başarıyla oluşturuldu!"

**Ne zaman görülür:**
- Tüm kontroller geçildi ve oturma planı başarıyla oluşturulduğunda

**Mesaj içeriği:**
```
✅ Oturma planı başarıyla oluşturuldu!

120 öğrenci 3 dersliğe yerleştirildi.
```

**Sonraki adımlar:**
1. Seating Plan View'da oturma düzenini görüntüleyin
2. "View Layout" ile görsel düzeni inceleyin
3. "Export to PDF" ile PDF olarak kaydedin
4. PDF'i yazdırın ve dersliklere asın

---

### 7. ❌ "Oturma planı oluşturulamadı!"

**Ne zaman görülür:**
- Beklenmeyen bir hata oluştuğunda

**Mesaj içeriği:**
```
❌ Oturma planı oluşturulamadı!

Lütfen sınav bilgilerini kontrol edin.
```

**Çözüm:**
1. Sınav bilgilerini kontrol edin
2. Ders, öğrenci ve derslik verilerinin doğru olduğundan emin olun
3. Veritabanı bağlantısını kontrol edin
4. Uygulamayı yeniden başlatın
5. Sorun devam ederse sistem yöneticisine başvurun

---

## Onay Diyaloğu

### "Oturma Planı Oluştur" Onayı

**Ne zaman görülür:**
- Tüm kontroller geçildikten sonra, oluşturmadan önce

**Mesaj içeriği:**
```
📋 Oturma planı oluşturulacak:

Ders: MAT101 - Matematik I
Tarih: 2024-01-15 09:00
Öğrenci Sayısı: 120
Derslik Sayısı: 3
Toplam Kapasite: 150

Bu işlem mevcut oturma planını silecektir. Devam edilsin mi?
```

**Butonlar:**
- **Yes**: Oturma planını oluştur (mevcut plan silinir)
- **No**: İptal et (hiçbir değişiklik yapılmaz)

**Önemli not:**
- Eğer bu sınav için daha önce oturma planı oluşturulduysa, eski plan silinir
- Yeni plan rastgele yerleşim ile oluşturulur
- Geri alma seçeneği yoktur

---

## Hata Önleme İpuçları

### 1. Sınav Oluşturmadan Önce
- [ ] Dersin öğrencileri import edilmiş mi?
- [ ] Yeterli sayıda derslik var mı?
- [ ] Derslik kapasiteleri yeterli mi?
- [ ] Sınav tarihi ve saati doğru mu?

### 2. Derslik Ataması Yaparken
- [ ] Toplam kapasite = Öğrenci sayısı + %10 fazla (rahat alan için)
- [ ] Büyük derslikler tercih edin (yönetimi kolay)
- [ ] Yakın derslikleri seçin (gözetim için)

### 3. Kapasite Hesaplama
```
Öğrenci Sayısı: 120
Önerilen Kapasite: 120 + 12 (yedek) = 132

Seçenek 1: 2 büyük derslik
  • D201: 80 kişi
  • D202: 60 kişi
  • TOPLAM: 140 kişi ✅

Seçenek 2: 3 orta derslik
  • D301: 50 kişi
  • D302: 45 kişi
  • D303: 40 kişi
  • TOPLAM: 135 kişi ✅
```

### 4. Çakışma Kontrolü
- Exam Schedule'da sınavları tarih/saat sırasına göre düzenleyin
- Aynı tarih/saate çok fazla sınav koymayın
- Çakışma uyarısı alırsanız zamanları yeniden düzenleyin

---

## Sık Sorulan Sorular

**S: Kapasite yeterli ama yine de hata alıyorum?**
C: Derslik atamalarını kontrol edin. "Assign Classrooms" butonuna tıklayıp dersliklerin gerçekten atandığından emin olun.

**S: Çakışma uyarısı alıyorum ama devam edebilir miyim?**
C: Evet, "Yes" diyerek devam edebilirsiniz. Ancak çakışan öğrenciler için alternatif sınav düzenlemeniz gerekir.

**S: Oturma planını nasıl silebilirim?**
C: Yeni bir plan oluşturduğunuzda eski plan otomatik olarak silinir. Manuel silme seçeneği yoktur.

**S: PDF export çalışmıyor?**
C: Önce oturma planı oluşturulmuş olmalıdır. Seating Plan View'da öğrencilerin yerleşimini görebiliyor musunuz?

**S: Öğrenciler rastgele mi yerleştiriliyor?**
C: Evet, öğrenciler rastgele sıralanır ve dersliklere yerleştirilir. Bu kopya çekmeyi zorlaştırır.

**S: Belirli öğrencileri yan yana oturtabilir miyim?**
C: Şu anda hayır. Sistem tamamen rastgele yerleşim yapar.

**S: Aynı sınıftan öğrencileri ayırabilir miyim?**
C: Rastgele yerleşim bunu otomatik olarak yapar, ancak garanti edilmez.

---

## Hata Kodu Referansı

| Kod | Mesaj | Çözüm |
|-----|-------|-------|
| E001 | Sınav bulunamadı | Geçerli sınav seçin |
| E002 | Öğrenci bulunamadı | Öğrenci import edin |
| E003 | Derslik bulunamadı | Derslik atayın |
| E004 | Kapasite yetersiz | Daha fazla/büyük derslik |
| W001 | Dersler çakışıyor | Zamanları düzenleyin veya devam edin |
| S001 | Başarıyla oluşturuldu | PDF export edebilirsiniz |
| E999 | Beklenmeyen hata | Destek alın |

---

**Son Güncelleme:** 2024
**Versiyon:** 1.0
