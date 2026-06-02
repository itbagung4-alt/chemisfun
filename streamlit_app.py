import streamlit as st
import pandas as pd
import math
from chempy import balance_stoichiometry

# ─── 1. KONFIGURASI HALAMAN ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Portal Analisis Kimia",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── 2. LOAD CSS GLOBAL (TEMA TERANG / LIGHT MODE) ──────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@700&display=swap');
:root {
    --bg: #f8fafc;         /* Slate 50 - Latar belakang utama */
    --surface: #ffffff;    /* Putih murni untuk kartu */
    --surface2: #f1f5f9;   /* Slate 100 - Latar belakang sekunder/input */
    --border: #cbd5e1;     /* Slate 300 - Garis batas */
    --accent: #0284c7;     /* Light Blue 600 */
    --accent2: #6366f1;    /* Indigo 500 */
    --accent3: #059669;    /* Emerald 600 */
    --text: #0f172a;       /* Slate 900 - Teks utama gelap */
    --text-muted: #475569; /* Slate 600 - Teks pendukung */
    --font-body: 'DM Sans', sans-serif; 
    --font-mono: 'Space Mono', monospace;
    --font-display: 'Playfair Display', serif; 
    --radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}
html, body, [class*="css"] { font-family: var(--font-body) !important; color: var(--text) !important; }
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Komponen Portal & Tim ─── */
.landing-hero { text-align: center; padding: 2rem 2rem 1rem; }
.hero-badge {
    display: inline-block; font-family: var(--font-mono); font-size: 0.75rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent);
    border: 1px solid rgba(2, 132, 199, 0.3); padding: 0.4rem 1.2rem;
    border-radius: 999px; margin-bottom: 1rem; background: rgba(2, 132, 199, 0.05);
}
.hero-title {
    font-family: var(--font-display) !important; font-size: clamp(2rem, 4vw, 3rem) !important;
    font-weight: 700 !important; line-height: 1.15 !important; color: var(--text) !important;
    margin-bottom: 0.5rem !important;
}
.hero-accent {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { font-size: 1.05rem; color: var(--text-muted); max-width: 600px; margin: 0 auto; line-height: 1.6; }

/* Kartu Tim Pengembang di Depan */
.team-banner {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1.5rem; text-align: center; margin: 1.5rem auto 3rem; max-width: 900px;
    box-shadow: var(--shadow); border-top: 4px solid var(--accent);
}
.team-banner h4 { font-size: 1rem; color: var(--accent); margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.team-banner p { font-size: 0.95rem; color: var(--text); font-weight: 500; line-height: 1.8; margin: 0; }

.portal-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
    padding: 2.5rem 2rem; text-align: center; transition: all 0.3s ease; height: 100%; box-shadow: var(--shadow);
}
.portal-card:hover { border-color: var(--accent); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); transform: translateY(-5px); }
.portal-card h3 { color: var(--text); font-weight: 700; margin-top: 10px; }

/* ─── Komponen Spesifik ─── */
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; margin-top: 2rem; }
.feature-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.6rem; box-shadow: var(--shadow); }
.page-title { font-family: var(--font-display) !important; font-size: 2rem !important; color: var(--text) !important; margin-bottom: 0.3rem !important; }
.page-sub { color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem; }
.app-header { font-size: 32px; font-weight: 800; color: var(--accent); margin-bottom: 5px; }

/* ─── General Streamlit Override ─── */
.stButton > button {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important;
    font-weight: 600 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
.stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; border-color: transparent !important; color: white !important; }
.stButton > button[kind="primary"]:hover { opacity: 0.9 !important; color: white !important; }

.stTextInput > div > div > input, .stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
.streamlit-expanderHeader { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; color: var(--text) !important; font-weight: 600 !important; }
.streamlit-expanderContent { background: var(--surface) !important; border: 1px solid var(--border) !important; border-top: none !important; }
hr { border-color: var(--border) !important; }
code, pre { background: var(--surface2) !important; border: 1px solid var(--border) !important; color: var(--accent2) !important; border-radius: 6px !important; }
.stAlert { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }

.result-box { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-top: 1.5rem; }
.result-item { background: var(--surface); border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem; border-left: 4px solid var(--accent3); box-shadow: var(--shadow); }
.result-golongan { font-family: var(--font-mono); font-weight: 700; color: var(--accent3); }
.tag { display: inline-block; background: #e0f2fe; border: 1px solid #bae6fd; color: #0369a1; font-size: 0.78rem; padding: 0.25rem 0.7rem; border-radius: 999px; margin: 0.2rem; }
</style>""", unsafe_allow_html=True)

# ─── 3. DATABASE ORGANIK ────────────────────────────────────────────────────
SENYAWA_DB = [
    {"Nama": "Etanol", "Rumus": "C₂H₅OH", "Golongan": "Alkohol", "Uji Positif": "Esterifikasi, Iodoform"},
    {"Nama": "Aseton", "Rumus": "CH₃COCH₃", "Golongan": "Keton", "Uji Positif": "2,4-DNPH"},
    {"Nama": "Formaldehid", "Rumus": "HCHO", "Golongan": "Aldehid", "Uji Positif": "Tollens, Fehling"},
    {"Nama": "Asam Asetat", "Rumus": "CH₃COOH", "Golongan": "Asam Karboksilat", "Uji Positif": "Lakmus, Esterifikasi"},
    {"Nama": "Fenol", "Rumus": "C₆H₅OH", "Golongan": "Fenol", "Uji Positif": "FeCl₃ (ungu)"},
    {"Nama": "Glukosa", "Rumus": "C₆H₁₂O₆", "Golongan": "Karbohidrat", "Uji Positif": "Tollens, Fehling, Molisch"},
    {"Nama": "Albumin", "Rumus": "Protein", "Golongan": "Protein", "Uji Positif": "Biuret, Ninhidrin"},
]

def identifikasi_senyawa(jawaban: dict) -> list:
    kandidat = []
    if jawaban.get("tollens") == "Ya" and jawaban.get("fehling") == "Ya": kandidat.append(("Aldehid / Gula Pereduksi", "Tollens ✅ + Fehling ✅"))
    if jawaban.get("iodoform") == "Ya": kandidat.append(("Metil Keton / Alkohol Sekunder", "Iodoform ✅"))
    if jawaban.get("fecl3") == "Ya": kandidat.append(("Fenol", "FeCl₃ ✅"))
    if jawaban.get("biuret") == "Ya": kandidat.append(("Protein", "Biuret ✅"))
    if jawaban.get("molisch") == "Ya": kandidat.append(("Karbohidrat", "Molisch ✅"))
    if not kandidat: kandidat.append(("Tidak Teridentifikasi", "Kombinasi hasil uji tidak spesifik."))
    return kandidat

# ─── 4. DATABASE & FUNGSI METATESIS ─────────────────────────────────────────
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
    hasil_a = anion if indeks_a == 1 else (f"({anion}){indeks_a}" if is_poliatomik_a else f"{anion}{indeks_a}")
    senyawa_baru = f"{hasil_k}{hasil_a}"
    return "H2O" if senyawa_baru == "HOH" else senyawa_baru

def apakah_mengendap(kation, anion):
    if kation == 'H' and anion in ['OH', 'O']: return False
    if kation in ['Na', 'K', 'NH4', 'Li', 'Rb', 'Cs']: return False
    if anion in ['NO3', 'CH3COO']: return False
    if anion in ['Cl', 'Br', 'I']: return True if kation in ['Ag', 'Pb', 'Hg'] else False
    if anion == 'SO4': return True if kation in ['Ba', 'Ca', 'Sr', 'Pb'] else False
    if anion == 'OH': return False if kation in ['Ca', 'Sr', 'Ba'] else True
    if anion in ['CO3', 'PO4', 'CrO4', 'S', 'O']: return True
    return False

def fmt_muatan(nilai, tanda):
    return tanda if nilai == 1 else f"{nilai}{tanda}"

# ─── 5. PENGATURAN STATE & NAVIGASI ─────────────────────────────────────────
if "app_mode" not in st.session_state: st.session_state.app_mode = "portal"
if "halaman_org" not in st.session_state: st.session_state.halaman_org = "landing"

def go_portal(): st.session_state.app_mode = "portal"; st.rerun()
def nav_org(page): st.session_state.halaman_org = page; st.session_state.app_mode = "organik"; st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
#  A. PORTAL UTAMA (TIM PENGEMBANG DIPINDAHKAN KE SINI)
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.app_mode == "portal":
    st.markdown("""
    <div class="landing-hero">
        <div class="hero-badge">Aplikasi Pendidikan Interaktif</div>
        <h1 class="hero-title">Portal Analisis <span class="hero-accent">Kimia Terpadu</span></h1>
        <p class="hero-desc">Pilih modul simulasi laboratorium virtual yang ingin Anda akses di bawah ini.</p>
    </div>
    
    <div class="team-banner">
        <h4>👨‍🔬 Tim Pengembang Aplikasi (D3 Analisis Kimia - AKA Bogor)</h4>
        <p>✨ Agung Nugraha (NIM: 2560557) &nbsp; | &nbsp; ✨ Alifia Citra Nabila &nbsp; | &nbsp; ✨ Haifa Maulafida<br>✨ Nabila Putri Khorinnisa &nbsp; | &nbsp; ✨ Rania Ayudia</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 4, 4, 1])
    with col2:
        st.markdown('<div class="portal-card"><h1>🔬</h1><h3>Identifikasi Organik</h3><p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">Analisis kualitatif berdasarkan pengujian pereaksi untuk identifikasi golongan organik.</p>', unsafe_allow_html=True)
        if st.button("Masuk Modul Organik ➔", use_container_width=True, type="primary"):
            st.session_state.halaman_org = "landing"; st.session_state.app_mode = "organik"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="portal-card"><h1>⚗️</h1><h3>Reaksi Metatesis</h3><p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">Prediksi produk reaksi pertukaran ganda dan penyetaraan persamaan kimia otomatis.</p>', unsafe_allow_html=True)
        if st.button("Masuk Modul Metatesis ➔", use_container_width=True, type="primary"):
            st.session_state.app_mode = "metatesis"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
#  B. MODUL: IDENTIFIKASI SENYAWA ORGANIK
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.app_mode == "organik":
    if st.session_state.halaman_org == "landing":
        st.button("🏠 Kembali ke Portal Utama", on_click=go_portal)
        st.markdown('<div class="landing-hero" style="padding-top:1rem;"><div class="hero-badge">⚗️ Kimia Organik</div><h1 class="hero-title">Sistem Identifikasi<br><span class="hero-accent">Senyawa Organik</span></h1></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔬 Mulai Identifikasi", use_container_width=True, type="primary"): nav_org("identifikasi")
        with col2:
            if st.button("🗄️ Database Senyawa", use_container_width=True): nav_org("database")

    elif st.session_state.halaman_org == "identifikasi":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🔬 Form Identifikasi</h2>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        jawaban = {
            "tollens": st.radio("Cermin perak (Tollens)?", ["Ya", "Tidak"], horizontal=True),
            "iodoform": st.radio("Endapan kuning (Iodoform)?", ["Ya", "Tidak"], horizontal=True),
            "fecl3": st.radio("Warna ungu (FeCl₃)?", ["Ya", "Tidak"], horizontal=True),
        }
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("🔎 Identifikasi!", type="primary"):
            st.write(identifikasi_senyawa(jawaban))

    elif st.session_state.halaman_org == "database":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🗄️ Database Senyawa</h2>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(SENYAWA_DB), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════════
#  C. MODUL: REAKSI METATESIS (DENGAN 3 REAKTAN)
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.app_mode == "metatesis":
    st.button("🏠 Kembali ke Portal Utama", on_click=go_portal)
    st.markdown('<h1 class="page-title">🧪 Analisis Stoikiometri & Metatesis</h1>', unsafe_allow_html=True)
    st.markdown("Sistem mendeteksi muatan ion secara otomatis untuk menyilangkan produk reaktan secara instan.")
    st.divider()

    st.markdown("#### 📥 Masukkan Senyawa Reaktan (Maksimal 3)")
    col1, col2, col3 = st.columns(3)
    with col1: reaktan1 = st.text_input("Reaktan 1", "NaOH").strip().replace(" ", "")
    with col2: reaktan2 = st.text_input("Reaktan 2", "HCl").strip().replace(" ", "")
    with col3: reaktan3 = st.text_input("Reaktan 3 (Opsional)", "").strip().replace(" ", "")

    if st.button("Analisis Reaksi", type="primary"):
        input_raw = [r for r in [reaktan1, reaktan2, reaktan3] if r]
        
        if len(input_raw) < 2:
            st.warning("⚠️ Minimal masukkan 2 reaktan untuk melakukan reaksi silang.")
        elif "H2O" in input_raw:
            st.warning("⚠️ Reaktan H₂O memicu pelarutan fisik, bukan metatesis murni.")
        else:
            # Urai semua reaktan yang diinput
            parsed_reactants = [urai_senyawa(r) for r in input_raw]
            
            if not all(k and a for k, a in parsed_reactants):
                st.error("❌ Salah satu senyawa tidak dikenali. Pastikan kaidah penulisan huruf kapital sudah benar.")
            else:
                kations = [p[0] for p in parsed_reactants]
                anions = [p[1] for p in parsed_reactants]
                
                # Buat semua kemungkinan produk silang
                produk_kemungkinan = set()
                for i, k in enumerate(kations):
                    for j, a in enumerate(anions):
                        if i != j:  # Jangan gabungkan kation dan anion dari reaktan yang sama
                            produk_kemungkinan.add(gabung_ion(k, a))
                
                try:
                    # Penyetaraan menggunakan ChemPy
                    r_setara, p_setara = balance_stoichiometry(set(input_raw), produk_kemungkinan)
                    
                    # Format string reaksi
                    def format_dict(senyawa_dict):
                        hasil = []
                        for seny, koef in senyawa_dict.items():
                            k, a = urai_senyawa(seny)
                            wujud = "(l)" if seny == "H2O" else ("(s)" if (k and a and apakah_mengendap(k, a)) else "(aq)")
                            prefix = "" if koef == 1 else f"{koef}"
                            hasil.append(f"{prefix}{seny}{wujud}")
                        return " + ".join(hasil)
                    
                    kiri = format_dict(r_setara)
                    kanan = format_dict(p_setara)
                    
                    # Cek Driving Force pada produk yang BENAR-BENAR terbentuk
                    alasan = []
                    for p in p_setara.keys():
                        if p == "H2O": 
                            alasan.append(f"**molekul air (H₂O)** (elektrolit lemah)")
                        else:
                            kp, ap = urai_senyawa(p)
                            if kp and ap and apakah_mengendap(kp, ap):
                                alasan.append(f"endapan **{p}**")
                                
                    st.success("✅ Secara Teori: REAKSI BERLANGSUNG (Valid)")
                    st.markdown("### Persamaan Reaksi Setara:")
                    st.latex(f"{kiri} \\rightarrow {kanan}")
                    
                    if alasan:
                        st.markdown(f"**Driving Force:** Reaksi dapat berlangsung ke arah produk karena terbentuk {', '.join(alasan)}.")
                    else:
                        st.info("ℹ️ Tidak ada endapan atau air yang terbentuk. Dalam dunia nyata, semua ion mungkin hanya bercampur dalam larutan (reaksi tidak berkesudahan).")
                    
                    st.divider()
                    
                    # --- Lembar Kerja Analisis ---
                    st.markdown("### 🔍 Lembar Kerja Analisis Ion")
                    cols_urai = st.columns(len(input_raw))
                    
                    # Tampilkan Penguraian (Dinamis 2 atau 3 kolom)
                    for idx, (k, a) in enumerate(parsed_reactants):
                        c_k, c_a = fmt_muatan(kation_db[k][0], '+'), fmt_muatan(abs(anion_db[a][0]), '-')
                        with cols_urai[idx]:
                            st.markdown(f"**Penguraian Reaktan {idx+1}:**")
                            st.latex(f"{input_raw[idx]} \\longrightarrow {k}^{{{c_k}}} + {a}^{{{c_a}}}")
                            
                    st.info("💡 **Aturan Silang Muatan:** Kation (positif) dari satu reaktan bertukar pasangan dengan Anion (negatif) dari reaktan lain membentuk senyawa baru: $A^{x+} + B^{y-} \\rightarrow A_yB_x$")
                    
                    # Tampilkan Pembentukan Produk yang berhasil disetarakan
                    cols_prod = st.columns(len(p_setara))
                    for idx, p in enumerate(p_setara.keys()):
                        k_p, a_p = urai_senyawa(p)
                        if k_p and a_p:
                            c_k = fmt_muatan(kation_db[k_p][0], '+')
                            c_a = fmt_muatan(abs(anion_db[a_p][0]), '-')
                            with cols_prod[idx % len(cols_prod)]:
                                st.markdown(f"**Silang Produk {idx+1}:**")
                                st.latex(f"{k_p}^{{{c_k}}} + {a_p}^{{{c_a}}} \\longrightarrow {p}")
                                
                except Exception as e:
                    st.error("❌ Reaksi silang tidak dapat disetarakan secara matematis. Kombinasi ion antar reaktan mungkin tidak menghasilkan set produk yang valid secara persamaan kimia.")
