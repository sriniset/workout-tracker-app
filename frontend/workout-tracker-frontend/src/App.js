import './App.css';
import React, {useEffect, useState} from 'react';
import axios from './services/api';
import NavBar from './components/NavBar';
import AddWorkout from './components/AddWorkout';
import WorkoutChart from './components/WorkoutChart';


function App() {
  
  const [workoutTypes, setWorkoutTypes] = useState([]);
  const [selectedType, setSelectedType] = useState('');
  const [chartReload, setChartReload] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    const getWorkoutTypes = async () => {
    try{
      const response = await axios.get('/getWorkoutTypes');
      setWorkoutTypes(response.data)
      setSelectedType(response.data[0]);
    } catch (error) {
      console.error("Could not get workout types:", error)
    }
  };
  
  getWorkoutTypes();
 }, []); 

  const handleWorkoutAdded = (message) => {
    console.log(message)
    setChartReload(!chartReload)
    setResponseMessage(message)
    setIsError(false);
    setTimeout(() => {
      setResponseMessage('');
  }, 2000);
  };

  const handleAddWorkoutError = (errorMessage) => {
    console.log(errorMessage)
    setResponseMessage(errorMessage);
    setIsError(true)
    setTimeout(() => {
      setResponseMessage('');
  }, 2000);
  }



  return (
    <div className='App'>
      <NavBar
        workoutTypes={workoutTypes}
        selectedType={selectedType}
        onTypeChange={setSelectedType} />

        <div className="content">
          <AddWorkout selectedType={selectedType} 
          onWorkoutAdded={handleWorkoutAdded} 
          responseMessage={responseMessage} 
          onError = {handleAddWorkoutError}
          isError={isError}/>
          <WorkoutChart selectedType={selectedType} chartReload={chartReload}/>
        </div>
    </div>
  );
}

export default App;
