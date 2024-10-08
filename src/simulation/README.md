# Simulation of traffic flow and traffic signal deployment scenarios

[site](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41597-022-01448-6/MediaObjects/41597_2022_1448_Fig2_HTML.png?as=webp)

### Scenario 1: Rule-Based or Fixed Timing 
- Fixed green-red cycle length, e.g., 60 seconds each.
- No adaptation based on traffic density.
- View simulation [here](https://streamable.com/26y91c)

### Scenario 2: Dynamic Deployment Based on Traffic Flow Forecast (Proposed Approach)
- Forecast vehicle counts and queues at each link of the intersection.
- Adjust green light duration based on predicted traffic density.
- Prioritize directions with heavier traffic flow. (??)
- Heuristics or RL-based system


### To Do
- [x] **Set up simulation environment** (SUMO).
- [x] **Define the traffic network** using OpenStreetMap (OSM) data.
- [x] **Generate synthetic traffic flows** (randomTrips.py in SUMO) for realistic simulations.
- [x] **Implement fixed-time signal control** for all traffic signals.
- [ ] **Integrate traffic flow forecast model** (trained Temporal Fusion Transformer) into the simulation.
- [ ] **Implement dynamic traffic signal control**:
- [ ] **Visualize the traffic movement and traffic light phases** as shown in the .
- [ ] **Collect performance metrics**:
  - Average vehicle wait time.
  - Queue lengths at intersections.
  - Overall throughput (number of vehicles passing through in a given time).
- [ ] **Compare fixed vs dynamic deploymnt scenarios**
- [ ] **Validate on real-world dataset**: (Optional)
