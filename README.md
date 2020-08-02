# Elevator Model

Small project which uses the pygame module to show an elevator moving up and down. The elevator picks up passengers and drops them off at other locations.


## Elevator Modes

There are two modes avaliable in this program:
 * Linear - Elevator moves up and down the page
 * First come first serve - Elevator picks up the first passenger which spawns and drops them off at their destination. Passengers are picked up in order of spawning.
 
 
## Getting Started

When selecting which mode to use, change the parameter 'mode' to either 'linear' or 'first_come' in the main.py file.

```
ElevatorSim(floors, elevator, passengers, speed, mode)
```

For example

```
ElevatorSim(floors, elevator, passengers, speed, 'linear')
ElevatorSim(floors, elevator, passengers, speed, 'first_come')
```


## Simulation Modes 

The program can either simulate the program with or without pygame. Using pygame will take longer, however the program visually shows the model. However, when not using the pygame animation the simulation runs much quicker until the time limit is reached - 1000 seconds by default.

Using pygame animation:
```
ElevatorSim(floors, elevator, passengers, speed, mode).py_animation()
```
Otherwise simulate the model:
```
ElevatorSim(floors, elevator, passengers, speed, mode).simulation()
```

## Running Application

By default the model will have four floors, no passengers present. Also the elevator mode will be 'linear' and the simulation mode will be 'py_animation'. Once all the correct modes, floors and passengers are inputted, run the elevator.py file.
