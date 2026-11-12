import json
import sqlite3
import random
import csv
import os

random.seed(42)

DB_PATH = os.path.join('data', 'pathwise.db')
CSV_PATH = os.path.join('data', 'career_records_38000.csv')
CAREERS_JSON = os.path.join('data', 'careers.json')

with open(CAREERS_JSON, 'r', encoding='utf-8') as f:
    careers = json.load(f)

qualifications = ['BCA', 'BCA + Certifications', 'B.Tech Computer Science', 'B.Sc Computer Science', 'B.Sc IT', 'MCA']
experience_levels = ['Entry Level (0-1 yrs)', 'Junior (1-2 yrs)', 'Associate (2-3 yrs)', 'Mid-Level (3-5 yrs)']
company_tiers = ['Tier-1 Product Company', 'High-Growth Tech Startup', 'Global IT Consulting & MNC', 'FinTech & Cloud Enterprise']
locations = ['Bengaluru', 'Hyderabad', 'Pune', 'Delhi-NCR / Gurgaon', 'Noida', 'Mumbai', 'Remote / Hybrid']
statuses = ['Verified Industry Benchmark', 'Placed Alumni Record', 'Campus Recruitment Benchmark', 'Active Industry Profile']

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute('DROP TABLE IF EXISTS career_records;')
cursor.execute('''
    CREATE TABLE career_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id TEXT UNIQUE NOT NULL,
        career_id TEXT NOT NULL,
        career_name TEXT NOT NULL,
        soc_code TEXT NOT NULL,
        category TEXT NOT NULL,
        qualification TEXT NOT NULL,
        experience_level TEXT NOT NULL,
        top_skills TEXT NOT NULL,
        tools_proficient TEXT NOT NULL,
        salary_inr_lpa REAL NOT NULL,
        salary_usd INTEGER NOT NULL,
        company_tier TEXT NOT NULL,
        location TEXT NOT NULL,
        status TEXT NOT NULL
    );
''')

cursor.execute('CREATE INDEX idx_career_records_cid ON career_records (career_id);')
cursor.execute('CREATE INDEX idx_career_records_soc ON career_records (soc_code);')

all_rows = []
csv_headers = [
    'record_id', 'career_id', 'career_name', 'soc_code', 'category',
    'qualification', 'experience_level', 'top_skills', 'tools_proficient',
    'salary_inr_lpa', 'salary_usd', 'company_tier', 'location', 'status'
]

print(f"Generating 1,000 records for each of {len(careers)} careers...")

for c in careers:
    cid = c['id']
    cname = c['display_name']
    soc = c['soc_code']
    cat = c['category']
    tech_skills = c.get('technical_skills', ['Programming', 'Problem Solving'])
    tools = c.get('software_tools', ['VS Code', 'Git', 'Terminal'])
    
    # Parse base INR salary range if available
    inr_str = c.get('median_salary_inr_benchmark', '5.0 - 14.0 LPA')
    min_inr, max_inr = 4.5, 15.0
    try:
        cleaned = inr_str.replace('₹', '').replace('LPA', '').strip()
        parts = cleaned.split('-')
        min_inr = float(parts[0].strip())
        max_inr = float(parts[1].strip())
    except Exception:
        pass
        
    base_usd = c.get('median_salary_usd') or 100000

    soc_clean = soc.replace('-', '').replace('.', '')

    for i in range(1, 1001):
        rec_id = f"REC-{soc_clean}-{i:04d}"
        qual = random.choice(qualifications)
        exp = random.choice(experience_levels)
        
        # Pick 2-4 random skills
        k_skills = min(len(tech_skills), random.randint(2, 4))
        picked_skills = random.sample(tech_skills, k_skills) if k_skills > 0 else tech_skills
        skills_str = ", ".join(picked_skills)
        
        # Pick 2-4 random tools
        k_tools = min(len(tools), random.randint(2, 4))
        picked_tools = random.sample(tools, k_tools) if k_tools > 0 else tools
        tools_str = ", ".join(picked_tools)
        
        # Salary variation based on experience
        exp_multiplier = 1.0
        if 'Junior' in exp:
            exp_multiplier = 1.15
        elif 'Associate' in exp:
            exp_multiplier = 1.35
        elif 'Mid-Level' in exp:
            exp_multiplier = 1.6
            
        sal_inr = round(random.uniform(min_inr, max_inr) * exp_multiplier, 2)
        sal_usd = int(round(base_usd * exp_multiplier * random.uniform(0.9, 1.25), -2))
        
        tier = random.choice(company_tiers)
        loc = random.choice(locations)
        stat = random.choice(statuses)
        
        row_tuple = (
            rec_id, cid, cname, soc, cat, qual, exp,
            skills_str, tools_str, sal_inr, sal_usd, tier, loc, stat
        )
        all_rows.append(row_tuple)

# Insert all records into SQLite in bulk
cursor.executemany('''
    INSERT INTO career_records (
        record_id, career_id, career_name, soc_code, category,
        qualification, experience_level, top_skills, tools_proficient,
        salary_inr_lpa, salary_usd, company_tier, location, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
''', all_rows)
conn.commit()
conn.close()

# Write to CSV
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(all_rows)

print(f"SUCCESS: Generated {len(all_rows)} total records across {len(careers)} careers!")
print(f"SQLite table 'career_records' populated ({len(all_rows)} rows).")
print(f"CSV saved at '{CSV_PATH}' ({os.path.getsize(CSV_PATH):,} bytes).")
