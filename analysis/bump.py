
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_bump(df):
    if df is not None and not df.empty:
    
        # Filter records with "bump" label
        bump_df = df[df['label'] == 'bump']

        # Add a severity column based on x, y, z values
        def classify_severity(row):
            total = row['y']
            if 5 <= total < 7:
                return "Less"
            elif 7 <= total <8:
                return "Mild"
            else:
                return "Severe"

        bump_df['Severity'] = bump_df.apply(classify_severity, axis=1)

        # Streamlit app
        st.title("Bump Severity Analysis")

        # Section 1: Filtered Bump Records
        st.header("1. Filtered Bump Records")
        st.dataframe(bump_df.head())

        # Section 2: Severity Distribution
        st.header("2. Severity Distribution")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x='Severity', data=bump_df, palette="pastel", order=["Less", "Mild", "Severe"])
        plt.title("Bump Severity Levels")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        st.pyplot(fig)

        # Completion Message
        st.success("Severity analysis completed successfully!")
