# BARE MASTER TO BUILD AUG 2025  FOR 1OF3  
import runloop, motor_pair, motor , color, time
from hub import motion_sensor, light_matrix, light, port,button
import math
from math import pi, radians
from time import sleep, sleep_ms
# from typing import TYPE_CHECKING

# INITIALIZE
COUNT_MAX=5         # NUMBER OF MISSIONS
motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)      # COACH BOT A,B  TWIN  A,E  1OF3  A,B
distance_motor = port.E                                 # COACH  B   TWIN  E
DEGREE_INCH = 51.4              # COACH 51.4,   TWIN  33
ARM_FRONT_PORT = port.C         # COACH  C,  TWIN  D   1OF3  C  RIGHT
ARM_BACK_PORT = port.D          # COACH  D,  TWIN  C   1OF3  D  LEFT
motion_sensor.set_yaw_face(motion_sensor.FRONT)
drive_motors = motor_pair.PAIR_1
TRUE = 1
FALSE = 0
PR_LETTER=['A','B','C','D','E','F','G','H','I','J','K']

#FUNCTIONS
async def WALL_SQUARE():    # square by backing against the wall
    await motor_pair.move_for_time(motor_pair.PAIR_1, 500, 0, velocity=-400)
    #500 milliseconds, straight,at -400 ~40% backup
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    sleep_ms(50)

async def MOV_INCHES(inc_dist,fast_slo):        # move inches at speed
    deg_inch = int(DEGREE_INCH * inc_dist )
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_inch , 0, velocity=fast_slo)   #52*inc_dist

async def ARMFRONT(degrees, power):
    motor.run_for_degrees(port.D, degrees, power)# '-' is downPORT, DEGREES, POWER

async def ARM_BACK(degrees, power):
    await motor.run_for_degrees(port.C, degrees, power)

async def ARM_MOTOR( arm_port, degrees, power):       # SHARE ARM FUNCTION?
    await motor.run_for_degrees(arm_port,degrees,power)

async def GYRO_INCH(g_inch, speed=350, gain=0.5):
    degrees = int(DEGREE_INCH*g_inch)
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(distance_motor, 0)
    sleep_ms(50)
    while abs(motor.relative_position(distance_motor)) <= degrees:
        yaw = motion_sensor.tilt_angles()[0]
        correction = max(-100, min(100, int(yaw * gain)))
        motor_pair.move(drive_motors, correction, velocity=speed)
        sleep_ms(10)
    motor_pair.stop(drive_motors)

async def GYRO_INCH_BK(g_inch, speed=-400, gain=0.5):
    degrees = int(DEGREE_INCH*g_inch)
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(distance_motor, 0)
    sleep_ms(50)
    while abs(motor.relative_position(distance_motor)) <= degrees:
        yaw = motion_sensor.tilt_angles()[0]
        correction = -max(-100, min(100, int(yaw * gain)))
        motor_pair.move(drive_motors, correction, velocity=speed)
        sleep_ms(10)
    motor_pair.stop(drive_motors)

async def RIGHT_GYRO(rob_degree, how_fast):    # turn right, robot degrees, at speed
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    sleep_ms(50)
    while motion_sensor.tilt_angles()[0] >= -10*rob_degree :
        motor_pair.move(motor_pair.PAIR_1, 100, velocity=how_fast)
        sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)

async def LEFT_GYRO(rob_degree, how_fast):    # turn left, robot degrees, at speed
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    sleep_ms(50)
    while motion_sensor.tilt_angles()[0] <= 10*rob_degree :
        motor_pair.move(motor_pair.PAIR_1, -100, velocity=how_fast)
        sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)

async def ROBOGUARD():
    await light_matrix.write('#3')

    times_to_loop_around = 2
    number_of_rotations = 8
    radius_of_surveillance = 20
    step_size = 2 * pi * radius_of_surveillance / number_of_rotations
    turn_angle = 360 / number_of_rotations
    count = 1
    while count <= number_of_rotations * times_to_loop_around:
        if count == 1:
            await GYRO_INCH(step_size/2,400)
        else:
            await GYRO_INCH(step_size,400)
        await RIGHT_GYRO(turn_angle,300)
        count += 1

MISSION_MAP = {     # CHATGPT SUGGESTED
    0: ROBOGUARD,                       # MISSION_3 = MINECART 
}

async def DO_MAP_MISSION(mission_number):
    func = MISSION_MAP.get(mission_number)
    if func:
        await func()
    else:
        await light_matrix.write('NO MATCH')

async def wait_for_release(btn):    # CHATGPT SUGGESTED
    light.color(light.POWER, color.RED) # FEED BACK
    while button.pressed(btn):
        pass

# write your code here  MAIN
async def main():
    motion_sensor.reset_yaw(0)
    sleep_ms(50)
    await light_matrix.write("TIMUR")
    count = 0
    #loop until stopped
    while TRUE:
        await light_matrix.write(PR_LETTER[count])
        if button.pressed(button.LEFT):         # DO mission if LEFT button pressed
            await wait_for_release(button.LEFT)       # wait for release
            await DO_MAP_MISSION(count)
            count = count + 1
        if button.pressed(button.RIGHT):        # SKIP mission if RIGHT button pressed
            await wait_for_release(button.RIGHT)      # wait for release
            count += 1
        if count==COUNT_MAX:                    # WRAP END OF LIST
            count=0 
        time.sleep_ms(200)
        light.color(light.POWER, color.GREEN)
#   MAIN()  LOOP

runloop.run(main())