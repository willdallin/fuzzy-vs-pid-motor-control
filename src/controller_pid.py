class PIDController:
    def __init__(self, kp, ki, kd, output_limits=(-24.0, 24.0)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min_out, self.max_out = output_limits
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, error, dt):
        self.integral += error * dt
        
        if self.ki != 0:
            self.integral = max(self.min_out / self.ki, min(self.max_out / self.ki, self.integral))
            
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        output = max(self.min_out, min(self.max_out, output))
        
        self.prev_error = error
        return output

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0