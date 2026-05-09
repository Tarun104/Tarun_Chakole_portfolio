import pandas as pd
import os
############## DAY1 ###############


# print(os.listdir("Data_analytics_job_dataset"))
# print(os.listdir("Software_dev_job_dataset"))
# print(os.listdir("AI_jobs_dataset"))


da = pd.read_csv(r"Data_analytics_job_dataset/BusinessAnalyst.csv") # r is used to avoid escape characters in the file path
da2 = pd.read_csv(r"Data_analytics_job_dataset/DataAnalyst Jobs.csv")
da3 = pd.read_csv(r"Data_analytics_job_dataset/DataAnalyst.csv")
sd = pd.read_csv(r"Software_dev_job_dataset/fresher_jobs_2025_q3.csv")
sd2 = pd.read_csv(r"Software_dev_job_dataset/fresher_jobs_2025_q4.csv")
sd3 = pd.read_csv(r"Software_dev_job_dataset/fresher_jobs.csv")
ai = pd.read_csv(r"AI_jobs_dataset/ai_jobs_market_2025_2026.csv")


# print(da.head())
# print(da2.head())
# print(da3.head())
# print(sd.head())
# print(sd2.head())
# print(sd3.head())
# print(ai.head())


da_files = os.listdir("Data_analytics_job_dataset") # os.listdir() returns a list of all files and directories in the specified directory.
# Here, it is used to get a list of all files in the "Data_analytics_job_dataset" directory, which contains the CSV files for data analytics jobs.

da_list = []
for file in da_files:
    if file.endswith(".csv"):
        path = f"Data_analytics_job_dataset\\{file}" # f-string is used to create a file path by combining the directory name and the file name. The double backslash is used to escape the backslash character in the file path.
        df = pd.read_csv(path, encoding="latin1") 
        da_list.append(df)

da = pd.concat(da_list, ignore_index=True) 
da["Domain"] = "Data Analytics"

# print(da.shape) 


####### Software Development
sd_files = os.listdir("Software_dev_job_dataset")

sd_list = []
for file in sd_files:
    if file.endswith(".csv"):
        path = f"Software_dev_job_dataset\\{file}"
        temp = pd.read_csv(path, encoding="latin1")
        sd_list.append(temp)

sd = pd.concat(sd_list, ignore_index=True)
sd["Domain"] = "Software Development"

# print(sd.shape)


##### AI Jobs
ai_files = os.listdir("AI_jobs_dataset")

ai_list = []
for file in ai_files:
    if file.endswith(".csv"):
        path = f"AI_jobs_dataset\\{file}"
        temp = pd.read_csv(path, encoding="latin1")
        ai_list.append(temp)

ai = pd.concat(ai_list, ignore_index=True)
ai["Domain"] = "AI/ML"

# print(ai.shape)



# print(da.columns)
# print(sd.columns)
# print(ai.columns)

#### common columns

# Data Analytics columns
da_clean = da.rename(columns={
    "Job Title": "Job_Title",
    "Salary Estimate": "Salary",
    "Job Description": "Description",
    "Company Name": "Company",
    "Location": "Location"
})

da_clean = da_clean[["Domain", "Job_Title", "Company", "Location", "Salary", "Description"]]


# Software Dev columns
sd_clean = sd.rename(columns={
    "Job Title": "Job_Title",
    "Salary": "Salary",
    "Company Name": "Company",
    "Location": "Location",
    "Job Roles": "Description"
})

sd_clean = sd_clean[["Domain", "Job_Title", "Company", "Location", "Salary", "Description"]]


# AI Jobs columns
ai_clean = ai.rename(columns={
    "job_title": "Job_Title",
    "annual_salary_usd": "Salary",
    "required_skills": "Description",
    "city": "Location",
    "industry": "Company"
})

ai_clean = ai_clean[["Domain", "Job_Title", "Company", "Location", "Salary", "Description"]]


#### combined data
final_df = pd.concat([da_clean, sd_clean, ai_clean], ignore_index=True)

# print(final_df.shape)
# print(final_df.head())
# print(final_df.isnull().sum())

final_df.to_csv("final_jobs_dataset.csv", index=False) 




################### DAY 2 ###################

########## LOAD DATASET
df = pd.read_csv("final_jobs_dataset.csv")

# print(df.shape)
# print(df.head())
# print(df.isnull().sum())

########### Data Cleaning
df = df.drop_duplicates()
df["Company"] = df["Company"].fillna("Unknown") #### Fill Missing Company Values
df["Description"] = df["Description"].fillna("Not Available") #### Fill Missing Description Values
df["Salary"] = df["Salary"].astype(str)
# print(df.info())
# print(df["Domain"].unique())
# print(df.shape)

df.to_csv("cleaned_jobs_dataset.csv", index=False)





################### DAY 3 ###################

######## SKILL EXTRACTION
df = pd.read_csv("cleaned_jobs_dataset.csv")
skills = [
    "Python", "SQL", "Excel", "Power BI", "Tableau",
    "Java", "C++", "Machine Learning", "Deep Learning",
    "React", "JavaScript", "AWS", "Azure",
    "Pandas", "NumPy", "Communication", "Statistics"
]
def extract_skills(text):
    found_skills = []

    text = str(text).lower()

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return ", ".join(found_skills)

df["Skills"] = df["Description"].apply(extract_skills)

# print(df[["Job_Title", "Skills"]].head())


####### MOST COMMON SKILLS
all_skills = ", ".join(df["Skills"]).split(",")

all_skills = [skill.strip() for skill in all_skills if skill.strip() != ""]

skill_counts = pd.Series(all_skills).value_counts()

# print(skill_counts.head(15))
# print(df.head())

### DOMAIN WISE SKILLS
da_skills = df[df["Domain"] == "Data Analytics"]

# print(da_skills["Skills"].head())

sd_skills = df[df["Domain"] == "Software Development"]

# print(sd_skills["Skills"].head())



######## MULTI DOMAIN SKILL ANALYSIS
df.to_csv("skills_jobs_dataset.csv", index=False)
for domain in df["Domain"].unique():

    temp = df[df["Domain"] == domain]

    skills_text = ", ".join(temp["Skills"]).split(",")

    skills_text = [s.strip() for s in skills_text if s.strip() != ""]

# print("\n", domain)
# print(pd.Series(skills_text).value_counts().head(10))




################### DAY 4 ###################
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("skills_jobs_dataset.csv")

## Charts ##
## top hiring ##
domain_counts = df["Domain"].value_counts()

plt.figure(figsize=(8,5))
domain_counts.plot(kind="bar")

plt.title("Top Hiring Domains")
plt.xlabel("Domain")
plt.ylabel("Number of Jobs")

plt.xticks(rotation=0)
plt.savefig("charts/top_hiring_domains.png")

# plt.show()

## top skills ##
all_skills = ", ".join(df["Skills"].dropna().astype(str)).split(",")

all_skills = [s.strip() for s in all_skills if s.strip() != ""]

skill_counts = pd.Series(all_skills).value_counts().head(10)

plt.figure(figsize=(10,5))

skill_counts.plot(kind="bar")

plt.title("Top 10 Most Demanded Skills")
plt.xlabel("Skills")
plt.ylabel("Demand Count")

plt.xticks(rotation=0)
plt.savefig("charts/top_skills.png")

# plt.show()

## Top locations ##
top_locations = df["Location"].value_counts().head(10)

plt.figure(figsize=(10,5))
top_locations.plot(kind="bar")

plt.title("Top Hiring Locations")
plt.xlabel("Location")
plt.ylabel("Job Count")

plt.xticks(rotation=0)
plt.savefig("charts/top_locations.png")

# plt.show()

## ai vs da vs dev ##
domain_skill_counts = df.groupby("Domain")["Skills"].count()

plt.figure(figsize=(8,5))
domain_skill_counts.plot(kind="bar")

plt.title("Skills Records by Domain")
plt.xlabel("Domain")
plt.ylabel("Count")

plt.xticks(rotation=0)
plt.savefig("charts/domain_skill_comparison.png")

# plt.show()

## top job titles ##
top_jobs = df["Job_Title"].value_counts().head(10)

plt.figure(figsize=(10,5))
top_jobs.plot(kind="bar")

plt.title("Top Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Count")

plt.xticks(rotation=30)
plt.savefig("charts/top_job_titles.png")

# plt.show()


## domain wise top skills ##
# Loop through each domain
for domain in df["Domain"].unique():

    # Filter domain data
    temp = df[df["Domain"] == domain]

    # Handle NaN values safely
    skills_text = ", ".join(
        temp["Skills"].dropna().astype(str)
    ).split(",")

    # Clean skills list
    skills_text = [
        skill.strip()
        for skill in skills_text
        if skill.strip() != ""
    ]

    # Count top skills
    top_skills = pd.Series(skills_text).value_counts().head(10)

    # Create chart
    plt.figure(figsize=(10, 5))

    top_skills.plot(kind="bar")

    # Titles & Labels
    plt.title(f"Top Skills in {domain}")
    plt.xlabel("Skills")
    plt.ylabel("Demand Count")

    plt.xticks(rotation=45)

    # Safe file name
    safe_domain = domain.replace("/", "_")

    # Save chart
    plt.savefig(f"charts/{safe_domain}_skills.png")

    # Show chart
    plt.show()