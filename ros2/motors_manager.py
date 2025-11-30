import board
import busio

# Initiera I2C-bussen
i2c = busio.I2C(board.SCL, board.SDA)

print("Trying to lock I2C bus...")
while not i2c.try_lock():
    pass

print("I2C bus locked successfully.")

# Försök “scanna” – kommer vara tomt om ingen enhet finns
devices = i2c.scan()

if devices:
    print("Found I2C device(s) at addresses:", [hex(d) for d in devices])
else:
    print("No I2C devices found (normal if no hardware is connected)")

# Lås upp bussen och stäng
i2c.unlock()
i2c.deinit()
print("I2C bus cleaned up and released.")
