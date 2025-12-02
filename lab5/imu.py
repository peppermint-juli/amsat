
# imu.py
import time, math
from smbus2 import SMBus

I2C_BUS   = 1
MPU_ADDR  = 0x68  # change to 0x69 if AD0 is pulled high
# Registers
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43

# Scale factors for default ranges: ±2g, ±250 dps
ACC_SCALE = 16384.0
GYR_SCALE = 131.0

class MPU6050:
    def __init__(self, addr=MPU_ADDR, busnum=I2C_BUS):
        self.bus = SMBus(busnum)
        self.addr = addr
        # Wake up device
        self.bus.write_byte_data(self.addr, PWR_MGMT_1, 0)
        time.sleep(0.05)
        # Bias offsets (measure at rest and update these)
        self.gyro_bias = {'x':0.0, 'y':0.0, 'z':0.0}
        self.acc_bias  = {'x':0.0, 'y':0.0, 'z':0.0}

    def _read_word(self, reg):
        hi = self.bus.read_byte_data(self.addr, reg)
        lo = self.bus.read_byte_data(self.addr, reg+1)
        val = (hi << 8) | lo
        return val - 65536 if val >= 0x8000 else val

    def read(self):
        ax = self._read_word(ACCEL_XOUT_H)
        ay = self._read_word(ACCEL_XOUT_H+2)
        az = self._read_word(ACCEL_XOUT_H+4)
        gx = self._read_word(GYRO_XOUT_H)
        gy = self._read_word(GYRO_XOUT_H+2)
        gz = self._read_word(GYRO_XOUT_H+4)
        # Scale
        ax, ay, az = ax/ACC_SCALE, ay/ACC_SCALE, az/ACC_SCALE
        gx, gy, gz = gx/GYR_SCALE, gy/GYR_SCALE, gz/GYR_SCALE
        # Apply simple static biases
        ax -= self.acc_bias['x']; ay -= self.acc_bias['y']; az -= self.acc_bias['z']
        gx -= self.gyro_bias['x']; gy -= self.gyro_bias['y']; gz -= self.gyro_bias['z']
        return ax, ay, az, gx, gy, gz

# Complementary filter for fused orientation
class ComplementaryFilter:
    def __init__(self, alpha=0.98):
        self.alpha = alpha
        # Initialize with level from accelerometer
        self.pitch = 0.0; self.roll = 0.0; self.yaw = 0.0
        self._initialized = False

    @staticmethod
    def accel_angles(ax, ay, az):
        # Roll: rotation around X; Pitch: around Y
        roll  = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))
        return pitch, roll

    def update(self, ax, ay, az, gx, gy, gz, dt):
        # gyro integration
        pitch_gyro = self.pitch + gy * dt
        roll_gyro  = self.roll  + gx * dt
        yaw_gyro   = self.yaw   + gz * dt   # will drift without magnetometer

        pitch_acc, roll_acc = self.accel_angles(ax, ay, az)

        a = self.alpha
        self.pitch = a * pitch_gyro + (1 - a) * pitch_acc
        self.roll  = a * roll_gyro  + (1 - a) * roll_acc
        self.yaw   = yaw_gyro
        return self.yaw, self.pitch, self.roll

def orientation_stream(addr=MPU_ADDR, hz=60):
    mpu = MPU6050(addr)
    filt = ComplementaryFilter(alpha=0.98)
    period = 1.0 / hz
    last = time.perf_counter()
    # Initialize with first accel read
    ax, ay, az, gx, gy, gz = mpu.read()
    pitch0, roll0 = filt.accel_angles(ax, ay, az)
    filt.pitch, filt.roll = pitch0, roll0
    while True:
        now = time.perf_counter()
        dt = now - last
        if dt < period:
            time.sleep(period - dt)
            continue
        last = now
        ax, ay, az, gx, gy, gz = mpu.read()
        yaw, pitch, roll = filt.update(ax, ay, az, gx, gy, gz, dt)
        yield {'yaw': yaw, 'pitch': pitch, 'roll': roll, 'dt_ms': int(dt*1000)}
