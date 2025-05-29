import pandas as pd
df = pd.read_csv('Salaries.csv')

# ----------Cleaning up the data---------------------------------------

#print(df.info())
#print(df.isnull().sum()) #will find the sum of missing values within each column
df = df.drop(['Notes'],axis=1) # Notes has a null value for all entries so drop  (0 valid values)
df = df.drop(['Status'],axis=1)
#print(df.isnull().sum()) #will find the sum of missing values within each column
df = df[df['BasePay'].notnull()] # drop rows that have missing pay, apparently this is best for salary metrics
print(df.isnull().sum()) #will find the sum of missing values within each column
#print(df.duplicated().sum()) #check if there are duplicates
df['EmployeeName'] = df['EmployeeName'].str.strip().str.title() # duplicate names 
df['Benefits'] = df['Benefits'].fillna(df['TotalPayBenefits'] - df['TotalPay'])
pay_cols = ['BasePay', 'OvertimePay', 'OtherPay', 'TotalPay', 'TotalPayBenefits']
df = df[(df[pay_cols] >= 0).all(axis=1)]
df.to_csv("cleaned_salaries.csv", index=False)



#--------------------------------------------------------------------------
# Question 1: How much the total salary has increased from year 2011 to 2014?
#find total salary for each year then subtract them 
print("\nQuestion 1: How much the total salary has increased from year 2011 to 2014?\n" )
total_salary_by_year = df.groupby('Year')['TotalPay'].sum()
print(total_salary_by_year)

increase = total_salary_by_year[2014] - total_salary_by_year[2011]
print(f"\n Total salary increase from 2011 to 2014: {increase:} ")

#Question 2: Which job title had the highest mean salary in the years 2011 through 2014?
# group each by job title and salaries, find mean, then use max to find whcih is greatets
print("\nQuestion 2: Which job title had the highest mean salary in the years 2011 through 2014?\n" )

mean_salary_by_jobtitle = df.groupby('JobTitle')['TotalPay'].mean()
print(mean_salary_by_jobtitle)

top_job = mean_salary_by_jobtitle.idxmax() 

highest_salary = max(mean_salary_by_jobtitle)
print(f"\n Job title with highest mean salary: {top_job}")
print(f"\n Highest mean salary: {highest_salary}")

#Question 3: How much money could have been saved in the year 2014 by stopping overtime pay?
# Find how much was spent on overtime in 2014

print("\nQuestion 3: How much money could have been saved in the year 2014 by stopping overtime pay?\n" )

total_overtime_pay = df.groupby('Year')['OvertimePay'].sum() #per year
overtime_2014 = total_overtime_pay[2014]
print(f"\n Total saved by stopping overtime in 2014: {overtime_2014}")

#Question 4: Who were the top earning employees across all the years?
# find total earning of each employee, use max to find the top, top 10?

print("\nQuestion 4: Who were the top earning employees across all the years?\n" )

top_salary_by_employee = df.groupby('EmployeeName')['TotalPay'].sum()
#print(top_salary_by_employee)

top_employee = top_salary_by_employee.idxmax() 
print(f"\n Employee with highest salary: {top_employee}")
print(f"\n Top 10 earners in the company: \n{top_salary_by_employee.sort_values(ascending=False).head(10)}")

# Question 5: Which were the least 5 common jobs in 2014, and how much did they cost?
# filter for only 2014, find the amount of employees in certain jobs and use min to find the least employee in each, find the cost, top 5 least

print("\nQuestion 5: Which were the least 5 common jobs in 2014, and how much did they cost?\n" )


df_2014 = df[df['Year'] == 2014]
total_employee_in_job = df_2014.groupby('JobTitle')['EmployeeName'].count()
least_employees_per_job = total_employee_in_job.sort_values(ascending=True).head(5)
print(f"\n 5 jobs with least employees: \n {least_employees_per_job}")

least_job_per_employee = total_employee_in_job.idxmin()

costs =  df_2014[df_2014['JobTitle'].isin(least_employees_per_job.index)]
cost_by_job = costs.groupby('JobTitle')['TotalPay'].sum()

print(f"Cost of jobs with least employees: \n {cost_by_job}")

#Question 6: What percentage did overtime pay constitute of the total pay?
#find total overtime pay and total toal pay, divide overtime pay by total pay and then multiply by 100

print("\nQuestion 6: What percentage did overtime pay constitute of the total pay?\n" )

total_overtime = df['OvertimePay'].sum()  

total_pay = df['TotalPay'].sum()

percentage = (total_overtime/total_pay) * 100 

print(f"Percet of overtime in total pay: {percentage} % \n")