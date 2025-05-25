import pandas as pd

# Kaldırılacak sütunların listesi
columns_to_drop = [
    'MusteriBolge2',
    'RutAdi',
    'RutgrupKod',
    'SatisTemsilcisi',
    'StTakipKod',
    'SatisSefi',
    'SonGuncellenmeZamani',
    'not',
    'username',
    'Url detay',
    'url',
    'DDegeri',
    'RDegeri',
    'HDegeri',
    'IsbirligiDuzeyi'
]

# Giriş ve çıkış dosyalarının adları
input_csv_file = 'maindata.csv'
output_csv_file = 'filtered_data.csv'

try:
    df = pd.read_csv(input_csv_file, sep=';', encoding='utf-8')

   

    # Mevcut sütunları kontrol et ve sadece var olanları kaldır
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    
    if not columns_to_drop_existing:
        print(f"Belirtilen sütunlardan hiçbiri '{input_csv_file}' dosyasında bulunamadı.")
    else:
        # Belirtilen sütunları çıkar
        df_filtered = df.drop(columns=columns_to_drop_existing)

        # Filtrelenmiş veriyi yeni bir CSV dosyasına yaz
        df_filtered.to_csv(output_csv_file, sep=';', index=False, encoding='utf-8')
        print(f"Filtrelenmiş veri '{output_csv_file}' dosyasına başarıyla yazıldı.")
        print(f"Kaldırılan sütunlar: {columns_to_drop_existing}")

except FileNotFoundError:
    print(f"Hata: '{input_csv_file}' dosyası bulunamadı.")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
    print("Lütfen CSV dosyasının doğru formatta ve encoding'de olduğundan emin olun.")
    print("Özellikle Türkçe karakterler varsa 'utf-8', 'iso-8859-9' veya 'windows-1254' encodinglerini deneyebilirsiniz.")
