# Proje: Kişisel ev egzersiz programı (Türkçe)

Bu klasör Claude sohbetinden Claude Code'a devredildi. Kullanıcıyla Türkçe konuş, sade ve motive edici ama gerçekçi bir dil kullan.

## Kullanıcı
- 28 yaş, kadın, 164 cm, 58 kg. Kilosu normal aralıkta, hedef yağ oranını düşürüp kas tonusu kazanmak (vücut rekompozisyonu). İlk hedef: 12 hafta, ~3-4 kg yağ kaybı ve/veya bel çevresinde azalma + güç artışı. Başta söylediği "8 kg" hedefi BMI'yi alt sınıra çeker; 12. haftada ölçülerle birlikte yeniden değerlendir.
- Kaygıları: kalça, basen ve uyluk bölgesinde sallanma. 5-6 ay önce Reformer yapmış, ara ara ev videoları.
- Sağlık sorunu/sakatlık belirtmedi.
- Haftada 4 gün, en fazla 45-50 dk. Evde.

## Ekipman (assets/ekipman.jpeg, repoya henüz eklenmedi)
- 2 kg çift dumbbell, mat
- Umbro 3'lü loop band seti: mavi 4,5 kg / kırmızı 6,75 kg / siyah 9 kg (lateks, ~76 cm)
- North Pacific uzun elastik esneme bandı (pull-apart ve row için)

## Dosyalar
- `program.json`: programın tek kaynağı (günler, hareketler, set×tekrar, ipuçları, ilerleme, beslenme, güvenlik). Programı değiştirirken sadece bunu düzenle.
- `build.py`: `program.json` -> `program.pdf` + `gunluk.html` (DejaVu fontu, çizim figürleri). `python3 build.py`
- `program.pdf`: çıktı (günler, 12 haftalık plan, yazdırılabilir günlük sayfası).
- `gorseller/`: hareket rehberi fotoğrafları (Free Exercise DB, Unlicense). `program.json` -> `guide` bu dosyalara `img` adıyla bağlanır.
- `gunluk_sablon.html`: HTML günlüğün şablonu; hareket listesi build sırasında `program.json`'dan eklenir. Günlüğü değiştirirken bunu düzenle.
- `gunluk.html`: üretilen antrenman günlüğü (tarayıcıda açılır, kayıtlar localStorage'da, CSV indir/yükle).
- `gunluk.csv`: aynı sütunlarla boş CSV şablonu (`;` ayraçlı, Türkçe Excel uyumlu).

## Programın dayanağı (araştırma özeti)
- ACSM 2026 direnç antrenmanı position stand'ı: her sınıf ekipman işe yarar, tükenene kadar gitmek şart değil, hipertrofi için haftalık ~10 set/kas grubu, tutarlılık karmaşıklıktan önemli.
- WHO 2020: yetişkinlere haftada 150-300 dk orta tempolu aerobik + haftada en az 2 gün kas güçlendirme.
- Direnç bandı vs. ağırlık: eşit efor ve ilerlemeyle benzer güç kazancı (2019 SAGE meta-analizi, 8 çalışma). Şart: bantları zamanla zorlaştırmak.
- HIIT vs. sürekli orta tempo: yağ kaybı benzer, kişi neyi sürdürebiliyorsa onu seçsin.
- Rekompozisyon: direnç antrenmanı + yeterli protein (ISSN: 1,4-2,0 g/kg) + hafif/orta kalori açığı.
- Kalça: banded glute bridge'in kalça kaslarını güçlü aktive ettiği EMG çalışmalarında gösterilmiş; ek yük (dumbbell) ve tek bacak varyasyonları ilerleme için kullanılıyor.

## Yapılacaklar (Claude Code için)
1. ~~`program.json`'u gözden geçir, tutarsızlık varsa düzelt.~~ (yapıldı)
2. ~~Gerçek hareket fotoğrafları/GIF'leri yerine şimdilik çizim figür var. İstenirse lisanslı/serbest görsel kaynakları araştırıp ekle.~~ (yapıldı: `guide` + `gorseller/`, Free Exercise DB, kamu malı/Unlicense)
3. ~~İlerleme takibi için basit bir antrenman günlüğü (CSV veya HTML) ekle: tarih, hareket, set, tekrar, bant rengi, zorluk 1-10.~~ (yapıldı: gunluk.html + gunluk.csv)
4. ~~Programı 12 hafta için haftalık tabloya aç (hafta 1-2 form, 3-8 yük, 9-12 varyasyon, 7. veya 8. hafta deload).~~ (yapıldı: `weeks`, 8. hafta deload)

## Sınırlar
- Tıbbi tavsiye verme; ağrı/sağlık sorunu olursa hekime yönlendir.
- Aşırı kalori kısıtlaması ya da hızlı kilo verme önerme.
- Kullanıcının sohbet geçmişi bu klasöre taşınmadı; yukarıdaki bilgiler tam özet.
