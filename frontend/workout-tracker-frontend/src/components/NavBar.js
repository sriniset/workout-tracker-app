import React from "react";
import axios from '../services/api';

function NavBar({workoutTypes, selectedType, onTypeChange}) {
    return (
        <div className = "nav-bar">
            <select value = {selectedType} onChange={e => onTypeChange(e.target.value)}>
                {workoutTypes.map((type, index) => (
                    <option key={index} value={type}>{type}</option>
                ))}
            </select>
        </div>
    );
}

export default NavBar;