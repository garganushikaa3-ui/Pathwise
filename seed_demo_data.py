import os
import json
import sqlite3
from models import (
    init_db, create_user, save_assessment, save_career,
    save_trial_result, award_badge, get_db_connection
)
from recommendation_engine import get_recommendations, normalize_weights

def seed():
    print("Initializing database...")
    init_db()

    # 1. Create a demonstration student profile
    username = "rahul_bca"
    email = "rahul.bca@student.mriirs.edu.in"
    password = "password123"
    full_name = "Rahul Sharma"
    college = "Manav Rachna International Institute of Research and Studies"
    qualification = "BCA"
    current_semester = "Semester 3 (Minor Project-I)"

    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not existing:
        user_id, err = create_user(username, email, password, full_name, college, qualification, current_semester)
        print(f"Created demo user: {full_name} (ID: {user_id})")
    else:
        user_id = existing['id']
        print(f"Demo user already exists (ID: {user_id})")

    # 2. Seed a realistic student questionnaire input
    demo_input = {
        "education": {
            "qualification": "BCA",
            "semester": "Semester 3",
            "completed_courses": [
                "Programming in C / C++",
                "Data Structures & Algorithms",
                "Database Management Systems (DBMS)",
                "Web Technologies (HTML, CSS, JS)",
                "Object Oriented Programming (Java / C++)",
                "Python Programming"
            ]
        },
        "interests": [
            "Programming and software development",
            "Data analysis and visualisation",
            "Web development",
            "Artificial intelligence and machine learning"
        ],
        "skills": {
            "Python": 4,
            "Java": 3,
            "C/C++": 3,
            "SQL": 3,
            "HTML/CSS/JavaScript": 3,
            "Excel & Spreadsheets": 4,
            "Data Analysis": 3,
            "Statistics & Probability": 2,
            "Networking Fundamentals": 2,
            "Problem-Solving": 4,
            "System Design & Architecture": 2
        },
        "tools": [
            "VS Code",
            "Git / GitHub",
            "Python / Jupyter Notebook",
            "Microsoft Excel",
            "MySQL / SQLite",
            "Postman"
        ],
        "work_preferences": {
            "coding_intensity": "High",
            "work_type": "Application Building",
            "analytical_creative": "Both",
            "independence": "Balanced"
        },
        "priorities": [
            "Interest in the work",
            "Skill compatibility",
            "Salary",
            "Job outlook"
        ]
    }

    weights = normalize_weights({
        'interests': 0.30,
        'skills': 0.30,
        'tools': 0.15,
        'education': 0.15,
        'work_preferences': 0.10,
        'salary': 0.05,
        'job_outlook': 0.05
    })

    recs = get_recommendations(demo_input, custom_weights=weights)
    save_assessment(user_id, "demo-session-2026", demo_input, recs, weights)
    print(f"Saved demo assessment with {len(recs)} calculated career recommendations.")

    # 3. Seed saved careers
    save_career(user_id, "software-developers", "Top personal interest for semester capstone.")
    save_career(user_id, "data-scientists", "Secondary exploration track for data analytics elective.")
    save_career(user_id, "web-developers", "Considering full-stack freelancing projects.")
    print("Bookmarked 3 target careers to student dashboard.")

    # 4. Seed completed practical trial lab results
    save_trial_result(
        user_id, "demo-session-2026", "software_developer", 3, 3,
        {"sd_q1": "B", "sd_q2": "B", "sd_q3": "B"},
        "Outstanding algorithmic logic! Identified coupon discount overwrite bug and hash map O(1) complexity correctly."
    )
    save_trial_result(
        user_id, "demo-session-2026", "data_analyst", 3, 3,
        {"da_q1": "B", "da_q2": "A", "da_q3": "B"},
        "Excellent data analysis intuition! Identified Friday revenue surge and weekend payment anomaly."
    )
    save_trial_result(
        user_id, "demo-session-2026", "cybersecurity", 3, 3,
        {"cs_q1": "B", "cs_q2": "B", "cs_q3": "B"},
        "High security awareness. Correctly triaged phishing headers and multi-factor authentication mitigations."
    )
    print("Recorded 3 practical trial lab submissions.")

    # 5. Award quest badges
    award_badge(user_id, "profile_pioneer", "Profile Pioneer", "bi-person-check")
    award_badge(user_id, "code_architect", "Code Architect", "bi-code-slash")
    award_badge(user_id, "data_detective", "Data Detective", "bi-graph-up-arrow")
    award_badge(user_id, "cyber_sentinel", "Cyber Sentinel", "bi-shield-check")
    award_badge(user_id, "career_scholar", "Career Scholar", "bi-bookmark-star")
    print("Awarded 5 exploration quest badges.")

    print("\n========================================================")
    print("Demo Data Seeded Successfully!")
    print(f"Login Email:    {email}")
    print(f"Login Password: {password}")
    print("You can log in directly or explore as a guest student.")
    print("========================================================")

if __name__ == '__main__':
    seed()
