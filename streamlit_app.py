import streamlit as st
import math
from chempy import balance_stoichiometry

# --- 1. DATABASE ION DASAR ---
# Format: 'Simbol': (Muatan, Apakah Poliatomik?)
kation_db = {
    'Ag': (1, False), 'Na': (1, False), 'K': (1, False), 'H': (1, False), 'Li': (1, False),
    'Ba': (2, False), 'Ca': (2, False), 'Mg': (2, False), 'Cu': (2, False), 'Pb': (2, False), 'Zn': (2, False),
    'Al': (3, False), 'Fe': (3, False)
}

anion_db = {
    'Cl': (-1, False), 'Br': (-1, False), 'I': (-1, False), 'F': (-1, False),
    'NO3': (-1, True), 'OH': (-1, True), 'CH3COO': (-1, True),
    'SO4': (-2, True), 'CO3': (-2, True), 'CrO4': (-2, True), 'S': (-2, False),
    'PO4': (-3, True)
}

# --- 2. FUNGSI LOGIKA KIMIA ---
def urai_senyawa(senyawa):
    """Mendeteksi kation dan anion dari teks input senyawa"""
    kation_terdeteksi = None
    anion_terdeteksi = None
    
    # Cari Kation (Cek dari string terpanjang untuk akurasi)
    for k in sorted(kation_db.keys(), key=len, reverse=True):
        if senyawa.startswith(k):
            kation_terdeteksi = k
            sisa_string = senyawa[len(k):]
            break
            
    if not kation_terdeteksi:
        return None, None

    # Cari Anion di sisa string
    for a in sorted(anion_db.keys(), key=len, reverse=True):
        if a in sisa_string:
            anion_terdeteksi = a
            break
            
    return kation_terdeteksi, anion_terdeteksi

def gabung_ion(kation, anion):
    """Menggabungkan ion menjadi senyawa baru berdasarkan muatannya (KPK)"""
    muatan_k = abs(kation_db[kation][0])
    muatan_a = abs(anion_db[anion][0])
    is_poliatomik_a = anion_db[anion][1]
    
    # Hitung Kelipatan Persekutuan Terkecil (KPK) untuk menetralkan muatan
    kpk = (muatan_k * muatan_a) // math.gcd(muatan_k, muatan_a)
    
    indeks_k = kpk // muatan_k
    indeks_a = kpk // muatan_a
    
    # Format kation
    hasil_k = kation if indeks_k == 1 else f"{kation}{indeks_k}"
    
    # Format anion (gunakan kurung jika poliatomik dan indeks > 1)
    if indeks_a == 1:
        hasil_a = anion
    else:
        hasil_a = f"({anion}){indeks_a}" if is_poliatomik_a else f"{anion}{indeks_a}"
        
    return f"{hasil_k}{hasil_a}"

def format_reaksi_str(senyawa_dict):
    """Mengubah dictionary chempy menjadi string reaksi yang rapi"""
    hasil = []
    for seny, koef in senyawa_dict.items():
        hasil.append(f"{seny}" if koef == 1 else f"{koef}{seny}")
    return " + ".join(hasil)

# --- 3. ANTARMUKA STREAMLIT ---
st.set_page_config(page_title="Prediksi & Balancer Metatesis", page_icon="🧪")

st.title("🧪 Engine Reaksi Metatesis")
st.markdown("Masukkan dua senyawa reaktan. Sistem akan **menebak produk pertukaran gandanya** dan **menyetarakan reaksinya** secara otomatis.")

st.info("💡 **Tips Input:** Gunakan senyawa umum. Contoh: AgNO3, BaCl2, Na2SO4, Pb(NO3)2, KI.")

col1, col2 = st.columns(2)
with col1:
    reaktan1 = st.text_input("Reaktan 1", "AgNO3").strip()
with col2:
    reaktan2 = st.text_input("Reaktan 2", "BaCl2").strip()

if st.button("Proses Reaksi", type="primary"):
    # Tahap 1: Ekstraksi Ion
    k1, a1 = urai_senyawa(reaktan1)
    k2, a2 = urai_senyawa(reaktan2)
    
    if not (k1 and a1 and k2 and a2):
        st.error("❌ Senyawa tidak dikenali atau di luar database. Pastikan format penulisan benar (huruf besar/kecil sesuai kaidah kimia).")
    else:
        # Tahap 2: Silangkan Ion (Metatesis)
        # Kation 1 + Anion 2 | Kation 2 + Anion 1
        produk1 = gabung_ion(k1, a2)
        produk2 = gabung_ion(k2, a1)
        
        st.success("✅ Produk berhasil ditebak dan direaksikan!")
        
        # Tahap 3: Penyetaraan dengan Chempy
        try:
            reaktan_dict = {reaktan1: 1, reaktan2: 1}
            produk_dict = {produk1: 1, produk2: 1}
            
            # Chempy menyeimbangkan reaksi
            r_setara, p_setara = balance_stoichiometry(
                {reaktan1, reaktan2}, 
                {produk1, produk2}
            )
            
            # Tampilkan Hasil Visual
            st.subheader("Hasil Reaksi Setara:")
            kiri = format_reaksi_str(r_setara)
            kanan = format_reaksi_str(p_setara)
            
            # Menampilkan bentuk formula LaTeX
            st.latex(f"{kiri} \\rightarrow {kanan}")
            
            st.divider()
            
            # Tampilkan Detail Logika (Breakdown)
            st.markdown("### 🔍 Detail Analisis Kimia")
            st.markdown("Berikut adalah mekanisme pertukaran ion yang dilakukan oleh sistem di belakang layar:")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Pemecahan Reaktan 1:**\n- Kation: ${k1}^{{{kation_db[k1][0]}+}}$\n- Anion: ${a1}^{{{anion_db[a1][0]}-}}$")
            with col_b:
                st.markdown(f"**Pemecahan Reaktan 2:**\n- Kation: ${k2}^{{{kation_db[k2][0]}+}}$\n- Anion: ${a2}^{{{anion_db[a2][0]}-}}$")
                
            st.markdown(f"""
            **Mekanisme Pertukaran (Silang):**
            1. ${k1}^{{{kation_db[k1][0]}+}}$ berikatan dengan ${a2}^{{{anion_db[a2][0]}-}}$ membentuk **${produk1}$**
            2. ${k2}^{{{kation_db[k2][0]}+}}$ berikatan dengan ${a1}^{{{anion_db[a1][0]}-}}$ membentuk **${produk2}$**
            """)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan pada kalkulasi stoikiometri: {e}")

st.divider()
st.caption("Dikembangkan oleh: Agung Nugraha (NIM 2560557) - D3 Analisis Kimia")
