# Elevator Model

Small project which uses the pygame module to show an elevator moving up and down. The elevator picks up passengers and drops them off at other locations.

## Elevator Modes

There are two modes avaliable in this program:
 * Linear - Elevator moves up and down the page
 * First Come first serve - Elevator picks up the first passenger which spawns and drops them off at their destination, then picks up the passenger which spawns next.
 
## Getting Started

When selecting which mode to use, change the mode parameter 'mode' to either 'linear' or 'first_come' in the main.py file.

```
ElevatorSim(floors, elevator, passengers, 100, 2, mode)
```

For example

```
ElevatorSim(floors, elevator, passengers, 100, 2, 'linear')
ElevatorSim(floors, elevator, passengers, 100, 2, 'first_come')
```

## Running Application

After selecting the mode you would like to use, run the main.py file
