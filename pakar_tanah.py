# =========================================
# SISTEM PAKAR — DIAGNOSA KERUSAKAN TANAH PERTANIAN
# Metode: Forward Chaining
# Ranking: Persentase Kecocokan Gejala
# =========================================

# ------------------------------------------
# BASIS PENGETAHUAN — GEJALA
# ------------------------------------------

GEJALA = {
    'G01': 'Tanah retak-retak di permukaan',
    'G02': 'Tanaman layu meski sudah disiram',
    'G03': 'Lapisan atas tanah tipis atau menipis',
    'G04': 'Air cepat mengalir saat hujan deras',
    'G05': 'Permukaan tanah keras dan padat',
    'G06': 'Tanah berpasir, mudah hancur',
    'G07': 'Ada genangan air yang lama',
    'G08': 'Warna tanah pucat atau keputihan',
    'G09': 'Akar tanaman dangkal, tidak menembus dalam',
    'G10': 'Tanaman tumbuh kerdil dan pucat',
    'G11': 'Tanah berbau busuk atau asam',
    'G12': 'Tanah terasa berat dan lengket saat basah',
    'G13': 'Muncul bercak putih/kristal di permukaan',
    'G14': 'Pertumbuhan gulma meningkat pesat',
    'G15': 'Tanah mudah longsor atau terkikis hujan',
    'G16': 'Air tanah terasa asin atau pahit',
    'G17': 'Tanaman menguning dari daun bawah ke atas',
    'G18': 'Bekas penggunaan pupuk kimia berlebih',
    'G19': 'Aktivitas cacing tanah berkurang drastis',
    'G20': 'Tanah tidak menyerap air (air menggenang di atas)',
}


# ------------------------------------------
# BASIS PENGETAHUAN — PENYAKIT & ATURAN
# ------------------------------------------

BASIS_PENGETAHUAN = [
    {
        'nama'       : 'Erosi Tanah',
        'gejala'     : ['G03', 'G04', 'G06', 'G15', 'G14'],
        'penyebab'   : (
            'Curah hujan tinggi, lereng curam, kurangnya vegetasi '
            'penutup tanah, pengolahan tanah berlebih.'
        ),
        'rekomendasi': [
            'Tanam tanaman penutup tanah (cover crop) untuk menahan erosi',
            'Buat teras atau terasering di lahan miring',
            'Pasang pematang/guludan mengikuti kontur lahan',
            'Hindari membiarkan lahan terbuka di musim hujan',
        ],
        'urgensi': 'SEGERA',
    },
    {
        'nama'       : 'Kekeringan / Degradasi Kelembaban',
        'gejala'     : ['G01', 'G02', 'G06', 'G08', 'G10'],
        'penyebab'   : (
            'Curah hujan rendah berkepanjangan, drainase buruk, '
            'kandungan bahan organik rendah.'
        ),
        'rekomendasi': [
            'Tambahkan mulsa organik (jerami/daun) untuk menahan kelembaban',
            'Lakukan penyiraman di pagi dan sore hari secara terjadwal',
            'Tambah bahan organik (kompos) untuk memperbaiki kapasitas simpan air',
            'Gunakan irigasi tetes untuk efisiensi air',
        ],
        'urgensi': 'SEGERA',
    },
    {
        'nama'       : 'Pemadatan Tanah (Soil Compaction)',
        'gejala'     : ['G05', 'G09', 'G12', 'G20', 'G07'],
        'penyebab'   : (
            'Penggunaan alat berat berulang, pengolahan tanah saat basah, '
            'minimnya bahan organik.'
        ),
        'rekomendasi': [
            'Lakukan penggemburan tanah (subsoiling) secara berkala',
            'Tambahkan bahan organik untuk memperbaiki struktur tanah',
            'Hindari pengolahan tanah saat kondisi terlalu basah',
            'Rotasi tanaman dengan tanaman berakar dalam',
        ],
        'urgensi': 'TERJADWAL',
    },
    {
        'nama'       : 'Salinitas Tinggi',
        'gejala'     : ['G13', 'G16', 'G08', 'G10', 'G17'],
        'penyebab'   : (
            'Irigasi air asin, penggunaan pupuk kimia berlebih, '
            'evaporasi tinggi, drainase buruk.'
        ),
        'rekomendasi': [
            'Lakukan pencucian tanah (leaching) dengan air bersih berlimpah',
            'Perbaiki sistem drainase lahan',
            'Gunakan tanaman toleran salinitas sebagai peralihan',
            'Kurangi atau hentikan pupuk berbasis garam',
        ],
        'urgensi': 'SEGERA',
    },
    {
        'nama'       : 'Pencemaran Kimia',
        'gejala'     : ['G18', 'G11', 'G19', 'G10', 'G17'],
        'penyebab'   : (
            'Penggunaan pestisida/pupuk kimia berlebih, '
            'limbah industri, residu herbisida.'
        ),
        'rekomendasi': [
            'Hentikan penggunaan bahan kimia penyebab kontaminasi',
            'Tambahkan bahan organik untuk menetralisir bahan kimia',
            'Lakukan remediasi dengan tanaman fitoremediasi (bunga matahari, kenaf)',
            'Konsultasikan dengan dinas pertanian setempat untuk uji tanah',
        ],
        'urgensi': 'KRITIS',
    },
    {
        'nama'       : 'Tanah Masam Berlebih',
        'gejala'     : ['G11', 'G17', 'G10', 'G14', 'G19'],
        'penyebab'   : (
            'Curah hujan tinggi (mencuci basa), penggunaan pupuk nitrogen berlebih, '
            'dekomposisi bahan organik.'
        ),
        'rekomendasi': [
            'Aplikasikan kapur pertanian (dolomit/kalsit) sesuai dosis uji tanah',
            'Kurangi penggunaan pupuk nitrogen jenis sulfat/klorida',
            'Tambahkan abu sekam atau abu kayu sebagai penyeimbang pH',
            'Lakukan uji pH tanah secara rutin',
        ],
        'urgensi': 'TERJADWAL',
    },
]


# ------------------------------------------
# MESIN INFERENSI — FORWARD CHAINING
# ------------------------------------------

def diagnosa(gejala_input: list[str]) -> list[dict]:
    """
    Mendiagnosa kerusakan tanah berdasarkan gejala yang diinput.

    Parameter:
      gejala_input : list kode gejala, misal ['G01', 'G02', 'G05']

    Return:
      list of dict, diurutkan berdasarkan persentase kecocokan tertinggi
    """
    if not gejala_input:
        return []

    selected = set(gejala_input)
    hasil = []

    for penyakit in BASIS_PENGETAHUAN:
        aturan_set = set(penyakit['gejala'])
        cocok      = selected & aturan_set
        kurang     = aturan_set - selected

        skor      = len(cocok)
        persentase = round((skor / len(aturan_set)) * 100, 1)

        if skor > 0:
            hasil.append({
                'nama'      : penyakit['nama'],
                'skor'      : skor,
                'total'     : len(aturan_set),
                'persentase': persentase,
                'urgensi'   : penyakit['urgensi'],
                'penyebab'  : penyakit['penyebab'],
                'rekomendasi': penyakit['rekomendasi'],
                'gejala_cocok' : [f"{k} - {GEJALA[k]}" for k in sorted(cocok)],
                'gejala_kurang': [f"{k} - {GEJALA[k]}" for k in sorted(kurang)],
            })

    hasil.sort(key=lambda x: (-x['persentase'], -x['skor']))
    return hasil


# ------------------------------------------
# TAMPILAN OUTPUT
# ------------------------------------------

def tampilkan_hasil(hasil: list[dict]):
    if not hasil:
        print("Tidak ditemukan kerusakan tanah yang cocok.")
        return

    print("\n" + "=" * 60)
    print("  DIAGNOSA UTAMA")
    print("=" * 60)
    top = hasil[0]
    print(f"  Jenis Kerusakan : {top['nama']}")
    print(f"  Kecocokan       : {top['persentase']}% ({top['skor']}/{top['total']} gejala)")
    print(f"  Urgensi         : {top['urgensi']}")
    print(f"\n  Penyebab Umum:")
    print(f"  {top['penyebab']}")
    print(f"\n  Gejala yang Cocok:")
    for g in top['gejala_cocok']:
        print(f"    ✓ {g}")
    if top['gejala_kurang']:
        print(f"\n  Gejala yang Tidak Dipilih:")
        for g in top['gejala_kurang']:
            print(f"    — {g}")
    print(f"\n  Rekomendasi Penanganan:")
    for i, r in enumerate(top['rekomendasi'], 1):
        print(f"    {i}. {r}")

    if len(hasil) > 1:
        print("\n" + "-" * 60)
        print("  RANKING SEMUA KEMUNGKINAN")
        print("-" * 60)
        for i, h in enumerate(hasil, 1):
            bar = '█' * int(h['persentase'] / 10) + '░' * (10 - int(h['persentase'] / 10))
            print(f"  {i}. {h['nama']:<35} {bar} {h['persentase']}%")

    print("=" * 60)


# ------------------------------------------
# CONTOH PENGGUNAAN
# ------------------------------------------

if __name__ == '__main__':
    print("SISTEM PAKAR — DIAGNOSA KERUSAKAN TANAH PERTANIAN")
    print("Metode: Forward Chaining\n")

    # Kasus 1: Kekeringan
    print("[ KASUS 1 ] Gejala: G01, G02, G06, G08")
    hasil1 = diagnosa(['G01', 'G02', 'G06', 'G08'])
    tampilkan_hasil(hasil1)

    # Kasus 2: Erosi
    print("\n[ KASUS 2 ] Gejala: G03, G04, G15, G14")
    hasil2 = diagnosa(['G03', 'G04', 'G15', 'G14'])
    tampilkan_hasil(hasil2)

    # Kasus 3: Pencemaran kimia
    print("\n[ KASUS 3 ] Gejala: G18, G11, G19, G17")
    hasil3 = diagnosa(['G18', 'G11', 'G19', 'G17'])
    tampilkan_hasil(hasil3)
