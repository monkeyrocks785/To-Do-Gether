@echo off
REM ============================================
REM To-Do-Gether - Collaborative Todo App
REM ============================================
REM This script sets up the entire project structure
REM with virtual environment and dependencies
REM Cute theme: Warm peachy tones (#eab676 palette)
REM ============================================

echo.
echo ========================================
echo    TO-DO-GETHER - PROJECT SETUP
echo ========================================
echo    ^(Collaborative Todo Magic^^!^)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found!
echo.

REM Create project folder structure
echo [*] Creating folder structure...
mkdir templates
mkdir static\css
mkdir static\js
mkdir static\images
echo [✓] Folders created!
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv
echo [✓] Virtual environment created!
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated!
echo.

REM Create requirements.txt
echo [*] Creating requirements.txt...
(
    echo Flask==2.3.3
    echo Flask-SQLAlchemy==3.0.5
    echo Flask-Login==0.6.2
    echo Werkzeug==2.3.7
    echo python-dotenv==1.0.0
) > requirements.txt
echo [✓] requirements.txt created!
echo.

REM Install dependencies
echo [*] Installing dependencies (this may take a moment)...
pip install -r requirements.txt
echo [✓] Dependencies installed!
echo.

REM Create .gitignore
echo [*] Creating .gitignore...
(
    echo # Virtual Environment
    echo venv/
    echo env/
    echo ENV/
    echo.
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo *.so
    echo .Python
    echo build/
    echo develop-eggs/
    echo dist/
    echo downloads/
    echo eggs/
    echo .eggs/
    echo lib/
    echo lib64/
    echo parts/
    echo sdist/
    echo var/
    echo wheels/
    echo *.egg-info/
    echo .installed.cfg
    echo *.egg
    echo.
    echo # Flask
    echo instance/
    echo .webassets-cache
    echo.
    echo # Database
    echo *.db
    echo *.sqlite
    echo *.sqlite3
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo *.swp
    echo *.swo
    echo *~
    echo .DS_Store
    echo.
    echo # Environment variables
    echo .env
    echo .env.local
) > .gitignore
echo [✓] .gitignore created!
echo.

REM Create .env template
echo [*] Creating .env template...
(
    echo # Flask Configuration
    echo FLASK_ENV=development
    echo FLASK_APP=app.py
    echo SECRET_KEY=your-secret-key-here-change-in-production
) > .env.example
echo [✓] .env.example created!
echo.

REM Create placeholder files
echo [*] Creating placeholder files...
(
    echo # To-Do-Gether - Collaborative Todo App
    echo ## A cute shared task manager for you and your friends
    echo.
    echo ### Theme
    echo - Color Palette: Warm peachy tones (#eab676 and variations^)
    echo - Vibe: Cute, cozy, collaborative
    echo.
    echo ### Setup
    echo Run `setup.bat` to initialize the project.
    echo.
    echo ### Development
    echo 1. Virtual environment is auto-activated after setup
    echo 2. Run app: `python app.py`
    echo 3. Visit: `http://localhost:5000`
    echo.
    echo ### Features
    echo - Collaborative Todo Lists
    echo - Real-time shared viewing
    echo - Date/Day/Time display
    echo - User Authentication
    echo - Edit/Delete/Reorder todos
    echo - Cross-user todo management
) > README.md
echo [✓] README.md created!
echo.

(
    echo # Flask Configuration
    echo import os
    echo from dotenv import load_dotenv
    echo.
    echo load_dotenv^(^)
    echo.
    echo class Config:
    echo     """Base configuration"""
    echo     SQLALCHEMY_DATABASE_URI = 'sqlite:///todos.db'
    echo     SECRET_KEY = os.environ.get^('SECRET_KEY'^) or 'dev-secret-key-change-in-production'
    echo     SQLALCHEMY_TRACK_MODIFICATIONS = False
) > config.py
echo [✓] config.py created!
echo.

(
    echo # Flask App Entry Point
    echo # TODO: Add main Flask app setup here
) > app.py
echo [✓] app.py created!
echo.

(
    echo # Database Models
    echo # TODO: Add User and Todo models here
) > models.py
echo [✓] models.py created!
echo.

(
    echo /* To-Do-Gether - Cute CSS Styling */
    echo /* Color Palette: Warm peachy tones (#eab676 variations) */
    echo /* TODO: Add styling here in Phase 2 */
) > static\css\style.css
echo [✓] style.css created!
echo.

(
    echo // To-Do-Gether Interactive JavaScript
    echo // TODO: Add interactivity here in Phase 2
) > static\js\script.js
echo [✓] script.js created!
echo.

REM Create .git initialization instructions
echo [*] Git initialization info...
echo [!] To initialize git, run: git init
echo [!] Then: git add . ^& git commit -m "Initial To-Do-Gether setup"
echo.

REM Final summary
echo.
echo ========================================
echo    SETUP COMPLETE! 🎉
echo ========================================
echo.
echo Project: TO-DO-GETHER
echo Theme: Cute ^& Cozy (Peachy Palette^)
echo.
echo Project Structure:
echo.
echo to-do-gether/
echo ├── venv/                 (Virtual Environment^)
echo ├── templates/            (HTML templates^)
echo ├── static/
echo │   ├── css/style.css     (Cute styling^)
echo │   ├── js/script.js      (Interactivity^)
echo │   └── images/           (Assets^)
echo ├── app.py               (Main Flask app^)
echo ├── models.py            (Database models^)
echo ├── config.py            (Configuration^)
echo ├── requirements.txt     (Dependencies^)
echo ├── .gitignore
echo ├── .env.example
echo ├── README.md
echo └── todos.db             (Database - created on first run^)
echo.
echo Next Steps:
echo.
echo 1. Virtual environment is already active!
echo 2. Run: python app.py
echo 3. Visit: http://localhost:5000
echo.
echo Let's build something adorable! 💕
echo.
pause
