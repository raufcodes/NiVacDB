import pandas as pd

# Data for Literature DB
data_literature = {
    "Construct Name": ["ChAdOx1 NipahB", "mRNA-1215", "HeV-sG-V", "PHV02", "Gennova saRNA", "Multiepitope Constructs"],
    "Type": ["Viral Vector (Adenovirus)", "mRNA (LNP)", "Protein Subunit", "Viral Vector (rVSV)", "Self-amplifying mRNA", "Peptides"],
    "Target Antigen": ["NiV-G (Bangladesh strain)", "NiV-F / NiV-G", "Hendra-G (Soluble)", "NiV-G + Ebola GP", "NiV-G", "NiV-G / NiV-F"],
    "Key Epitopes / Components": ["Full-length G-glycoprotein", "Pre-fusion F and G glycoproteins", "Soluble G-protein tetramer", "Live attenuated rVSV expressing NiV-G", "saRNA platform", "In silico CTL, HTL, LBL epitopes"],
    "Dev Stage": ["Clinical Phase 2", "Clinical Phase 1", "Clinical Phase 1", "Clinical Phase 1", "Preclinical", "In Silico / Preclinical"],
    "Developer / Reference": ["University of Oxford / CEPI", "Moderna / NIH", "Auro Vaccines", "Public Health Vaccines", "Gennova Biopharmaceuticals", "Various academic publications"]
}

# Data for Preclinical Data
data_preclinical = {
    "Vaccine Candidate": ["ChAdOx1 NipahB", "mRNA-1215", "HeV-sG-V", "PHV02", "Multiepitope Constructs"],
    "Animal Model": ["Syrian Hamster", "African Green Monkey", "Ferret & AGM", "Syrian Hamster", "In Silico / Mice"],
    "Challenge Strain": ["NiV-B", "NiV-M / NiV-B", "NiV & HeV", "NiV-B", "N/A"],
    "Efficacy / Survival %": ["100%", "100%", "100%", "100%", "N/A"],
    "Immunogenicity & Notes": ["Single dose induced robust neutralizing antibodies.", "Elicited high neutralizing antibody titers.", "Demonstrated cross-protective immunity >12 months.", "Rapid onset of immunity; single-dose protection.", "Predicted 97.94% HLA population coverage."]
}

# Data for Clinical Trials
data_clinical = {
    "Trial Name / ID": ["Oxford/CEPI Phase 2", "Oxford Phase 1", "Moderna Phase 1", "Auro Vaccines Phase 1", "PHV02 Phase 1"],
    "Candidate": ["ChAdOx1 NipahB", "ChAdOx1 NipahB", "mRNA-1215", "HeV-sG-V", "PHV02 (rVSV)"],
    "Sponsor": ["Univ. of Oxford / CEPI", "Univ. of Oxford / OVG", "Moderna / NIH", "Auro Vaccines / CEPI", "Public Health Vaccines"],
    "Phase": ["Phase 2", "Phase 1", "Phase 1", "Phase 1", "Phase 1"],
    "Location": ["Bangladesh (icddr,b)", "United Kingdom", "USA", "USA / Australia", "USA"],
    "Status": ["Launched Dec 2025", "Launched Jan 2024", "Ongoing", "Completed", "Ongoing"],
    "Participants": ["306", "51", "Dose-escalation", "Dose-dependent cohort", "Safety cohort"]
}

# Convert dictionaries to pandas DataFrames
df_lit = pd.DataFrame(data_literature)
df_preclin = pd.DataFrame(data_preclinical)
df_clin = pd.DataFrame(data_clinical)

# Export to an Excel file with multiple sheets
file_name = "NipahVaxDB_Data.xlsx"
with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    df_lit.to_excel(writer, sheet_name='Literature DB', index=False)
    df_preclin.to_excel(writer, sheet_name='Preclinical Data', index=False)
    df_clin.to_excel(writer, sheet_name='Clinical Trials', index=False)
    
    # Auto-adjust column widths for better readability
    for sheet_name, df in zip(['Literature DB', 'Preclinical Data', 'Clinical Trials'], [df_lit, df_preclin, df_clin]):
        worksheet = writer.sheets[sheet_name]
        for idx, col in enumerate(df):
            max_len = max(df[col].astype(str).map(len).max(), len(str(col))) + 2
            worksheet.set_column(idx, idx, max_len)

print(f"Successfully generated {file_name}!")