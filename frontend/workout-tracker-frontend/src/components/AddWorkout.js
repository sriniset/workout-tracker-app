import React, { useState } from "react";
import axios from '../services/api';
import DatePicker from "react-datepicker";
import 'react-datepicker/dist/react-datepicker.css';

function AddWorkout({ selectedType, onWorkoutAdded, responseMessage, isError, onError}) {
    const [duration, setDuration] = useState('');
    const [date, setDate] = useState(new Date());
    

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await axios.post('/addWorkout', {
                type: selectedType,
                duration: parseInt(duration, 10),
                date: date.toISOString().split('T')[0],
            });
            onWorkoutAdded(response.data);
            setDuration('');
            setDate(new Date());
        }
        catch (error){
            console.error("Cannot add workout: ", error);
            onError(error.response.data.error)
            setDuration('');
            setDate(new Date());
        }
    };


return (
    <div className="add-workout">
        <h2>Add New Workout</h2>
        <form onSubmit={handleSubmit}>
            <div>
                <label>Date:</label>
                <DatePicker selected={date} onChange={date => setDate(date)} />
            </div>
            <div>
                <label>Duration (minutes):</label>
                <input
                type="number"
                value={duration}
                onChange={e => setDuration(e.target.value)}
                required />
            </div>
            <button type="submit">Add Workout</button>
            {responseMessage && 
            (<p className={`response-message ${isError ? 'error' : 'success'}`}>{responseMessage}</p>
        )}
        </form>
    </div>
);
}



export default AddWorkout;