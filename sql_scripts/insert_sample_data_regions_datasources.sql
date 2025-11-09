-- Sorumlu: Devrim Polat
-- Bu script, 'DataSources' ve 'Regions' tablolarına
-- 'db_utils.py' dosyasının test edilebilmesi için örnek veriler ekler.
-- MySQL'in "INSERT IGNORE" komutu, kayıt zaten varsa hata vermeden atlar.

-- 1. Adım: DataSources tablosuna ana veri kaynağını ekle
-- (Bu, Regions tablosunun FK'sı (source_id) için gereklidir)
INSERT INTO DataSources (id, source_name, source_url, description)
VALUES (
    1, -- Elle bir ID veriyoruz
    'World Bank', 
    'https://databank.worldbank.org/source/world-development-indicators', 
    'World Development Indicators (WDI) dataset.'
);

-- 2. Adım: Regions tablosuna bir örnek bölge ekle
-- (source_id = 1 olarak 1. adımda eklediğimiz kaydı referans gösterir)
INSERT  INTO Regions (region_name, income_group, world_bank_code, source_id)
VALUES (
    'Europe & Central Asia', 
    'High income', 
    'ECA', 
    1 -- DataSources tablosundaki 'World Bank' kaydının ID'si
),
(
    'Middle East & North Africa', 
    'Low income', 
    'MEA', 
    1 -- DataSources tablosundaki 'World Bank' kaydının ID'si
);