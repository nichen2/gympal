from flask import Flask, request, render_template, flash, redirect, session, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
import random
from models import connect_db, db, User, Exercise, Workout, WorkoutExercise
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///workout'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

connect_db(app)

toolbar = DebugToolbarExtension(app)

# Routes for user authentication and login
@app.before_request
def load_logged_in_user():
    user_id = session.get('username')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(username=user_id).first()

def auth():
    """Check user authentication and permissions."""
    if g.user is None:
        flash('Login first to view this page.', "primary")
        return redirect('/login')


@app.route("/register", methods=["GET","POST"])
def register():
    """Register a new user"""
    if 'username' in session:
        flash('Please log out to register new account', "primary")
        return redirect('/')
    
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken, please use another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Successfully Created Your Account!', "success")
        return redirect('/')
    return render_template("register.html",form=form)

@app.route("/login", methods=["GET","POST"])
def log_in():
    """User login"""
    if 'username' in session:
        flash('Already signed in', "primary")
        return redirect('/secret')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username,password)
        if (user):
            session['username'] = user.username
            flash('Welcome back', "primary")
            return redirect('/')
        else:
            form.password.errors.append('Incorrect username or password')
            return render_template("login.html",form=form)
    return render_template("login.html",form=form)

@app.route('/logout')
def logout_user():
    """User log out"""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')

@app.route('/profile')
def show_profile():
    """Shows the profile of the logged in user"""
    if g.user is None:
        return redirect('/login')
    return render_template('user_detail.html', user=g.user)
    
@app.route('/')
def home():
    """Home page"""
    if g.user is None:
        flash('Please log in or sign up.', "primary")
        return redirect('/login')
    return render_template('index.html', user=g.user)


# Exercise library routes
@app.route('/exercises')
def show_exercises():
    """Show exercises contained in the database"""
    muscles = Exercise.query.with_entities(Exercise.muscle).distinct().all()
    muscles_list = [muscle[0] for muscle in muscles]
    random.shuffle
    page = request.args.get('page', 1, type=int)  
    per_page = 25
    exercises = Exercise.query.order_by(db.func.random())
    paginated_exercises = exercises.paginate(page, per_page, error_out=False)
    return render_template('exercises.html', exercises=paginated_exercises.items, pagination=paginated_exercises, muscle_groups=muscles_list)

@app.route('/exercises/<muscle>')
def show_muscle_group(muscle):
    """Groups exercises by their muscle group"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    muscles = Exercise.query.with_entities(Exercise.muscle).distinct().all()
    muscles_list = [muscle[0] for muscle in muscles]
    exercises = Exercise.query.filter_by(muscle=muscle)
    paginated_exercises = exercises.paginate(page, per_page, error_out=False)
    return render_template('exercise_muscles.html', exercises=paginated_exercises.items, pagination=paginated_exercises, muscle_groups=muscles_list, muscle=muscle)

@app.route('/exercises/searchbar')
def search_exercises():
    """Parse search query from javascript front end"""
    query = request.args.get('q')
    if query:
        exercises = Exercise.query.filter(Exercise.name.ilike(f'%{query}%')).limit(10).all()
        results = [{'id': exercise.id, 'name': exercise.name} for exercise in exercises]
    else:
        results = []
    return jsonify(results)

@app.route('/exercises/search')
def show_search():
    """Show the search results from database"""
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    per_page = 25
    exercises = Exercise.query.filter(Exercise.name.ilike(f'%{query}%'))
    paginated_exercises = exercises.paginate(page, per_page, error_out=False)
    return render_template('exercise_search.html',exercises=paginated_exercises.items, pagination=paginated_exercises,query=query)

@app.route('/exercises/show/<int:exercise_id>')
def show_exercise(exercise_id):
    """Show exercise page of a specific exercise"""
    exercise = Exercise.query.get_or_404(exercise_id)
    return render_template('exercise_single.html', exercise=exercise)

# Workout builder routes
@app.route('/workouts')
def show_workouts():
    """Shows the user's workouts"""
    if g.user is None:
        return redirect('/login')
    user_id = g.user.id
    workouts = Workout.query.filter_by(user_id=user_id).all()
    return render_template('workouts.html', workouts=workouts)


@app.route('/workouts/builder')
def build_workout():
    """Build custom workouts"""
    if g.user is None:
        return redirect('/login')
    user = User.query.filter_by(username=session['username']).first()
    muscles = Exercise.query.with_entities(Exercise.muscle).distinct().all()
    muscles_list = [muscle[0] for muscle in muscles]
    return render_template('workout_builder.html', user=user, muscle_groups=muscles_list)

@app.route('/workouts/search')
def workout_search():
    """User search for specific exercises in workout builder"""
    if g.user is None:
        return redirect('/login')
    query = request.args.get('q')
    muscle = request.args.get('m')
    if query and muscle:
        exercises = Exercise.query.filter(Exercise.name.ilike(f'%{query}%')).filter_by(muscle=muscle).limit(10).all()
        results = [{'id': exercise.id, 'name': exercise.name} for exercise in exercises]
    elif query:
        exercises = Exercise.query.filter(Exercise.name.ilike(f'%{query}%')).limit(10).all()
        results = [{'id': exercise.id, 'name': exercise.name} for exercise in exercises]
    elif muscle:
        exercises = Exercise.query.filter_by(muscle=muscle)
        results = [{'id': exercise.id, 'name': exercise.name} for exercise in exercises]
    else:
        results = []
    return jsonify(results)

@app.route('/workouts/save_workout', methods=['POST'])
def save_workout():
    """Save workout to database"""
    if g.user is None:
        return redirect('/login')
    # Set up a new workout
    user = User.query.filter_by(username=session['username']).first()
    workout_data = request.json
    workout_name = workout_data.get('name')
    exercises = workout_data.get('exercises')
    workout = Workout(user_id=user.id,name=workout_name)
    db.session.add(workout)
    db.session.commit()

    # Unpack exercises from json object and assign it to this new workout
    for exercise in exercises:
        print(exercise)
        exercise_id = exercise.get('exerciseId')
        sets = exercise.get('sets')
        reps = exercise.get('reps')

        # create a relationship between the exercise and workout
        workout_exercise = WorkoutExercise(workout_id=workout.id, exercise_id=exercise_id, sets=sets, reps=reps)
        db.session.add(workout_exercise)
    
    db.session.commit()

    return jsonify({'message': 'Workout saved successfully'}), 200

@app.route('/workouts/<int:workout_id>')
def workout_detail(workout_id):
    """Show the exercises in a workout"""
    if g.user is None:
        return redirect('/login')
    workout = Workout.query.get_or_404(workout_id)
    workout_exercises = (db.session.query(WorkoutExercise, Exercise)
                         .join(Exercise, WorkoutExercise.exercise_id == Exercise.id)
                         .filter(WorkoutExercise.workout_id == workout_id)
                         .all())

    return render_template('workout_detail.html', workout=workout, workout_exercises=workout_exercises)

@app.route('/workouts/log')
def workout_log():
    """work in progress"""
    return render_template('workout_log.html')





