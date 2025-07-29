import csv
import matplotlib.pyplot as plt
import numpy as np
#from controller_GridSearch import PIDController
from controller_NelderMead import PIDController





def read_waypoints(file_path):
    times = []
    speeds = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            speeds.append(float(row[0]))
            times.append(float(row[1]))
    return times, speeds




def simulate(times, speeds, pid_controller, dt, total_time, initial_speed=0):
    time_steps = int(total_time / dt)
    sim_times = np.linspace(0, total_time, time_steps)
    sim_speeds = np.zeros(time_steps)
    current_speed = initial_speed

    for i in range(1, time_steps):
        target_speed = np.interp(sim_times[i], times, speeds)
        control_signal = pid_controller.control(target_speed, current_speed, dt)
        current_speed += control_signal * dt
        sim_speeds[i] = current_speed

    return sim_times, sim_speeds




def grade_performance(actual_speeds, target_speeds):
    error = np.array(actual_speeds) - np.array(target_speeds)
    mse = np.mean(np.square(error))
    return mse




def main():
    times, speeds = read_waypoints('waypointsNew.csv')
     
    dt = 0.1
    total_time = 179
    initial_speed = 0


    #######################################################################################################
    ######################### Apply your tuned parameters to the controller class #########################
    #######################################################################################################
    kp=0.01                                                        
    ki=0.01
    kd=0.01
    pid_controller = PIDController(kp, ki, kd)
    #######################################################################################################
    #######################################################################################################

    
    sim_times, sim_speeds = simulate(times, speeds, pid_controller, dt, total_time, initial_speed)
    
    target_speeds = np.interp(sim_times, times, speeds)
    mse = grade_performance(sim_speeds, target_speeds)
    print(f'Mean Squared Error: {mse}')
    
    plt.plot(sim_times, sim_speeds, label='Speed', color='black')
    plt.plot(sim_times, target_speeds, label='Target Speed', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()