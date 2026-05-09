import pandas as pd
import os

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

print(da.shape)


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

print(sd.shape)


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

print(ai.shape)



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

print(final_df.shape)
print(final_df.head())
print(final_df.isnull().sum())

final_df.to_csv("final_jobs_dataset.csv", index=False)
