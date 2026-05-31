import streamlit as st
import math
from chempy import balance_stoichiometry

# --- 1. CONFIGURASI HALAMAN & TEMA ---
st.set_page_config(page_title="Chemical Metathesis Engine", page_icon="🧪", layout="centered")

# Custom CSS untuk membuat layout judul dan identitas kelompok terlihat modern & simpel
st.markdown("""
    <style>
    .hero-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #1E3A8A; /* Warna Navy Blue */
        text-align: center;
        margin-top: -20px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #4B5563; /* Warna Abu-abu */
        text-align: center;
        margin-bottom: 25px;
    }
    .team-container {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 35px;
        border-top: 4px solid #3B82F6; /* Accent Blue */
    }
    .team-title {
        font-size: 13px;
        font-weight: bold;
        color: #1E3A8A;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
        text-align: center;
    }
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 10px;
        justify-content: center;
    }
    .team-card {
        background: #FFFFFF;
        padding: 10px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        font-size: 14px;
        color: #1F2937;
        font-weight: 500;
    }
    .team-card-highlight {
        background: #EFF6FF;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #BFDBFE;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        font-size: 14px;
        color: #1E3A8A;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. OPENING / HERO SECTION ---
st.markdown('<div class="hero-title">🧪 Engine Reaksi Metatesis</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Sistem Prediksi Produk, Penyetaraan Stoikiometri, dan Verifikasi Teori Kelarutan Akurat</div>', unsafe_allow_html=True)

# --- 3. DISPLAY KARTU ANGGOTA KELOMPOK ---
st.markdown("""
    <div class="team-container">
        <div class="team-title">👥 Kelompok Pengembang</div>
        <div class="team-grid">
            <div class="team-card-highlight">Agung Nugraha<br><span style="font-size:11px; font-weight:normal; color:#6B7280;">NIM 2560557</span></div>
            <div class="team-card">Alifia Citra Nabila</div>
            <div class="team-card">Haifa Maulafida</div>
            <div class="team-card">Nabila Putri Khorinnisa</div>
            <div class="team-card">Rania Ayudia</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. DATABASE ION SUPER LENGKAP ---
kation_db = {
    'H': (1, False), 'Li': (1, False), 'Na': (1, False), 'K': (1, False), 'Rb': (1, False), 'Cs': (1, False),
    'Be': (2, False), 'Mg': (2, False), 'Ca': (2, False), 'Sr': (2, False), 'Ba': (2, False),
    'Ag': (1, False), 'Zn': (2, False), 'Cd': (2, False), 'Al': (3, False), 'Bi': (3, False),
    'Cu': (2, False), 'Fe': (3, False), 'Pb': (2, False), 'Ni': (2, False), 'Co': (2, False), 
    'Mn': (2, False), 'Cr': (3, False), 'Sn': (2, False), 'Hg': (2, False),
    'NH4': (1, True)
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

# --- 5. LOGIKA KIMIA & ATURAN KELARUTAN ---
def urai_senyawa(senyawa):
    kation_terdeteksi = None
    anion_terdeteksi = None
    
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
    muatan_k = abs(kation_db[kation][0])
    muatan_a = abs(anion_db[anion][0])
    is_poliatomik_a = anion_db[anion][1]
    
    kpk = (muatan_k * muatan_a) // math.gcd(muatan_k, muatan_a)
    indeks_k = kpk // muatan_k
    indeks_a = kpk // muatan_a
    
    hasil_k = kation if indeks_k == 1 else f"{kation}{indeks_k}"
    if indeks_a == 1:
        hasil_a = anion
    else:
        hasil_a = f"({anion}){indeks_a}" if is_poliatomik_a else f"{anion}{indeks_a}"
        
    return f"{hasil_k}{hasil_a}"

def apakah_mengendap(kation, anion):
    if kation in ['Na', 'K', 'NH4', 'Li', 'Rb', 'Cs']:
        return False
    if anion in ['NO3', 'CH3COO']:
        return False
    if anion in ['Cl', 'Br', 'I']:
        return True if kation in ['Ag', 'Pb', 'Hg'] else False
    if anion == 'SO4':
        return True if kation in ['Ba', 'Ca', 'Sr', 'Pb'] else False
    if anion == 'OH':
        return False if kation in ['Ca', 'Sr', 'Ba'] else True
    if anion in ['CO3', 'PO4', 'CrO4', 'S', 'O']:
        return True
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

# --- 6. MENU UTAMA INPUT & ANALISIS ---
st.subheader("📝 Menu Analisis Stoikiometri")
st.markdown("Silakan masukkan reaktan yang akan direaksikan di bawah ini:")

col1, col2 = st.columns(2)
with col1:
    reaktan1 = st.text_input("Reaktan 1", "AgNO3").strip()
with col2:
    reaktan2 = st.text_input("Reaktan 2", "BaCl2").strip()

if st.button("Analisis Reaksi", type="primary"):
    if reaktan1 == "H2O" or reaktan2 == "H2O":
        st.warning("⚠️ **Analisis Teori:** Salah satu reaktan adalah air ($H_2O$). Pencampuran garam dengan air hanya memicu proses pelarutan fisik (disosiasi ion), bukan reaksi metatesis kimia antar dua senyawa.")
    else:
        k1, a1 = urai_senyawa(reaktan1)
        k2, a2 = urai_senyawa(reaktan2)
        
        if not (k1 and a1 and k2 and a2):
            st.error("❌ Senyawa tidak dikenali. Pastikan penulisan huruf besar/kecil benar (Contoh: NaCl, bukan nacl atau Nacl).")
        else:
            produk1 = gabung_ion(k1, a2)
            produk2 = gabung_ion(k2, a1)
            
            mengendap_p1 = apakah_mengendap(k1, a2)
            mengendap_p2 = apakah_mengendap(k2, a1)
            
            try:
                r_setara, p_setara = balance_stoichiometry({reaktan1, reaktan2}, {produk1, produk2})
                kiri = format_reaksi_str(r_setara)
                kanan = format_reaksi_str(p_setara)
                
                if not mengendap_p1 and not mengendap_p2:
                    st.error("❌ Secara Teori: TIDAK TERJADI REAKSI (No Reaction)")
                    st.latex(f"{reaktan1}(aq) + {reaktan2}(aq) \\rightarrow \\text{{Tidak Bereaksi}}")
                    st.info(f"""
                    **Penjelasan Ilmiah:** Sistem mendeteksi produk yang terbentuk berpotensi menjadi **{produk1}** dan **{produk2}**. 
                    Namun, berdasarkan *Aturan Kelarutan*, kedua senyawa tersebut **sangat larut dalam air (Aqueous)**. 
                    Di dalam gelas kimia, ion-ion hanya akan saling bercampur dan tetap melayang secara bebas tanpa membentuk endapan, gas, atau molekul air baru.
                    """)
                else:
                    st.success("✅ Secara Teori: REAKSI BERLANGSUNG (Valid)")
                    st.subheader("Persamaan Reaksi Setara:")
                    st.latex(f"{kiri} \\rightarrow {kanan}")
                    
                    endapan = []
                    if mengendap_p1: endapan.append(f"**{produk1}**")
                    if mengendap_p2: endapan.append(f"**{produk2}**")
                    
                    st.markdown(f"**Driving Force:** Reaksi dapat berjalan karena terbentuk endapan padat berupa {', '.join(endapan)} di dalam larutan.")
                
                st.divider()
                st.markdown("### 🔍 Lembar Kerja Analisis Ion")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Kation & Anion Reaktan 1:**\n- ${k1}^{{{kation_db[k1][0]}+}}$\n- ${a1}^{{{anion_db[a1][0]}-}}$")
                with col_b:
                    st.markdown(f"**Kation & Anion Reaktan 2:**\n- ${k2}^{{{kation_db[k2][0]}+}}$\n- ${a2}^{{{anion_db[a2][0]}-}}$")

            except Exception as e:
                st.error(f"❌ Reaksi tidak dapat disetarakan secara matematis stoikiometri.")

st.divider()
st.caption("D3 Analisis Kimia, Politeknik AKA Bogor")
