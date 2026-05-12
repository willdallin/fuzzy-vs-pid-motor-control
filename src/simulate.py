import os
import numpy as np
import matplotlib.pyplot as plt
from motor_plant import MotorPlant
from controller_fuzzy import FuzzyController
from controller_pid import PIDController

def run_simulation():
    dt = 0.01
    time = np.arange(0, 10, dt)
    target_rpm = 100.0
    load_step_time = 5.0
    load_torque_value = 0.02
    
    plant = MotorPlant()
    pid = PIDController(kp=0.2, ki=1.5, kd=0.005)
    fuzzy = FuzzyController()
    
    pid_rpm = []
    fuz_rpm = []
    
    # PID Simulation
    plant.reset()
    pid.reset()
    for t in time:
        torque = load_torque_value if t >= load_step_time else 0.0
        current_rpm = plant.omega * (60.0 / (2 * np.pi))
        error = target_rpm - current_rpm
        
        voltage = pid.compute(error, dt)
        plant.update(voltage, torque, dt)
        pid_rpm.append(current_rpm)
        
    # Fuzzy Simulation
    plant.reset()
    fuzzy.reset()
    prev_error = target_rpm
    for t in time:
        torque = load_torque_value if t >= load_step_time else 0.0
        current_rpm = plant.omega * (60.0 / (2 * np.pi))
        error = target_rpm - current_rpm
        delta_error = (error - prev_error) / dt
        
        err_in = max(-200, min(200, error))
        derr_in = max(-100, min(100, delta_error))
        
        voltage = fuzzy.compute(err_in, derr_in)
        plant.update(voltage, torque, dt)
        
        prev_error = error
        fuz_rpm.append(current_rpm)

    save_plot(time, pid_rpm, fuz_rpm, target_rpm, load_step_time)

def save_plot(time, pid_rpm, fuz_rpm, target_rpm, load_step_time):
    os.makedirs("../results", exist_ok=True)
    plt.figure(figsize=(10, 5))
    
    plt.plot(time, pid_rpm, label="PID Controller", color="#1f77b4", linewidth=2)
    plt.plot(time, fuz_rpm, label="Fuzzy Controller", color="#ff7f0e", linewidth=2)
    plt.axhline(target_rpm, color="r", linestyle="--", label="Setpoint")
    plt.axvline(load_step_time, color="gray", linestyle=":", label="Load Disturbance")
    
    plt.title("Motor Speed Control: PID vs Fuzzy")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (RPM)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_path = "../results/comparison.png"
    plt.savefig(output_path)
    print(f"Simulation completed successfully. Plot saved to: {output_path}")

if __name__ == "__main__":
    run_simulation()