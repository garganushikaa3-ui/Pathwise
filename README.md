# PathWise — Decision Support and Career Path Explorer for Technical Career Selection

**BCA Minor Project-I**  
**School of Computer Applications (SCA)**  
**Manav Rachna International Institute of Research and Studies (Computer Applications)**  
Academic Session: 2026

---

## 1. Project Overview

**PathWise** is an explainable decision-support and career exploration web application built specifically for undergraduate Computer Applications (BCA) and Computer Science students.

Undergraduate students frequently experience decision paralysis when trying to navigate technical careers. PathWise addresses this by combining official occupational taxonomy, transparent multi-criteria compatibility matching, hands-on practical task simulation, metacognitive self-rating calibration, and customizable learning roadmaps.

---

## 2. Key Features Implemented

1. **Explainable Recommendation Engine**:
   - Calculates compatibility using configurable transparent weights:
     - Technical Interests: 30%
     - Reported Skills (0–5 scale): 30%
     - Software Tools Known: 15%
     - Education / Academic Stage: 15%
     - Work Environment Preferences: 10%
   - Generates detailed diagnostics: reasons why a career matched, matching skills, skill gaps, and next action items.
   - Includes **Career Priority Sliders** that normalize weights and recalculate rankings dynamically.

2. **38 Verified Technical Careers**:
   - 100% verified against official **O*NET Online (v28.0)** and **U.S. Bureau of Labor Statistics (BLS 2025–2035)** employment projections.
   - **Enforced Data Bound**: Maximum 1,000 records safety cap per career on tools, skills, work activities, and batch dataset imports (`MAX_RECORDS_PER_CAREER = 1000`).
   - Features dual compensation benchmarking:
     - U.S. BLS 2025 Median Annual Wage ($)
     - Separate India Tech Market Benchmark Range (INR Lakhs Per Annum)
   - Detailed O*NET essential skills (with Importance & Level data), curated practical skills, and tools.

3. **Suggested Careers Comparison Matrix**:
   - Direct side-by-side comparative matrix of the student's top recommended careers embedded directly on the Recommendations page.
   - 1-click comparison shortcuts: `Compare #1 vs #2`, `Compare #1 vs #3`, or `Compare All Top 3 Together`.
   - Compares personalized compatibility score, India vs US salaries, 10-year job outlook, coding intensity, matched strengths, and skill gaps to bridge.
   - Personalized compatibility scores and readiness badges reflected in the main `/compare` comparison tool.

4. **Career Trial Lab**:
   - Practical interactive sandbox across 4 core technical domains:
     - **Data Analyst**: Interpret college cafeteria sales dataset, calculate metrics, and identify behavioral anomalies.
     - **Software Developer**: Inspect Python discount logic, identify edge case overwrite bug, and analyze data structure complexity.
     - **Cybersecurity**: Analyze phishing email headers, SPF/DKIM validation, and assess authentication mitigations.
     - **UI/UX Designer**: Critique a mobile form flow for WCAG contrast ratios, cognitive chunking, and button psychology.
   - Provides instant scoring, detailed explanations for every option, and quest badge awards.

4. **Self-Rating vs Task Evidence Check**:
   - Metacognitive calibration tool comparing self-reported skill ratings (e.g. Python 4/5) with practical lab outcomes.
   - Provides constructive, non-shaming feedback without silently overwriting student self-perceptions.

5. **What-If Career Simulator**:
   - Interactive testing laboratory allowing students to test hypothetical skill improvements (e.g. Python 2 &rarr; 4) or tool additions without altering their saved profile.
   - Displays side-by-side before/after comparison tables with exact score differentials.

6. **Career Reality Check**:
   - "Day in the Life" transparency view highlighting typical daily activities, common developer frustrations, entry prerequisites, and starter tasks for BCA students.

7. **"Why Not This Career?" Module**:
   - Explicit explainability inspector for lower-ranked careers, explaining which unselected interests, missing tools, or work preferences caused the lower score.

8. **Career Switch Bridge**:
   - Pivot analyzer between any two careers (e.g. Web Developer &rarr; Data Scientist) with skill overlap analysis and a 4-phase transition roadmap.

9. **Career Quest Gamification**:
   - 8 professional exploration missions with XP counters and unlockable badges (e.g., *Profile Pioneer*, *Data Detective*, *Code Architect*, *Cyber Sentinel*, *UX Craftsman*).

10. **Future Path Preview**:
    - Side-by-side trajectory comparison of learning paths (e.g. *Data Intelligence Path* vs *Full-Stack Web Development Path*).

11. **Anonymous Exploration Trends**:
    - Privacy-conscious aggregate analytics on frequently matched roles and popular categories among students.

12. **Dataset & Administrator Management**:
    - Upload and validate external CSV/Excel career datasets with duplicate detection, schema validation, error reporting, and master dataset CSV export.

13. **Methodology & Limitations**:
    - Mathematical scoring transparency, ethical disclaimers, and data attribution.

---

## 3. Technology Stack

- **Backend**: Python 3.13, Flask 3.1
- **Data Analytics**: Pandas, OpenPyXL
- **Database**: SQLite 3 (`data/pathwise.db`)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons, Chart.js
- **Network / Dependencies**: 100% Local and Offline (No paid APIs or external keys required)

---

## 4. How to Run the Application

The application is already running in your workspace on:
```
http://127.0.0.1:5000
```

To run manually at any time:
```powershell
# 1. Open PowerShell in project directory
cd c:\Users\garga\OneDrive\Desktop\pathwise

# 2. Run Flask application
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000`.

To run automated tests:
```powershell
python test_app.py
```

---

## 5. Viva Voce Preparation Guide (For Examiners)

### Q1: What is the main objective of PathWise?
> **Answer**: PathWise is a technical career decision-support system designed for BCA students. It replaces guesswork with explainable compatibility scoring across 38 verified technical careers, lets students try real tasks in a Trial Lab, and provides step-by-step roadmaps from college coursework to career entry.

### Q2: Why is the recommendation engine called "explainable"?
> **Answer**: Instead of using opaque black-box machine learning algorithms, PathWise uses an explicit weighted scoring formula:
> $$\text{Score} = (0.30 \times \text{Interests}) + (0.30 \times \text{Skills}) + (0.15 \times \text{Tools}) + (0.15 \times \text{Education}) + (0.10 \times \text{Preferences})$$
> Every recommendation displays exact contribution percentages, matched skills, missing tools, and includes a "Why Not This Career?" diagnostic for lower-ranked roles.

### Q3: What is the Career Trial Lab and how does it support students?
> **Answer**: Many students self-rate skills based on classroom theory rather than practical problem-solving. The Trial Lab gives them bite-sized tasks in Data Analytics, Software Debugging, Cybersecurity, and UX Design. The Evidence Check module then compares their self-rating against their task result respectfully to build honest self-awareness without discouragement.

### Q4: Where does the dataset come from?
> **Answer**: Occupational skills, importance levels, and tools are imported and normalized from the official U.S. Department of Labor **O*NET Online (v28.0)** database (`Essential Skills.xlsx`). International median wages and 10-year job outlooks come from the **U.S. Bureau of Labor Statistics (BLS 2025–2035)** matrix. Domestic salary ranges are separately provided under the **India Tech Market Benchmark (INR LPA)** to ensure students have realistic local expectations.
