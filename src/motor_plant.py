import math

class MotorPlant:
    def __init__(self, J=0.01, b=0.001, K=0.1, R=1.0, L=0.05):
        self.J = J
        self.b = b
        self.K = K
        self.R = R
        self.L = L
        self.omega = 0.0
        self.current = 0.0

    def update(self, voltage, load_torque, dt):
        voltage = max(-24.0, min(24.0, voltage))
        
        di_dt = (voltage - self.R * self.current - self.K * self.omega) / self.L
        domega_dt = (self.K * self.current - self.b * self.omega - load_torque) / self.J
        
        self.current += di_dt * dt
        self.omega += domega_dt * dt
        
        rpm = self.omega * (60.0 / (2 * math.pi))
        return rpm

    def reset(self):
        self.omega = 0.0
        self.current = 0.0