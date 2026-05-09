import pandas as pd

df = pd.read_csv("skills_jobs_dataset.csv")

## input ## 
user_skills = input("Enter your skills: ").lower().split(",")

user_skills = [skill.strip() for skill in user_skills]

domain_skills = {}

## Domain Skills Dictionary ##
for domain in df["Domain"].unique():

    temp = df[df["Domain"] == domain]

    skills_text = ", ".join(
        temp["Skills"].dropna().astype(str)
    ).lower().split(",")

    skills_text = [s.strip() for s in skills_text if s.strip() != ""]

    top_skills = list(pd.Series(skills_text).value_counts().head(10).index)

    domain_skills[domain] = top_skills

## Skill Matching Logic ##
results = []

for domain, skills in domain_skills.items():

    matched = []

    missing = []

    for skill in skills:

        if skill.lower() in user_skills:
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

## Final Recommendation ##
results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Match %",
    ascending=False
)

best_domain = results_df.iloc[0]

print("\n===== Career Recommendation =====\n")

print(f"Best Matching Domain: {best_domain['Domain']}")
print(f"Match Percentage: {best_domain['Match %']}%")

print("\nMatched Skills:")
print(best_domain['Matched Skills'])

print("\nRecommended Skills To Learn:")
print(best_domain['Missing Skills'])