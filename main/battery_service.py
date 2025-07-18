class BatMonitor():
    """A simple class to encapsulate battery state."""
    def __init__(self, battery_status, limit):
        self.percentage = battery_status.percent
        self.is_charging = battery_status.power_plugged
        self.limit = limit

    def limit_reached(self):
        """Check if the current percentage has reached the set limit."""
        return self.percentage >= self.limit

    def is_plugged_in(self):
        """Check if the device is plugged in and charging."""
        return self.is_charging
