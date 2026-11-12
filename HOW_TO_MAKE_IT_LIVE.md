# PathWise — How to Make It Live (Complete Deployment Guide)

This guide explains how to run **PathWise** live locally on your computer, across your college Wi-Fi network, and deploy it live to the public internet for free.

---

## Part 1: Your Direct Live Links Right Now

The local server is already running. Click or paste these links in your browser:

- **Homepage:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Recommendations & Comparison Matrix:** [http://127.0.0.1:5000/recommendations](http://127.0.0.1:5000/recommendations)
- **Side-by-Side Career Comparison:** [http://127.0.0.1:5000/compare](http://127.0.0.1:5000/compare)
- **Career Trial Lab (Hands-on Tasks):** [http://127.0.0.1:5000/trial-lab](http://127.0.0.1:5000/trial-lab)
- **What-If Career Simulator:** [http://127.0.0.1:5000/simulator](http://127.0.0.1:5000/simulator)
- **BCA Minor Project-I Report (Print/PDF):** [http://127.0.0.1:5000/project-report](http://127.0.0.1:5000/project-report)

---

## Part 2: How to Run It Live on Your Computer Anytime

You do **not** need to write complex commands every time:

### Method A: 1-Click Desktop Launcher (Easiest)
1. Go to your computer's **Desktop**.
2. Double-click the file named **`Run_PathWise.bat`** (or click the shortcut **`Launch PathWise`**).
3. A black command window will open, and your default web browser (Chrome or Edge) will automatically open `http://127.0.0.1:5000`.

### Method B: From PowerShell or Command Prompt
1. Open PowerShell or Command Prompt.
2. Navigate to your project folder:
   ```powershell
   cd C:\Users\garga\OneDrive\Desktop\pathwise
   ```
3. Run the Flask server:
   ```powershell
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000`.

---

## Part 3: How to Open It Live on Your Mobile Phone (Same Wi-Fi)

You can demonstrate PathWise to your teachers or friends directly on your phone without deploying anything to the cloud:

1. Connect your mobile phone and your laptop to the **same Wi-Fi network** (or connect your laptop to your phone's mobile hotspot).
2. Ensure PathWise is running on your laptop.
3. Open the Chrome or Safari browser on your phone and type your laptop's Wi-Fi IP address:
   ```
   http://192.168.10.41:5000
   ```
4. The complete responsive PathWise website will load on your phone!

*(Note: If your laptop's IP address changes in the future, run `ipconfig` in PowerShell to find your current IPv4 Address).*

---

## Part 4: How to Get an Instant Public Internet Link (In 30 Seconds)

If you need a public `https://...` link so someone outside your house or an external examiner can view it live from their own phone/laptop anywhere in the world:

### Option 1: Instant Free SSH Tunnel (No Account, No Installation Needed)
Your Windows machine already has OpenSSH installed. With PathWise running on port 5000:

1. Open a new PowerShell window.
2. Run this command:
   ```powershell
   ssh -p 443 -R0:localhost:5000 a.pinggy.io
   ```
   *(Or alternatively: `ssh -R 80:localhost:5000 localhost.run`)*
3. Pinggy will immediately output a public HTTPS URL (e.g. `https://random-name.a.pinggy.link`).
4. Anyone in the world can open that link in their browser and access your running project!

### Option 2: Using ngrok
1. Download ngrok from [ngrok.com](https://ngrok.com) (free).
2. In PowerShell, run:
   ```powershell
   ngrok http 5000
   ```
3. Copy the `Forwarding` URL (`https://....ngrok-free.app`) and share it with your professor.

---

## Part 5: How to Deploy Permanently on Free Cloud Hosting

If you want the project permanently live 24/7 on the internet (even when your computer is turned off):

### Option A: Deploy on Render.com (Recommended for College Projects)
**Render** gives you a free URL like `https://pathwise.onrender.com`.

1. Create a free account on [GitHub.com](https://github.com) and push your `pathwise` folder to a new repository.
2. Sign up for free at [Render.com](https://render.com).
3. Click **New +** &rarr; **Web Service**.
4. Select your GitHub repository.
5. In the settings:
   - **Name:** `pathwise`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app` *(We already configured the `Procfile` and `requirements.txt` for this)*
6. Click **Deploy Web Service**.
7. In 2–3 minutes, Render will give you your permanent public HTTPS URL!

### Option B: Deploy on PythonAnywhere.com (No Git Required)
**PythonAnywhere** is designed specifically for Python students:

1. Sign up for a free Beginner account at [PythonAnywhere.com](https://www.pythonanywhere.com).
2. Go to the **Files** tab and upload your `pathwise` folder as a `.zip` file, then open a Bash console and run `unzip pathwise.zip`.
3. In the **Web** tab, click **Add a new web app** &rarr; select **Flask** &rarr; **Python 3.10+**.
4. Set the path to `/home/yourusername/pathwise/app.py`.
5. Click **Reload your web app**.
6. Your site is live at `https://yourusername.pythonanywhere.com`!

---

## Summary Checklist for Your Viva / Demo

- [x] Local Server is running: `http://127.0.0.1:5000`
- [x] Desktop 1-Click Launchers are placed on your Desktop: `Run_PathWise.bat`
- [x] Phone Access on Wi-Fi: `http://192.168.10.41:5000`
- [x] Demo Account Credentials:
  - **Email:** `rahul.bca@student.mriirs.edu.in`
  - **Password:** `password123`
- [x] Academic Project Report with Print/PDF formatting: `http://127.0.0.1:5000/project-report`
- [x] Examiner Q&A Guide: [`VIVA_EXAMINATION_GUIDE.md`](file:///c:/Users/garga/OneDrive/Desktop/pathwise/VIVA_EXAMINATION_GUIDE.md)
