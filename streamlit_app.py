import streamlit as st
import math
from chempy import balance_stoichiometry

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Chemical Metathesis Engine", page_icon="🧪", layout="centered")

# --- 2. MANAGEMENT HALAMAN (SESSION STATE) ---
if 'halaman_utama' not in st.session_state:
    st.session_state.halaman_utama = False

# --- 3. CUSTOM STYLING (CSS INTERAKTIF) ---
st.markdown("""
    <style>
    /* Desain Halaman Cover */
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
        color: #FBBF24; /* Warna Gold */
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .member-name {
        font-size: 17px;
        font-weight: 500;
        margin: 6px 0;
    }
    
    /* Desain Core App */
    .app-header {
        font-size: 32px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# SCREEN 1: HALAMAN COVER (AWAL)
# ==============================================================================
if not st.session_state.halaman_utama:
    
    # Elemen Visual Cover
    st.markdown("""
        <div class="cover-box">
            <div class="cover-title">🧪 ENGINE REAKSI METATESIS</div>
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
    
    # Tombol Masuk yang Besar dan Menarik
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("KLIK UNTUK MASUK APLIKASI ➔", type="primary", use_container_width=True):
            st.session_state.halaman_utama = True
            st.rerun()

    st.markdown("<br><p style='text-align:center; color:#9CA3AF; font-size:13px;'>D3 Analisis Kimia • Politeknik AKA Bogor</p>", unsafe_allow_html=True)


# ==============================================================================
# SCREEN 2: HALAMAN INTI / CORE APPLICATION
# ==============================================================================
else:
    # Tombol Navigasi Kembali ke Cover di bagian atas secara elegan
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

    # --- LOGIKA KIMIA ---
    def urai_senyawa(senyawa):
        kation_terdeteksi, anion_terdeteksi = None, None
        for k in sorted(kation_db.keys(), key=len, reverse=True):
            if senyawa.startswith(k):
                kation_terdeteksi = k
                sisa_string = senyawa[len(k):]
                break
        if not kation_terdeteksi:
            return None, None
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
        return f"{hasil_k}{hasil_a}"

    def apakah_mengendap(kation, anion):
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
            wujud = "(s)" if (k and a and apakah_mengendap(k, a)) else "(aq)"
            if seny == "H2O": wujud = "(l)"
            prefix = "" if koef == 1 else f"{koef}"
            hasil.append(f"{prefix}{seny}{wujud}")
        return " + ".join(hasil)

    # --- MENU INPUT UTAMA ---
    st.subheader("📝 Menu Analisis Stoikiometri")
    st.markdown("Masukkan senyawa kimia reaktan untuk memulai perhitungan:")
    
    col1, col2 = st.columns(2)
    with col1:
        reaktan1 = st.text_input("Reaktan 1", "AgNO3").strip()
    with col2:
        reaktan2 = st.text_input("Reaktan 2", "BaCl2").strip()

    if st.button("Analisis Reaksi", type="primary"):
        if reaktan1 == "H2O" or reaktan2 == "H2O":
            st.warning("⚠️ **Analisis Teori:** Salah satu reaktan adalah air ($H_2O$). Proses ini memicu pelarutan fisik, bukan reaksi metatesis kimia.")
        else:
            k1, a1 = urai_senyawa(reaktan1)
            k2, a2 = urai_senyawa(reaktan2)
            
            if not (k1 and a1 and k2 and a2):
                st.error("❌ Senyawa tidak dikenali. Perhatikan kaidah penulisan huruf kapital (Contoh: NaCl).")
            else:
                produk1 = gabung_ion(k1, a2)
                produk2 = gabung_ion(k2, a1)
                mengendap_p1 = apakah_mengendap(k1, a2)
                mengendap_p2 = apiKey = apakah_mengendap(k2, a1)
                
                try:
                    r_setara, p_setara = balance_stoichiometry({reaktan1, reaktan2}, {produk1, produk2})
                    kiri = format_reaksi_str(r_setara)
                    kanan = format_reaksi_str(p_setara)
                    
                    if not mengendap_p1 and not mengendap_p2:
                        st.error("❌ Secara Teori: TIDAK TERJADI REAKSI (No Reaction)")
                        st.latex(f"{reaktan1}(aq) + {reaktan2}(aq) \\rightarrow \\text{{Tidak Bereaksi}}")
                        st.info(f"**Penjelasan Ilmiah:** Produk berpotensi menjadi {produk1} dan {produk2}, namun keduanya larut sempurna di air, sehingga tidak memicu reaksi kimia nyata.")
                    else:
                        st.success("✅ Secara Teori: REAKSI BERLANGSUNG (Valid)")
                        st.subheader("Persamaan Reaksi Setara:")
                        st.latex(f"{kiri} \\rightarrow {kanan}")
                        
                        endapan = []
                        if mengendap_p1: endapan.append(f"**{produk1}**")
                        if mengendap_p2: endapan.append(f"**{produk2}**")
                        st.markdown(f"**Driving Force:** Terbentuk fase padat/endapan {', '.join(endapan)} di dalam larutan.")
                    
                    st.divider()
                    st.markdown("### 🔍 Lembar Kerja Analisis Ion")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Reaktan 1:**\n- ${k1}^{{{kation_db[k1][0]}+}}$\n- ${a1}^{{{anion_db[a1][0]}-}}$")
                    with col_b:
                        st.markdown(f"**Reaktan 2:**\n- ${k2}^{{{kation_db[k2][0]}+}}$\n- ${a2}^{{{anion_db[a2][0]}-}}$")

                except Exception as e:
                    st.error("❌ Reaksi tidak dapat disetarakan secara matematis stoikiometri.")
