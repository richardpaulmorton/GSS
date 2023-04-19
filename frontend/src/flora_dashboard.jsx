import React, { useState, useEffect } from 'react';

function FloraDashboard() {
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    async function fetchPlants() {
      const response = await fetch('/plants.csv');
      const csv = await response.text();
      const lines = csv.trim().split('\n');
      const headers = lines[0].split(',');
      const data = lines.slice(1).map((line) => {
        const values = line.split(',');
        return headers.reduce((obj, header, i) => {
          obj[header] = values[i];
          return obj;
        }, {});
      });
      setPlants(data);
    }

    fetchPlants();
  }, []);

  function handlePlantSeed(plantName) {
    // Find the index of the plant with the specified name
    const index = plants.findIndex((plant) => plant.name === plantName);

    // Create a copy of the plant object and update its lifecycle stages
    const updatedPlant = { ...plants[index] };
    updatedPlant.lifecycleStages = 'seedling';

    // Replace the old plant object with the updated one in the plants array
    const updatedPlants = [...plants];
    updatedPlants[index] = updatedPlant;

    // Update the plants state with the new array
    setPlants(updatedPlants);
  }

  return (
    <div>
      <h1>Available Plants</h1>
      <ul>
        {plants.map((plant) => (
          <li key={plant.name}>{plant.name}</li>
        ))}
      </ul>
      <button onClick={() => handlePlantSeed('Carrots')}>Plant Carrot Seed</button>
      {/* Add buttons for other plant types here */}
    </div>
  );
}

export default FloraDashboard;
