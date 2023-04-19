export function plantSeed(name, lifecycleDurations, caloriesPerCycle) {
    return {
      name,
      lifecycleStages: ["seed"],
      lifecycleDurations,
      caloriesPerCycle,
      currentCycle: 1,
    };
  }
  
  export function growPlant(plant) {
    const currentStage = plant.lifecycleStages[plant.currentCycle - 1];
    const nextCycle = plant.currentCycle + 1;
    if (nextCycle > plant.lifecycleDurations.length) {
      // Plant has reached end of life cycle
      return null;
    }
    const nextStage = plant.lifecycleStages[nextCycle - 1];
    const caloriesProduced =
      (plant.caloriesPerCycle * plant.lifecycleDurations[nextCycle - 1]) / 5; // Divide by 5 for 5 seconds in a day
    return {
      ...plant,
      lifecycleStages: plant.lifecycleStages.slice(0, nextCycle),
      currentCycle: nextCycle,
      caloriesProduced,
    };
  }
  