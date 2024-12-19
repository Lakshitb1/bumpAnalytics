
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_pothole(df):
    if df is not None and not df.empty:
    
        # Filter records with "pothole" label
        pothole_df = df[df['label'] == 'pothole']

        # Add a severity column based on x, y, z values
        def classify_severity(row):
            total = row['y']
            if 0 < total <= -2.2:
                return "Less"
            elif -2.2 < total <= -3.1:
                return "Mild"
            else:
                return "Severe"

        pothole_df['Severity'] = pothole_df.apply(classify_severity, axis=1)

        # Streamlit app
        st.title("Bump Severity Analysis")

        # Section 1: Filtered Pothole Records
        st.header("1. Filtered Pothole Records")
        st.dataframe(pothole_df.head())

        # Section 2: Severity Distribution
        st.header("2. Severity Distribution")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x='Severity', data=pothole_df, palette="pastel", order=["Less", "Mild", "Severe"])
        plt.title("Pothole Severity Levels")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        st.pyplot(fig)

        # Completion Message
        st.success("Severity analysis completed successfully!")
