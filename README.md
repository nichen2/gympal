# Gym Pal

## Description
Gym Pal is a full-stack web application designed to serve as a utility for users to manage and keep track of their fitness routines. Users can create, track, and log workouts. Users are also able to browse a library containing 200+ exercises, filter them by muscle group, and add them to their own custom workouts. The live deployed web app can be found here:  [Gym Pal](https://gympal-q64r.onrender.com/)

## Features

- **User Authentication**: Secure login and registration system to manage user accounts.
- **Exercise Library**: Browse exercises by name or muscle group, with detailed instructions and difficulty levels.
- **Workout Builder**: Dynamically create custom workouts by adding exercises from the library. Specify sets and reps for each exercise.
- **Workout Log**: Keep track of completed workouts, including details about exercises, sets, and reps.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap for styling), JavaScript (jQuery for dynamic content)
- **Backend**: Python, Flask (for server-side logic), SQLAlchemy (ORM for database interactions)
- **API/Database**: PostgreSQL, APINinjas' ExerciseAPI
- **Deployment**: Render

## Database Schema Diagram
![database-schema](https://github.com/user-attachments/assets/56c24910-a659-4822-9c2e-e222804ecd81)


## Setup Instructions

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository:**
   git clone https://github.com/username/gym-pal.git
   cd gym-pal

2. **Create the virtual environment:**
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Set up the database:**
   psql -U your_username -c "CREATE DATABASE gym_pal_db;"

5. **Run the populate_db.py script**:
   populate_db.py


