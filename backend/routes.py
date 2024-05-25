from flask import request, jsonify, Response, abort
from app import app, db 
from dataModel import Workout
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

@app.errorhandler(400)
def handleError(error):
    return jsonify(error=str(error.description)), 400

#home route
@app.route('/')
def index():
    return 'Welcome to workout tracker!'

#route to add new workout
#example payload: 
# {
#   "type": "running",
#   "duration": 60,
#   "date": "2024-05-21"
# }
#can only add one workout per day of distinct type, for simplicity
@app.route('/addWorkout', methods=['POST'])
def addWorkout():
    data = request.get_json()
    
    workoutType = data.get('type')
    duration = data.get('duration')
    dateString = data.get('date')

    if not workoutType or not duration or not dateString:
        abort(400, description="Need type, duration, and date to make new workout!")

    try: 
        date = datetime.strptime(dateString, '%Y-%m-%d').date()
    except ValueError:
        abort(400, description="Date format not valid. Please use YYYY-MM-DD")
    
    workoutExists = Workout.query.filter_by(type=workoutType, date=date).first()
    
    if workoutExists:
        abort(400, description=f"{workoutType.capitalize()} workout for {dateString} already exists!")

    workout = Workout(
        type = data['type'],
        duration = data['duration'],
        date = datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(workout)
    db.session.commit()
    return "New workout added!", 201

#route to get all workouts
@app.route('/getWorkouts', methods=['GET'])
def getWorkouts():
    allWorkouts = Workout.query.all()
    return jsonify([{
        'type': workout.type,
        'duration': workout.duration,
        'date': workout.date.strftime('%Y-%m-%d')
    } for workout in allWorkouts])

#route to get all workouts of a specific type
@app.route('/getWorkouts/<workoutType>', methods=['GET'])
def getWorkoutsByType(workoutType):
    workoutsByType = Workout.query.filter_by(type=workoutType).all()
    return jsonify([{
        'type': workout.type,
        'duration': workout.duration,
        'date': workout.date.strftime('%Y-%m-%d')
    } for workout in workoutsByType])

#route to get all the workout types 
@app.route('/getWorkoutTypes', methods=['GET'])
def getWorkoutTypes():
    workoutTypes = db.session.query(Workout.type).distinct().all()
    workoutTypesList = [type[0] for type in workoutTypes]
    return jsonify(workoutTypesList)

#route to generate workout chart using matplotlib
#for a workout type, if there are gaps in working out, will generate dates with duration of 0
@app.route('/workoutChart/<workoutType>', methods=['GET'])
def generateWorkoutChart(workoutType):
    workouts = Workout.query.filter_by(type=workoutType).order_by(Workout.date).all()
    startDate = workouts[0].date
    endDate = workouts[-1].date
    dateRange = [startDate + timedelta(days=dur) for dur in range((endDate - startDate).days + 1)]
    workoutDict = {workout.date:workout.duration for workout in workouts}
    workoutDurationsPerDay = [workoutDict.get(date, 0) for date in dateRange]

    plt.figure()
    plt.plot(dateRange, workoutDurationsPerDay, marker='o')
    plt.title(f'{workoutType.capitalize()} Workouts Duration Over Time')
    plt.xlabel('Date')
    plt.ylabel('Duration (min)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

#route to delete workouts based on id
@app.route('/deleteWorkout/<int:id>', methods=['DELETE'])
def deleteWorkout(id):
    workout = Workout.query.get(id)
    if not workout:
        abort(404, description=f"No workout with id {id} in database")
    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": f"Workout {id} is deleted!"})