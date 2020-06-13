import serial
from datetime import datetime


START_BYTES = [0x42, 0x4D]
# 32 - 2 start bytes
FRAME_LENGTH = 30

s = serial.Serial(
    port="COM6",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=2,
)

try:
    while True:
        s.read_until(START_BYTES)
        data = s.read(size=FRAME_LENGTH)
        if len(data) != FRAME_LENGTH:
            print("Error reading serial...")
            continue
        data = list(data)
        data_pairs = [(data[e], data[e + 1]) for e in range(0, FRAME_LENGTH, 2)]
        glued = [f[0] << 8 | f[1] for f in data_pairs]
        print(data, "\n", data_pairs, "\n", glued)
        with open("data.csv", "a+", encoding="utf-8") as f:
            f.write(str(datetime.now()))
            f.write("\n")
            f.write(str(glued))
            f.write("\n")
            f.write(str(data_pairs))
            f.write("\n")
finally:
    print("Closing serial connetion...")
    s.close()
    print("Serial closed:", not s.is_open)
