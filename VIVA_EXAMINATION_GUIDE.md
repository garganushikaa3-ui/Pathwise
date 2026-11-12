# PathWise — Viva Voce Examination & Presentation Guide

**Project Title:** PathWise: Decision Support and Career Path Explorer for Technical Career Selection  
**Course:** Bachelor of Computer Applications (BCA) — Minor Project-I  
**Department:** School of Computer Applications (SCA)  
**Institution:** Manav Rachna International Institute of Research and Studies (Computer Applications), Faridabad  
**Academic Year:** 2026  

---

## 1. Executive Abstract

Undergraduate computer applications students frequently struggle to decide which technical career path best matches their evolving skills, coursework, tool knowledge, and work preferences. Commercial portals often exacerbate this confusion through aggressive marketing, unverified salary claims, and opaque recommendations.

**PathWise** is an explainable decision-support and career path explorer built specifically for college students. The system integrates:
1. **38 Verified Technical Careers** mapped directly from official **O*NET Online (v28.0)** and **U.S. Bureau of Labor Statistics (BLS 2025–2035)** matrices, complemented by separate **India Tech Market Benchmarks (INR LPA)**.
2. **Transparent Multi-Factor Scoring Engine** that evaluates compatibility across Interests (30%), Skills (30%), Tools (15%), Education (15%), and Work Preferences (10%) with configurable dynamic priority sliders.
3. **Interactive Career Trial Lab** allowing students to experience bite-sized practical problem-solving in Data Analytics, Software Debugging, Cybersecurity Phishing Triage, and UI/UX Accessibility.
4. **Self-Rating vs Task Evidence Check** that contrasts self-perception against demonstrated task outcomes respectfully to cultivate metacognitive self-awareness without silent overwriting.
5. **What-If Career Simulator & Switch Bridge** to test hypothetical skill improvements and cross-discipline transition feasibility.

---

## 2. System Architecture & Component Interaction

```
+-------------------------------------------------------------------------------+
|                             CLIENT BROWSER (UI)                               |
|   Bootstrap 5.3 + Responsive HTML5/CSS3 + Vanilla JS (DOM & Fetch API)        |
+-------------------------------------------------------------------------------+
       |                                   ^                           |
       | HTTP Form Submissions             | HTML Jinja2 Templates     | Asynchronous Fetch
       v                                   |                           v
+-------------------------------------------------------------------------------+
|                             FLASK APPLICATION CORE (app.py)                   |
|   - Session & Guest Identity Management                                       |
|   - Route Handlers (23+ Endpoints)                                            |
|   - API Endpoints (/api/recalculate, /api/simulate, /api/submit-lab, /api/save)|
+-------------------------------------------------------------------------------+
       |                         |                          |
       v                         v                          v
+-------------------+   +--------------------+   +-----------------------+
| RECOMMENDATION    |   | DATA MANAGER       |   | SQLite DATABASE       |
| ENGINE            |   | (data_manager.py)  |   | (models.py)           |
| Multi-Criteria    |   | JSON/CSV Parser,   |   | - users               |
| Weighted Utility  |   | Schema Validation, |   | - assessments         |
| Scoring & Diags   |   | Duplicate Detector |   | - saved_careers       |
+-------------------+   +--------------------+   | - trial_lab_results   |
       |                         |               | - quest_badges        |
       v                         v               +-----------------------+
+--------------------------------------------+
| MASTER DATASET (data/careers.json)         |
| 38 Verified Technical Roles (O*NET & BLS)  |
+--------------------------------------------+
```

---

## 3. Mathematical Formulation of the Recommendation Model

The scoring engine implements a normalized linear multi-criteria decision model (MCDM):

$$\text{Final Score}(C) = \sum_{k=1}^{n} w_k \cdot S_k(C)$$

Where:
- $w_k$ is the normalized weight for factor $k$, satisfying $\sum_{k=1}^n w_k = 1.0$.
- $S_k(C) \in [0.0, 1.0]$ is the sub-score for career $C$ on dimension $k$.

### Dimensional Scoring Criteria:
1. **Technical Interests ($S_{\text{interests}}$):**
   $$S_{\text{interests}} = \min\left(1.0, \frac{|I_{\text{student}} \cap I_{\text{career}}|}{\min(3, |I_{\text{career}}|)}\right)$$
2. **Current Skills ($S_{\text{skills}}$):**
   $$S_{\text{skills}} = \frac{1}{|K_{\text{career}}|} \sum_{s \in K_{\text{career}}} \frac{\text{Rating}(s)}{5.0}$$
3. **Tools Familiarity ($S_{\text{tools}}$):**
   $$S_{\text{tools}} = \min\left(1.0, \frac{|T_{\text{student}} \cap T_{\text{career}}|}{\min(4, |T_{\text{career}}|)}\right)$$
4. **Education Compatibility ($S_{\text{edu}}$):**
   - Bachelor's / BCA entry: $0.95$
   - Master's / Specialized entry: $0.65$
5. **Work Preference Alignment ($S_{\text{pref}}$):**
   - Coding intensity match (High, Moderate, Low): $1.0$ (exact), $0.75$ (adjacent), $0.40$ (divergent).
   - Analytical vs Creative style alignment: $1.0$ (aligned), $0.80$ (neutral).

---

## 4. Database Schema (SQLite 3)

The persistent database is located at `data/pathwise.db`:

1. **`users` Table:**
   - `id` (INTEGER PRIMARY KEY)
   - `username` (TEXT UNIQUE)
   - `email` (TEXT UNIQUE)
   - `password_hash` (TEXT, PBKDF2-SHA256 via Werkzeug)
   - `full_name`, `college`, `qualification`, `current_semester`, `created_at`

2. **`assessments` Table:**
   - `id` (INTEGER PRIMARY KEY)
   - `user_id` (INTEGER, FOREIGN KEY)
   - `session_id` (TEXT, enables guest assessment persistence)
   - `answers_json` (TEXT, serialized student input)
   - `results_json` (TEXT, top recommendations with breakdown)
   - `weights_json` (TEXT, custom weight values used)
   - `completed_at` (TIMESTAMP)

3. **`saved_careers` Table:**
   - `id` (INTEGER PRIMARY KEY)
   - `user_id`, `career_id`, `notes`, `saved_at` (UNIQUE constraint on user_id + career_id)

4. **`trial_lab_results` Table:**
   - `id` (INTEGER PRIMARY KEY)
   - `user_id`, `session_id`, `career_track`, `score`, `max_score`, `answers_json`, `feedback`, `completed_at`

5. **`quest_badges` Table:**
   - `id` (INTEGER PRIMARY KEY)
   - `user_id`, `badge_key`, `badge_title`, `badge_icon`, `earned_at`

---

## 5. File-by-File Code Walkthrough

| File | Primary Responsibility | Key Functions & Methods |
| :--- | :--- | :--- |
| [`app.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/app.py) | Main controller, routing, session management, REST APIs | `index()`, `assessment()`, `recommendations_view()`, `api_recalculate()`, `api_submit_lab()`, `api_simulate()`, `compare()`, `skill_gap()`, `switch_bridge()` |
| [`recommendation_engine.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/recommendation_engine.py) | Algorithmic matching & explainability diagnostics | `normalize_weights()`, `calculate_career_match()`, `get_recommendations()` |
| [`models.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/models.py) | SQLite database queries, password hashing, persistence | `init_db()`, `create_user()`, `save_assessment()`, `save_trial_result()`, `award_badge()` |
| [`data_manager.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/data_manager.py) | Dataset access, CSV/Excel schema validation, exporter | `get_all_careers()`, `get_career_by_id()`, `validate_and_import_dataset()`, `export_careers_to_csv()` |
| [`trial_lab_data.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/trial_lab_data.py) | Interactive practical scenarios & answer grading | `TRIAL_LAB_TRACKS`, `evaluate_lab_submission()` |
| [`bridge_engine.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/bridge_engine.py) | Role pivot overlap analysis & 4-phase transition | `compute_career_bridge()` |
| [`future_paths_data.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/future_paths_data.py) | 6-month study trajectory comparison | `FUTURE_PATHS` dictionary |
| [`quest_data.py`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/quest_data.py) | Gamified missions and badge registry | `QUEST_MISSIONS` dictionary |

---

## 6. Top 15 Viva Voce Questions & Model Answers

### Q1: What problem does PathWise solve?
> **Answer**: PathWise resolves career decision paralysis among undergraduate BCA students. Rather than relying on generic internet advice or ungrounded commercial bootcamp claims, PathWise offers an explainable decision-support system that evaluates a student's actual coursework, self-rated skills, and work preferences against verified O*NET occupational data, tests practical intuition in a Trial Lab, and charts a realistic roadmap.

### Q2: Why did you choose Python and Flask over a complex framework like Django or React?
> **Answer**: Flask provides a lightweight, transparent, and modular micro-framework ideal for an academic minor project. It keeps code readable for examiners, avoids unnecessary dependency overhead, executes completely offline on local machines, and pairs seamlessly with Pandas for data analytics and Jinja2 for server-rendered UI.

### Q3: What makes the recommendation engine "explainable"?
> **Answer**: In black-box machine learning models (e.g. deep neural networks), it is impossible to explain to a student *why* a particular role was recommended. PathWise implements a multi-criteria weighted utility model where every score displays an exact breakdown: which interests aligned, which self-rated skills contributed, which industry tools were recognized, and what specific gaps remain. Furthermore, the "Why Not This Career?" module explains lower-scoring roles explicitly.

### Q4: Where did you get the career data, and how did you verify it?
> **Answer**: The dataset was constructed from official occupational research databases:
> 1. Occupational skills, tool taxonomies, and descriptions were extracted from the U.S. Department of Labor's **O*NET Online (v28.0)** database (`Essential Skills.xlsx`).
> 2. Median annual wages and 10-year job growth projections were sourced from the **U.S. Bureau of Labor Statistics (BLS 2025–2035)** Employment Matrix.
> 3. To ensure domestic relevance, a separate **India Tech Market Salary Index (INR LPA)** was created so students are not confused by international dollar figures.

### Q5: How do you prevent misleading students regarding salary expectations?
> **Answer**: The application strictly avoids claiming that international salaries apply to Indian graduates. On every career card, the U.S. BLS median ($) is explicitly labeled with country ("United States"), currency ("USD"), reference year ("2025"), and source attribution. Concurrently, a separate Indian benchmark range (e.g. ₹6.0–16.0 LPA for early-career developers) is presented alongside mandatory academic disclaimers.

### Q6: What is the Career Trial Lab and how does it differ from a quiz?
> **Answer**: Quizzes typically test rote factual recall (e.g., "What does HTML stand for?"). The Career Trial Lab presents realistic, situational problem-solving scenarios:
> - *Data Analyst*: Interprets a campus cafeteria sales table to identify volume surges and payment anomalies.
> - *Software Developer*: Dissects Python code to identify an edge-case logic bug where coupon discounts overwrite student discounts.
> - *Cybersecurity*: Triages a deceptive phishing email by analyzing SPF/DKIM authentication failures and lookalike domains.
> - *UI/UX Designer*: Critiques a registration screen based on WCAG contrast guidelines and cognitive chunking principles.

### Q7: Explain the "Self-Rating vs Task Evidence Check" feature.
> **Answer**: Students frequently over- or under-estimate their abilities when filling out self-reported questionnaires. The Evidence Check module pairs self-reported ratings (e.g. Python 4/5) with demonstrated performance on corresponding Trial Lab tasks. It delivers respectful, constructive feedback without shaming the student and—critically—never silently overwrites their self-rating without their explicit consent.

### Q8: What does the "What-If Career Simulator" do?
> **Answer**: The simulator allows students to experiment with hypothetical scenarios (e.g. "What if I improve my Python from 2/5 to 4/5?", "What if I learn Docker and SQL?") without altering their saved profile. It dynamically recalculates scores and shows a side-by-side before/after comparison with exact score differentials (+/- %).

### Q9: How are the weights normalized when a student changes priorities?
> **Answer**: When a student adjusts the priority sliders, the system normalizes the weights so they always sum to 1.0 (100%):
> $$w_k^{\text{norm}} = \frac{w_k}{\sum_{j} w_j}$$
> This mathematical constraint ensures that match scores remain strictly bounded between 0% and 100% and prevents artificial score inflation.

### Q10: How does the Career Switch Bridge calculate transition feasibility?
> **Answer**: The Switch Bridge computes set operations on skills and tools between Career A (Source) and Career B (Target):
> - Transferable Skills: $S_A \cap S_B$
> - Technical Gaps to Learn: $S_B \setminus S_A$
> - Transferable Tools: $T_A \cap T_B$
> It then calculates an overlap percentage and generates a structured 4-phase transition roadmap (Capitalize Strengths &rarr; Close Gaps &rarr; Build Hybrid Project &rarr; Resume Positioning).

### Q11: How is user data stored and secured?
> **Answer**: All data is stored in a local SQLite database (`data/pathwise.db`). User passwords are never stored in plain text; they are hashed using salted PBKDF2-SHA256 via Werkzeug's security module. Session identity handles both logged-in students and guest explorers seamlessly.

### Q12: What does the Career Readiness Meter indicate?
> **Answer**: We intentionally avoid calling undergraduate students "job ready" because true job readiness requires extensive project and internship experience. Instead, we use transparent exploration tiers:
> - *Better prepared for exploration* ($\ge 72\%$)
> - *Developing* ($48\% - 71\%$)
> - *Foundation to build* ($< 48\%$)

### Q13: How does the Dataset Administrator feature work?
> **Answer**: The `/admin/dataset` module provides an automated validation utility. If a user uploads an external CSV or Excel file, it scans column headers, validates required title fields, detects duplicate career rows, reports rejected rows with line numbers, and exports the active 38-career master dataset as a standardized CSV file.

### Q14: How does PathWise protect user privacy in the Trends feature?
> **Answer**: The `/trends` module only displays aggregate counts (e.g., number of times a career was matched, category distribution). No names, email addresses, or individual questionnaires are ever exposed. Furthermore, if fewer than 1 assessment exists, the system gracefully hides charts rather than fabricating synthetic user statistics.

### Q15: What are the main limitations of the system?
> **Answer**:
> 1. Self-reported skill ratings are subjective and depend on student honesty.
> 2. Trial Lab tasks are short introductory exercises, not full professional competency tests.
> 3. Recommendations represent guidance and decision-support, not an employment guarantee or deterministic future prediction.

---

## 7. Recommended 5-Minute Demonstration Script

When presenting to your supervisor or viva board:
1. **Introduction (1 min):**
   - *"Respected examiners, my BCA Minor Project-I is PathWise, a decision-support system for technical career exploration."*
   - Show the Landing Page: highlight 38 verified careers, O*NET integration, and the Computer Applications SCA header.
2. **Assessment & Recommendation Engine (1.5 mins):**
   - Click **Start Career Assessment** & show the 6-step wizard.
   - Show the generated **Recommendations** page: point out the top match, the match score (e.g. 92%), the breakdown of why it matched, and demonstrate the **Priority Sliders** recalculating rankings live.
3. **Career Trial Lab & Evidence Check (1.5 mins):**
   - Navigate to **Career Trial Lab** & open the **Software Developer Lab** (bug inspection) or **Data Analyst Lab** (cafeteria data).
   - Answer the scenario questions, submit, and show the immediate feedback and unlocked **Quest Badge**.
   - Open **Evidence Check** to show how self-ratings are calibrated against lab evidence respectfully.
4. **Simulator & Switch Bridge (1 min):**
   - Open the **What-If Simulator**, increase Python from 2 to 4, and click *Recalculate* to demonstrate the live +/- score differential.
   - Show the **Career Switch Bridge** (e.g. Web Developer &rarr; Data Scientist) displaying transferable skills and the 4-phase transition roadmap.
5. **Conclusion:**
   - Mention the **Dataset Inspector** and summarize: *"PathWise demonstrates that college career guidance can be transparent, data-grounded, and practically verifiable without relying on black-box hype."*
