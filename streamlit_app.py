import streamlit as st
import math
from chempy import balance_stoichiometry

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Reaksi Metatesis", page_icon="🧪", layout="centered")

# --- 2. MANAGEMENT HALAMAN (SESSION STATE) ---
if 'halaman_utama' not in st.session_state:
    st.session_state.halaman_utama = False

# --- 3. CUSTOM STYLING (CSS INTERAKTIF) ---
st.markdown("""
<style>
.cover-box {
    text-align: center;
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
    padding: 50px 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 15px 35px rgba(30, 58, 138, 0.2);
    margin-bottom: 30px;
}
.cover-title {
    font-family: 'Arial Black', Gadget, sans-serif;
    font-size: 40px;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 10px;
    line-height: 1.2;
}
.cover-subtitle {
    font-size: 16px;
    opacity: 0.9;
    font-weight: 300;
    margin-bottom: 40px;
}
.cover-card-team {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    max-width: 450px;
    margin: 0 auto;
}
.team-label {
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 3px;
    color: #FBBF24;
    margin-bottom: 15px;
    text-transform: uppercase;
}
.member-name {
    font-size: 17px;
    font-weight: 500;
    margin: 6px 0;
}
.app-header {
    font-size: 32px;
    font-weight: 800;
    color: #1E3A8A;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SCREEN 1: HALAMAN COVER 
# ==============================================================================
if not st.session_state.halaman_utama:
    st.markdown("""
<div class="cover-box">
<div class="cover-title">🧪 REAKSI METATESIS</div>
<div class="cover-subtitle">Aplikasi Pintar Prediksi Produk, Penyetaraan Stoikiometri, <br>dan Verifikasi Kelarutan Zat Analitis</div>
<div class="cover-card-team">
<div class="team-label">👥 Kelompok Pengembang</div>
<div class="member-name">✨ Agung Nugraha</div>
<div class="member-name">✨ Alifia Citra Nabila</div>
<div class="member-name">✨ Haifa Maulafida</div>
<div class="member-name">✨ Nabila Putri Khorinnisa</div>
<div class="member-name">✨ Rania Ayudia</div>
</div>
</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("KLIK UNTUK MASUK APLIKASI ➔", type="primary", use_container_width=True):
            st.session_state.halaman_utama = True
            st.rerun()

    st.markdown("<br><p style='text-align:center; color:#9CA3AF; font-size:13px;'>D3 Analisis Kimia • Politeknik AKA Bogor</p>", unsafe_allow_html=True)


# ==============================================================================
# SCREEN 2: HALAMAN INTI
# ==============================================================================
else:
    if st.button("⬅ Kembali ke Cover", type="secondary"):
        st.session_state.halaman_utama = False
        st.rerun()
        
    st.markdown('<div class="app-header">🧪 Dashboard Analisis Reaksi</div>', unsafe_allow_html=True)
    st.markdown("Sistem mendeteksi muatan ion secara otomatis untuk menyilangkan produk reaktan secara instan.")
    st.divider()

    # --- DATABASE ION SUPER LENGKAP ---
    kation_db = {
        'H': (1, False), 'Li': (1, False), 'Na': (1, False), 'K': (1, False), 'Rb': (1, False), 'Cs': (1, False),
        'Be': (2, False), 'Mg': (2, False), 'Ca': (2, False), 'Sr': (2, False), 'Ba': (2, False),
        'Ag': (1, False), 'Zn': (2, False), 'Cd': (2, False), 'Al': (3, False), 'Bi': (3, False),
        'Cu': (2, False), 'Fe': (3, False), 'Pb': (2, False), 'Ni': (2, False), 'Co': (2, False), 
        'Mn': (2, False), 'Cr': (3, False), 'Sn': (2, False), 'Hg': (2, False), 'NH4': (1, True)
    }

    anion_db = {
        'F': (-1, False), 'Cl': (-1, False), 'Br': (-1, False), 'I': (-1, False),
        'OH': (-1, True), 'NO3': (-1, True), 'NO2': (-1, True), 'CN': (-1, True), 'SCN': (-1, True), 
        'CH3COO': (-1, True), 'ClO': (-1, True), 'ClO2': (-1, True), 'ClO3': (-1, True), 'ClO4': (-1, True), 
        'MnO4': (-1, True), 'HCO3': (-1, True), 'HSO4': (-1, True), 'H2PO4': (-1, True),
        'O': (-2, False), 'S': (-2, False),
        'SO4': (-2, True), 'SO3': (-2, True), 'CO3': (-2, True), 'CrO4': (-2, True), 'Cr2O7': (-2, True), 
        'C2O4': (-2, True), 'S2O3': (-2, True), 'HPO4': (-2, True),
        'PO4': (-3, True), 'PO3': (-3, True), 'AsO4': (-3, True), 'N': (-3, False), 'P': (-3, False)
    }

    def urai_senyawa(senyawa):
        kation_terdeteksi, anion_terdeteksi = None, None
        for k in sorted(kation_db.keys(), key=len, reverse=True):
            if senyawa.startswith(k):
                kation_terdeteksi = k
                sisa_string = senyawa[len(k):]
                break
        if not kation_terdeteksi: return None, None
        for a in sorted(anion_db.keys(), key=len, reverse=True):
            if a in sisa_string:
                anion_terdeteksi = a
                break
        return kation_terdeteksi, anion_terdeteksi

    def gabung_ion(kation, anion):
        muatan_k, muatan_a = abs(kation_db[kation][0]), abs(anion_db[anion][0])
        is_poliatomik_a = anion_db[anion][1]
        kpk = (muatan_k * muatan_a) // math.gcd(muatan_k, muatan_a)
        indeks_k, indeks_a = kpk // muatan_k, kpk // muatan_a
        hasil_k = kation if indeks_k == 1 else f"{kation}{indeks_k}"
        
        if indeks_a == 1:
            hasil_a = anion
        else:
            hasil_a = f"({anion}){indeks_a}" if is_poliatomik_a else f"{anion}{indeks_a}"
            
        senyawa_baru = f"{hasil_k}{hasil_a}"
        if senyawa_baru == "HOH": return "H2O"
        return senyawa_baru

    def apakah_mengendap(kation, anion):
        if kation == 'H' and anion in ['OH', 'O']: return False
        if kation in ['Na', 'K', 'NH4', 'Li', 'Rb', 'Cs']: return False
        if anion in ['NO3', 'CH3COO']: return False
        if anion in ['Cl', 'Br', 'I']: return True if kation in ['Ag', 'Pb', 'Hg'] else False
        if anion == 'SO4': return True if kation in ['Ba', 'Ca', 'Sr', 'Pb'] else False
        if anion == 'OH': return False if kation in ['Ca', 'Sr', 'Ba'] else True
        if anion in ['CO3', 'PO4', 'CrO4', 'S', 'O']: return True
        return False

    def format_reaksi_str(senyawa_dict):
        hasil = []
        for seny, koef in senyawa_dict.items():
            k, a = urai_senyawa(seny)
            if seny == "H2O":
                wujud = "(l)"
            else:
                wujud = "(s)" if (k and a and apakah_mengendap(k, a)) else "(aq)"
            prefix = "" if koef == 1 else f"{koef}"
            hasil.append(f"{prefix}{seny}{wujud}")
        return " + ".join(hasil)
        
    def fmt_muatan(nilai, tanda):
        """Merapikan format muatan (contoh: 1+ menjadi +)"""
        return tanda if nilai == 1 else f"{nilai}{tanda}"

    # --- MENU INPUT UTAMA ---
    st.subheader("📝 Menu Analisis Stoikiometri")
    st.markdown("Masukkan senyawa kimia reaktan untuk memulai perhitungan:")
    
    col1, col2 = st.columns(2)
    with col1:
        reaktan1 = st.text_input("Reaktan 1", "NaOH").strip()
    with col2:
        reaktan2 = st.text_input("Reaktan 2", "HCl").strip()

    if st.button("Analisis Reaksi", type="primary"):
        if reaktan1 == "H2O" or reaktan2 == "H2O":
            st.warning("⚠️ Salah satu reaktan adalah air ($H_2O$). Proses ini memicu pelarutan fisik, bukan reaksi metatesis kimia.")
        else:
            k1, a1 = urai_senyawa(reaktan1)
            k2, a2 = urai_senyawa(reaktan2)
            
            if not (k1 and a1 and k2 and a2):
                st.error("❌ Senyawa tidak dikenali. Perhatikan kaidah penulisan huruf kapital.")
            else:
                produk1 = gabung_ion(k1, a2)
                produk2 = gabung_ion(k2, a1)
                
                mengendap_p1 = apakah_mengendap(k1, a2) and produk1 != "H2O"
                mengendap_p2 = apakah_mengendap(k2, a1) and produk2 != "H2O"
                membentuk_air = (produk1 == "H2O" or produk2 == "H2O")
                
                try:
                    r_setara, p_setara = balance_stoichiometry({reaktan1, reaktan2}, {produk1, produk2})
                    kiri = format_reaksi_str(r_setara)
                    kanan = format_reaksi_str(p_setara)
                    
                    if not mengendap_p1 and not mengendap_p2 and not membentuk_air:
                        st.error("❌ Secara Teori: TIDAK TERJADI REAKSI (No Reaction)")
                        st.latex(f"{reaktan1}(aq) + {reaktan2}(aq) \\rightarrow \\text{{Tidak Bereaksi}}")
                    else:
                        st.success("✅ Secara Teori: REAKSI BERLANGSUNG (Valid)")
                        st.subheader("Persamaan Reaksi Setara:")
                        st.latex(f"{kiri} \\rightarrow {kanan}")
                        
                        alasan = []
                        if mengendap_p1: alasan.append(f"fase padat/endapan **{produk1}**")
                        if mengendap_p2: alasan.append(f"fase padat/endapan **{produk2}**")
                        if membentuk_air: alasan.append(f"**molekul air ($H_2O$)** yang bersifat elektrolit lemah")
                        
                        st.markdown(f"**Driving Force:** Reaksi berlangsung karena terbentuk {', '.join(alasan)}.")
                    
                    st.divider()
                    
                    # ------------------------------------------------------------------
                    # PEMBARUAN VISUALISASI PERSILANGAN MUATAN (Sesuai Gambar User)
                    # ------------------------------------------------------------------
                    st.markdown("### 🔍 Lembar Kerja Analisis & Persilangan Ion")
                    
                    # 1. Format muatan untuk tampilan
                    c_k1 = fmt_muatan(kation_db[k1][0], '+')
                    c_a1 = fmt_muatan(abs(anion_db[a1][0]), '-')
                    c_k2 = fmt_muatan(kation_db[k2][0], '+')
                    c_a2 = fmt_muatan(abs(anion_db[a2][0]), '-')

                    # 2. Pemecahan Reaktan (Penguraian Ion)
                    col_uraian1, col_uraian2 = st.columns(2)
                    with col_uraian1:
                        st.markdown("**Penguraian Reaktan 1:**")
                        st.latex(f"{reaktan1} \\longrightarrow {k1}^{{{c_k1}}} + {a1}^{{{c_a1}}}")
                    with col_uraian2:
                        st.markdown("**Penguraian Reaktan 2:**")
                        st.latex(f"{reaktan2} \\longrightarrow {k2}^{{{c_k2}}} + {a2}^{{{c_a2}}}")

                    # 3. Penjelasan Aturan Silang
                    st.info("💡 **Aturan Silang Muatan:** Kation (positif) dari reaktan pertama akan bergabung dengan Anion (negatif) dari reaktan kedua, dan sebaliknya, membentuk senyawa baru menggunakan rumus:  $A^{x+} + B^{y-} \\rightarrow A_yB_x$")

                    # 4. Pembentukan Produk (Persilangan)
                    col_prod1, col_prod2 = st.columns(2)
                    with col_prod1:
                        st.markdown("**Silang 1 (Pembentukan Produk 1):**")
                        st.latex(f"{k1}^{{{c_k1}}} + {a2}^{{{c_a2}}} \\longrightarrow {produk1}")
                    with col_prod2:
                        st.markdown("**Silang 2 (Pembentukan Produk 2):**")
                        st.latex(f"{k2}^{{{c_k2}}} + {a1}^{{{c_a1}}} \\longrightarrow {produk2}")

                except Exception as e:
                    st.error("❌ Reaksi tidak dapat disetarakan secara matematis stoikiometri.")
