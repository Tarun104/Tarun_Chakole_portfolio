import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("skills_jobs_dataset.csv")

# Title
st.title("AI-Powered Career & Skill Analytics System")
st.image("Job_Market_Dashboard.png")
st.write("Analyze job market trends and get career recommendations based on your skills.")

# Show Dataset
if st.checkbox("Show Dataset"):
    st.dataframe(df.head())

# Domain Counts
st.subheader("Job Domain Distribution")
st.bar_chart(df["Domain"].value_counts())

# Skill Recommendation System
st.subheader("Skill Gap Analyzer")

user_input = st.text_input(
    "Enter your skills (comma separated)"
)

if user_input:

    user_skills = user_input.lower().split(",")

    user_skills = [s.strip() for s in user_skills]

    domain_skills = {}

    for domain in df["Domain"].unique():

        temp = df[df["Domain"] == domain]

        skills_text = ", ".join(
            temp["Skills"].dropna().astype(str)
        ).lower().split(",")

        skills_text = [
            s.strip()
            for s in skills_text
            if s.strip() != ""
        ]

        top_skills = list(
            pd.Series(skills_text)
            .value_counts()
            .head(10)
            .index
        )

        domain_skills[domain] = top_skills

    results = []

    for domain, skills in domain_skills.items():

        matched = []

        missing = []

        for skill in skills:

            if skill in user_skills:
                matched.append(skill)

            else:
                missing.append(skill)

        match_percent = round(
            (len(matched) / len(skills)) * 100,
            2
        )

        results.append({
            "Domain": domain,
            "Match %": match_percent,
            "Matched Skills": matched,
            "Missing Skills": missing[:5]
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="Match %",
        ascending=False
    )

    best_domain = results_df.iloc[0]

    st.success(
        f"Best Matching Domain: {best_domain['Domain']}"
    )

    st.write(
        f"Match Percentage: {best_domain['Match %']}%"
    )

    st.write("Matched Skills:")
    st.write(best_domain["Matched Skills"])

    st.write("Recommended Skills To Learn:")
    st.write(best_domain["Missing Skills"])