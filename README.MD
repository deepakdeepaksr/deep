morishield is a device for identifying pesticide drift in silk worm farms.for this identification we use a pcb board with sensors and a microcontroller.
a custom pcb, edgehax esp32 s3 (has built-in microSD slot for sensor data logging WHEN NO NETWORK and sync to server later).we use sensors like:
SGP41 — VOC/NOx air-quality (the primary drift signal), SHT45 — temperature/humidity
SPS30 — PM2.5/PM10 particulate, BME688 — gas/VOC
FDC1004 — 4-channel capacitance electrode (deposit on leaf/electrode at 1 m)
soil moisture probe (analog) and FSR (spray impact/weight)
reed switch anemometer for wind speed
GY-521 (MPU-6050) IMU and DS3231 RTC (plug-in modules)
and the carrier adds:
A7672S 4G LTE modem (SIM, J3/J4) + E22-900T22D LoRa (J6) for the uplink
TCA9548A 8-channel I²C multiplexer — each sensor gets its own switched 3.3 V channel (J11/J12/J13/J14/J21 + 2 spare)
TCA9535 16-bit I/O expander, TPS3823-33 watchdog, TPS7A2033 3.3 V LDO
5 V input at J18 with reverse-polarity/over-voltage FET protection, TVS + ESD arrays, PTC and ferrite; PE/earth at J19
user interface: panel LED pair (J24), 5 V buzzer (J25), external button (J23), on-board tactile switch + status LEDs