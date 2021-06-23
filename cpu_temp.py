import wmi


class CPU_temp:
    def __init__(self):
        self.load_wmi = wmi.WMI(namespace="root\OpenHardwareMonitor")
        self.temperature_infos = self.load_wmi.Sensor()

    def read_cpu_package_temp(self):
        for sensor in self.temperature_infos:
            if sensor.SensorType == u'Temperature' and sensor.Name == u'CPU Package':
                return sensor.Value


if __name__ == "__main__":
    cputmp = CPU_temp()
    cputmp.read_cpu_package_temp()
