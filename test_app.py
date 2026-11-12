import sys
sys.stdout.reconfigure(encoding='utf-8')
import unittest
import json
from app import app
from models import init_db, get_db_connection

class PathWiseAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-key-2026'
        self.client = app.test_client()
        init_db()

    def test_pages_get(self):
        routes = [
            '/',
            '/about',
            '/methodology',
            '/register',
            '/login',
            '/assessment',
            '/careers',
            '/career/software-developers',
            '/compare',
            '/skill-gap',
            '/roadmap',
            '/trial-lab',
            '/trial-lab/data_analyst',
            '/trial-lab/software_developer',
            '/trial-lab/cybersecurity',
            '/trial-lab/ui_ux',
            '/evidence-check',
            '/switch-bridge',
            '/quest',
            '/future-paths',
            '/admin/dataset',
            '/reality-check'
        ]
        for r in routes:
            response = self.client.get(r)
            print(f"GET {r} -> {response.status_code}")
            self.assertEqual(response.status_code, 200, f"Route {r} failed with status {response.status_code}")

    def test_assessment_flow_and_recommendations(self):
        # Submit assessment
        payload = {
            'qualification': 'BCA',
            'semester': 'Semester 3',
            'completed_courses': ['Data Structures & Algorithms', 'Python Programming'],
            'interests': ['Programming and software development', 'Data analysis and visualisation'],
            'skill_Python': '4',
            'skill_SQL': '3',
            'skill_HTML/CSS/JavaScript': '3',
            'skill_Excel & Spreadsheets': '4',
            'skill_Data Analysis': '3',
            'skill_Statistics & Probability': '2',
            'skill_Networking Fundamentals': '2',
            'skill_Problem-Solving': '4',
            'skill_Java': '2',
            'skill_C/C++': '3',
            'skill_System Design & Architecture': '2',
            'tools': ['Python / Jupyter Notebook', 'VS Code', 'Git / GitHub', 'Microsoft Excel'],
            'coding_intensity': 'High',
            'work_type': 'Application Building',
            'analytical_creative': 'Both',
            'independence': 'Balanced',
            'priorities': ['Interest in the work', 'Salary', 'Job outlook']
        }
        res = self.client.post('/assessment', data=payload, follow_redirects=True)
        print(f"POST /assessment -> {res.status_code}")
        self.assertEqual(res.status_code, 200)

        # Recommendations view
        res_rec = self.client.get('/recommendations')
        print(f"GET /recommendations -> {res_rec.status_code}")
        self.assertEqual(res_rec.status_code, 200)

        # Simulator view
        res_sim = self.client.get('/simulator')
        print(f"GET /simulator -> {res_sim.status_code}")
        self.assertEqual(res_sim.status_code, 200)

        # API recalculate
        res_calc = self.client.post('/api/recalculate', json={
            'interests': 40,
            'skills': 30,
            'tools': 10,
            'education': 10,
            'work_preferences': 10
        })
        print(f"POST /api/recalculate -> {res_calc.status_code}")
        self.assertEqual(res_calc.status_code, 200)
        data = json.loads(res_calc.data)
        self.assertEqual(data['status'], 'success')

    def test_trial_lab_submission(self):
        lab_payload = {
            'track_id': 'data_analyst',
            'answers': {
                'da_q1': 'B',
                'da_q2': 'A',
                'da_q3': 'B'
            }
        }
        res = self.client.post('/api/submit-lab', json=lab_payload)
        print(f"POST /api/submit-lab -> {res.status_code}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['score'], 3)
        self.assertEqual(data['max_score'], 3)
        self.assertEqual(data['percentage'], 100.0)

    def test_what_if_simulation(self):
        sim_payload = {
            'skills': {'Python': 5, 'SQL': 4},
            'tools': ['Git / GitHub', 'Docker'],
            'coding_intensity': 'High'
        }
        res = self.client.post('/api/simulate', json=sim_payload)
        print(f"POST /api/simulate -> {res.status_code}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['diffs']) > 0)

    def test_suggested_careers_comparison_and_limits(self):
        from data_manager import get_all_careers, MAX_RECORDS_PER_CAREER
        
        # Verify max 1000 records safety limit
        self.assertEqual(MAX_RECORDS_PER_CAREER, 1000)
        careers = get_all_careers()
        for c in careers:
            self.assertLessEqual(len(c.get('software_tools', [])), 1000)
            self.assertLessEqual(len(c.get('onet_essential_skills', [])), 1000)
            self.assertLessEqual(len(c.get('technical_skills', [])), 1000)
        
        # Test 2-way and 3-way comparison of suggested careers
        res_compare_2 = self.client.get('/compare?c1=software-developers&c2=data-scientists')
        self.assertEqual(res_compare_2.status_code, 200)
        self.assertIn(b'Side-by-Side Career Comparison', res_compare_2.data)
        self.assertIn(b'Software Developers', res_compare_2.data)
        self.assertIn(b'Data Scientists', res_compare_2.data)

        res_compare_3 = self.client.get('/compare?c1=software-developers&c2=data-scientists&c3=web-developers')
        self.assertEqual(res_compare_3.status_code, 200)
        self.assertIn(b'Web Developers', res_compare_3.data)
        print("Comparison of suggested careers and 1000 records limit verified!")

if __name__ == '__main__':
    unittest.main()
