import streamlit as st
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from stmol import showmol
import py3Dmol

# ==========================================
# Page Configuration & Styling
# ==========================================
st.set_page_config(page_title="NiVacDB", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; }
    .stAlert { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Data Loader
# ==========================================
@st.cache_data
def load_literature_data():
    # Reads directly from your generated Excel file
    return pd.read_excel("NipahVaxDB_Data.xlsx", sheet_name="Literature DB")

# ==========================================
# Sidebar Navigation
# ==========================================
with st.sidebar:
    st.title("🧬 NiVacDB")
    st.markdown("---")
    menu = ["Dashboard", "In Silico Workbench", "Literature DB", "Preclinical Data", "Clinical Trials"]
    choice = st.radio("Navigation", menu)
    
    st.markdown("---")
    st.caption("Researcher Access | Session Active")

# ==========================================
# View 1: Dashboard
# ==========================================
if choice == "Dashboard":
    st.header("Dashboard")
    st.markdown("Nipah Virus Vaccine Research Overview")
    
    # --- CUSTOM CSS FOR METRIC CARDS ---
    st.markdown("""
        <style>
        .dash-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            position: relative;
            margin-bottom: 2rem;
            margin-top: 1rem;
        }
        .dash-title {
            color: #64748b;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .dash-value {
            font-size: 2.25rem;
            font-weight: 700;
            color: #0f172a;
            margin-top: 0.5rem;
        }
        .dash-subtext {
            font-size: 0.75rem;
            margin-top: 1rem;
        }
        .dash-icon {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            font-size: 1.5rem;
            background-color: #f8fafc;
            border-radius: 0.5rem;
            padding: 0.25rem 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- 4 METRIC BOXES ---
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">My Constructs</div>
            <div class="dash-value">1</div>
            <div class="dash-subtext" style="color: #10b981;">↗ 1 New this week</div>
            <div class="dash-icon">🧪</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Lit. Candidates</div>
            <div class="dash-value">31</div>
            <div class="dash-subtext" style="color: #64748b;">Database updated 2h ago</div>
            <div class="dash-icon">📚</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Active Trials</div>
            <div class="dash-value">4</div>
            <div class="dash-subtext" style="color: #64748b;">Phase 1 & 2</div>
            <div class="dash-icon">🏥</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Epitopes Mapped</div>
            <div class="dash-value">31</div>
            <div class="dash-subtext" style="color: #64748b;">B-cell & T-cell</div>
            <div class="dash-icon">🧬</div>
        </div>
        """, unsafe_allow_html=True)

    # --- EXISTING SCHEMATIC & DETAILS SECTION ---
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Construct Schematic")
        try:
            st.image("construct.png", caption="NiV Chimeric Vaccine Construct")
        except Exception:
            st.warning("To display your schematic, save your image as 'construct.png' in the same folder as app.py")
        
        st.divider()
        st.subheader("Construct Analysis & 3D Structure")
        
        # Create tabs for organization
        tab_3d, tab_pdb, tab_data = st.tabs(["🧬 3D Viewer", "📂 Upload PDB", "📊 Upload Data"])
        
        # Initialize session state for custom PDB uploads
        if "custom_pdb_data" not in st.session_state:
            st.session_state.custom_pdb_data = None
            st.session_state.custom_pdb_name = "Multiepitope-vaccine-construct.pdb"

        # --- TAB 1: 3D Viewer & Controls ---
        with tab_3d:
            pdb_data = None
            if st.session_state.custom_pdb_data is not None:
                pdb_data = st.session_state.custom_pdb_data
            else:
                try:
                    with open("Multiepitope-vaccine-construct.pdb", "r") as f:
                        pdb_data = f.read()
                except FileNotFoundError:
                    pass
            
            if pdb_data:
                render_col1, render_col2 = st.columns(2)
                with render_col1:
                    show_surface = st.toggle("Show Surface", value=False)
                with render_col2:
                    color_style = st.selectbox("Color Style", ["spectrum", "chain", "secondary structure"], label_visibility="collapsed")
                
                st.divider()
                
                viewer = py3Dmol.view(width=400, height=400)
                viewer.addModel(pdb_data, "pdb")
                
                if color_style == "spectrum":
                    viewer.setStyle({'cartoon': {'color': 'spectrum'}})
                elif color_style == "chain":
                    viewer.setStyle({'cartoon': {'colorscheme': 'chain'}})
                else:
                    viewer.setStyle({'cartoon': {'colorscheme': 'ssPyMOL'}})
                
                if show_surface:
                    viewer.addSurface(py3Dmol.VDW, {'opacity': 0.6, 'color': 'white'})
                
                viewer.zoomTo()
                showmol(viewer, height=400, width=400)
                
                st.caption("Interactive 3D model. Scroll to zoom, click and drag to rotate.")
                st.divider()
                
                st.download_button(
                    label="⬇️ Download PDB Model",
                    data=pdb_data,
                    file_name=st.session_state.custom_pdb_name,
                    mime="chemical/x-pdb",
                    use_container_width=True
                )
            else:
                st.info("💡 Place your 'Multiepitope-vaccine-construct.pdb' in the project folder, or upload a new one in the next tab.")

        # --- TAB 2: Upload More PDB Constructs ---
        with tab_pdb:
            st.markdown("**Upload a new 3D Model**")
            st.divider()
            uploaded_pdb = st.file_uploader("Choose a PDB file to view", type=["pdb"])
            
            if uploaded_pdb is not None:
                st.session_state.custom_pdb_data = uploaded_pdb.getvalue().decode("utf-8")
                st.session_state.custom_pdb_name = uploaded_pdb.name
                st.success(f"✅ Loaded {uploaded_pdb.name}! Switch back to the '3D Viewer' tab to see it.")
                
            if st.session_state.custom_pdb_data is not None:
                st.divider()
                if st.button("Reset to Default PDB", use_container_width=True):
                    st.session_state.custom_pdb_data = None
                    st.rerun()

        # --- TAB 3: Upload Epitopes & Properties ---
        with tab_data:
            st.markdown("**Upload Construct Metadata**")
            st.divider()
            uploaded_seq = st.file_uploader("Upload Sequences (FASTA/TXT)", type=["fasta", "txt"])
            if uploaded_seq:
                st.success("Sequence uploaded successfully.")
                
            st.divider()
            uploaded_epi = st.file_uploader("Upload Epitopes/Properties (Excel/CSV)", type=["xlsx", "csv"])
            if uploaded_epi:
                st.success("Epitope properties loaded successfully.")

    with col2:
        st.subheader("Construct Details: NiV-Multi-Epitope")
        st.write("**Target:** Nipah Virus")
        st.write("**Sequence:**")
        
        full_sequence = (
            "GIINTLQKYYCRVRGGRCAVLSCLPKEEQIGKCSTRGRKCCRRKK" 
            "EAAAK"                                         
            "ADDSSRDVIKAAYADQLEFEDEAAYADQLEFEDEFAAYADRQRPGTPPAAYADRQRPGTPM" 
            "AAYAENVQLNASTAVKETGPGPGALYEAMKNADNINKLGPGPGAQITAGVALYEAMKNGPGPGAQPPYHWSIERSISPGPGPGASQFVPMMADDSSRDVGPGPG" 
            "SETSREKDHRESRSTKKNTVDKLSLSLGLIKKCRTANPKLECYSSKKKSTEPRYSNPDSTKK" 
            "HHHHHH"                                        
        )
        st.code(full_sequence, language="text")
        
        st.write("**Construct Components:**")
        
        epitope_data = pd.DataFrame({
            "Component": [
                "Adjuvant", 
                "MHC-I Epitope 1", "MHC-I Epitope 2", "MHC-I Epitope 3", "MHC-I Epitope 4", "MHC-I Epitope 5",
                "MHC-II Epitope 1", "MHC-II Epitope 2", "MHC-II Epitope 3", "MHC-II Epitope 4", "MHC-II Epitope 5",
                "B-cell Epitope 1", "B-cell Epitope 2", "B-cell Epitope 3", "B-cell Epitope 4",
                "His-tag"
            ],
            "Sequence": [
                "GIINTLQKYYCRVRGGRCAVLSCLPKEEQIGKCSTRGRKCCRRKK",
                "ADDSSRDVIK", "ADQLEFEDE", "ADQLEFEDEF", "ADRQRPGTP", "ADRQRPGTPM",
                "AENVQLNASTAVKET", "ALYEAMKNADNINKL", "AQITAGVALYEAMKN", "AQPPYHWSIERSISP", "ASQFVPMADDSSRDV",
                "SETSREKDHRESRST", "NTVDKLSLSLGLI", "CRTANPKLECYSS", "KSTEPRYSNPDST",
                "HHHHHH"
            ],
            "Type": [
                "TLR Agonist", 
                "CD8+ T-cell", "CD8+ T-cell", "CD8+ T-cell", "CD8+ T-cell", "CD8+ T-cell",
                "CD4+ T-cell", "CD4+ T-cell", "CD4+ T-cell", "CD4+ T-cell", "CD4+ T-cell",
                "Linear B-cell", "Linear B-cell", "Linear B-cell", "Linear B-cell",
                "Purification Tag"
            ],
            "Preceding Linker": [
                "None", 
                "EAAAK", "AAY", "AAY", "AAY", "AAY",
                "AAY", "GPGPG", "GPGPG", "GPGPG", "GPGPG",
                "GPGPG", "KK", "KK", "KK",
                "KK"
            ]
        })
        
        st.dataframe(epitope_data, hide_index=True)

# ==========================================
# View 2: In Silico Workbench
# ==========================================
elif choice == "In Silico Workbench":
    st.header("In Silico Workbench")
    st.markdown("Evaluate physicochemical properties, allergenicity, and toxicity of your designed vaccine constructs.")
    
    sequence = st.text_area("Input Peptide/Protein Sequence (FASTA or plain text):", height=150, 
                            placeholder="Paste your amino acid sequence here...")
    
    if st.button("Analyze Construct", type="primary"):
        if sequence:
            seq_clean = "".join(sequence.split()).upper()
            
            try:
                analysis = ProteinAnalysis(seq_clean)
                mw = analysis.molecular_weight()
                pi = analysis.isoelectric_point()
                instability = analysis.instability_index()
                gravy = analysis.gravy()
                
                st.subheader("Physicochemical Properties")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Molecular Weight", f"{mw/1000:.2f} kDa")
                col2.metric("Isoelectric Point (pI)", f"{pi:.2f}")
                
                if instability < 40:
                    col3.metric("Instability Index", f"{instability:.2f}", "Stable", delta_color="normal")
                else:
                    col3.metric("Instability Index", f"{instability:.2f}", "Unstable", delta_color="inverse")
                    
                col4.metric("GRAVY", f"{gravy:.3f}")
                
                st.divider()
                
                st.subheader("Safety Profile Validation")
                safety_col1, safety_col2 = st.columns(2)
                
                with safety_col1:
                    st.info("🧬 **Allergenicity Prediction**\n\n*Simulated Result:* Non-Allergen.")
                    
                with safety_col2:
                    st.success("🧪 **Toxicity Prediction**\n\n*Simulated Result:* Non-Toxic.")
                    
            except Exception as e:
                st.error("Invalid sequence input. Please ensure only standard amino acid letters are used.")
        else:
            st.warning("Please enter a sequence to analyze.")

# ==========================================
# View 3: Literature DB
# ==========================================
elif choice == "Literature DB":
    st.header("Literature Repository")
    st.markdown("Comprehensive database of Nipah virus potential vaccine candidates from literature.")
    
    df = load_literature_data()
    
    search_term = st.text_input("Search Constructs or Targets:", "")
    if search_term:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False).any(), axis=1)]
        
    st.dataframe(
        df, 
        hide_index=True,
        column_config={
            "Reference Link": st.column_config.LinkColumn(
                "Reference Link",
                display_text="View Source 🔗" 
            )
        }
    )
    
    st.subheader("Database Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Candidates", len(load_literature_data()))
    m2.metric("In Active Trials", len(load_literature_data()[load_literature_data()["Dev Stage"].str.contains("Clinical")]))
    m3.metric("Epitope Profiles Mapped", len(load_literature_data()["Key Epitopes / Components"].dropna()))

# ==========================================
# View 4: Preclinical Data
# ==========================================
elif choice == "Preclinical Data":
    st.header("Preclinical Data")
    st.markdown("Efficacy studies in animal models (Mice, Hamster, Ferret, AGM).")
    
    st.info("Visualization of survival curves and immunogenicity.")
    
    st.subheader("Neutralizing Antibody Titers")
    chart_data = pd.DataFrame({
        "Dose": ["10µg", "50µg", "100µg"],
        "Titer": [640, 1280, 2560]
    }).set_index("Dose")
    
    st.bar_chart(chart_data)

# ==========================================
# View 5: Clinical Trials
# ==========================================
elif choice == "Clinical Trials":
    st.header("Clinical Trials")
    st.markdown("Current status of human trials for Nipah Virus vaccines based on literature and registry data.")
    
    df = load_literature_data()
    clinical_df = df[df["Dev Stage"].str.contains("Clinical")]
    
    for index, row in clinical_df.iterrows():
        with st.expander(f"{row['Construct Name']} - {row['Dev Stage']}", expanded=True):
            st.write(f"**Type:** {row['Type']}")
            st.write(f"**Target Antigen:** {row['Target Antigen']}")
            if "Developer / Reference" in row:
                st.write(f"**Sponsor/Developer:** {row['Developer / Reference']}")
            if "Reference Link" in row:
                st.markdown(f"**Link:** [Clinical Registry]({row['Reference Link']})")