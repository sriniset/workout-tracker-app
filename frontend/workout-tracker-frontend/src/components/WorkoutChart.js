import React, { useEffect, useState} from 'react';
import axios from '../services/api';

function WorkoutChart({selectedType, chartReload}) {
    const [chartUrl, setChartUrl] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const getChart = async () => {
            try{
                const response = await axios.get(`/workoutChart/${selectedType}`, {
                    responseType: 'blob',
                });
                
                if (response.data.size === 0){
                    setError('No workouts to make chart!')
                }

                else{
                    const imageUrl = URL.createObjectURL(response.data);
                    setChartUrl(imageUrl);
                    setError('')
                }
                
            }

            catch (error)  {
                console.error("Error getting chart:", error)
            }
        };

        getChart();
    }, [selectedType, chartReload]);

    return (
        <div className="workout-chart">
            <h2>Workout Chart</h2>
            {error && <p>{error}</p>}
            {chartUrl && <img src={chartUrl} alt="Workout Chart" />}
        </div>
    );
}

export default WorkoutChart