
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_overview(df):
    if df is not None and not df.empty:

        c = df['label'].value_counts()

        # Check conditions and display appropriate messages
        if c[0] < 2:
            st.subheader("<center>Well Maintained</center>", unsafe_allow_html=True)
        elif 2 <= c[0] < 8:
            st.subheader("<center>Poorly Maintained, requires urgent rectification</center>", unsafe_allow_html=True)
        else:
            st.subheader("<center>Critical Condition, needs immediate attention</center>", unsafe_allow_html=True)
            
        # Section 2: Label Distribution
        st.header("2. Label Distribution")
        st.subheader("Count of Each Label")
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.countplot(x="label", data=df, palette="Set2", ax=ax1)
        st.pyplot(fig1)

        # Section 3: Distribution of Sensor Data
        st.header("3. Distribution of Sensor Data")
        columns = ["x", "y", "z"]

        for col in columns:
            st.subheader(f"Histogram of {col}")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(df[col], bins=30, kde=True, color="skyblue", ax=ax)
            st.pyplot(fig)

        # Section 4: Pair Plot for Relationships
        st.header("4. Relationship Between Sensor Axes")
        st.subheader("Pair Plot of x, y, z")
        pair_fig = sns.pairplot(df, hue="label", palette="husl")
        st.pyplot(pair_fig)

        # Section 5: Correlation Heatmap
        st.header("5. Correlation Heatmap")
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.heatmap(df[columns].corr(), annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)

        
