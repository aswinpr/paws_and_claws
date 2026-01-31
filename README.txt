PAWS AND CLAWS – Django + MongoDB Project
========================================

This is a Django-based web application that uses MongoDB as the database.
Sensitive information such as the MongoDB connection string is secured
using environment variables and is NOT included in this repository.

--------------------------------------------------
PROJECT SETUP INSTRUCTIONS
--------------------------------------------------

1. Download or Clone the Project
-------------------------------
If downloaded as ZIP:
- Extract the ZIP file to any folder

If using Git:
git clone <repository_url>
cd paws_and_claws


2. Create and Activate Virtual Environment
------------------------------------------
python -m venv venv

Activate (Windows):
venv\Scripts\activate

Activate (Linux / Mac):
source venv/bin/activate


3. Install Required Packages
----------------------------
pip install -r requirements.txt


4. Environment Variable Setup (IMPORTANT)
-----------------------------------------
This project uses a MongoDB database.
For security reasons, the MongoDB URI is NOT included in the code.

Create a file named `.env` in the project root
(same folder as manage.py)

Add the following line to the .env file:

MONGO_URI=your_mongodb_connection_string_here


Example:
MONGO_URI=REMOVED_MONGO_URIusername:password@cluster.mongodb.net/dbname


5. Run the Django Server
-----------------------
python manage.py runserver

Open your browser and go to:
http://127.0.0.1:8000/


--------------------------------------------------
SECURITY NOTE
--------------------------------------------------
- Sensitive credentials are managed using environment variables
- The `.env` file is ignored using `.gitignore`
- This follows industry-standard security practices


--------------------------------------------------
TECHNOLOGIES USED
--------------------------------------------------
- Python
- Django
- MongoDB
- PyMongo
- HTML, CSS, JavaScript


--------------------------------------------------
IMPORTANT
--------------------------------------------------
If the project does not start, ensure:
- Python is installed
- Virtual environment is activated
- All dependencies are installed
- `.env` file exists and contains MONGO_URI

--------------------------------------------------
