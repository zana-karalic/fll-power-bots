# pyright: reportMissingImports=false

# FULL MASTER1022 updatesMERGE EAST & WEST
import runloop, motor_pair, motor , color, time
from hub import motion_sensor, light_matrix, light, port, button
import math
from math import *
from time import sleep, sleep_ms

# PORT DEFINITIONS
forward_motor= port.A
distance_motor = port.B
motor_pair.pair(motor_pair.PAIR_1, forward_motor, distance_motor)
drive_motors= motor_pair.PAIR_1

EYE_LEFT= port.C
EYE_RIGHT = port.D

ARM_RIGHT = port.E#right arm
ARM_LEFT= port.F#left arm

motion_sensor.set_yaw_face(motion_sensor.FRONT)

# INITIALIZE
COUNT_MAX= 11    # NUMBER OF MISSIONS
DEGREE_INCH = 51.4    # COACH 51.4,TWIN 33

TRUE = 1
FALSE = 0
PR_LETTER=['A','B','C','D','E','F','G','H','I','J','K']

# FUNCTIONS
async def WALL_SQUARE_TS():    # square by backing against the wall
    #await motor_pair.move_for_time(motor_pair.PAIR_1, 500, 0, velocity=-400)
    motor.run_for_time(forward_motor,500, 400)
    await motor.run_for_time(distance_motor,500, -400)
    #500 milliseconds, straight,at -400 ~40% backup
    sleep_ms(150)
    motion_sensor.reset_yaw(0)
    sleep_ms(100)    # CHAT WAIT MORE ?

async def WALL_SQUARE():    # square by backing against the wall
    await motor_pair.move_for_time(motor_pair.PAIR_1, 500, 0, velocity=-400)
    #500 milliseconds, straight,at -400 ~40% backup
    sleep_ms(100)
    motion_sensor.reset_yaw(0)
    sleep_ms(50)

async def MOV_INCHES(inc_dist,fast_slo):        # move inches at speed
    deg_inch = int(DEGREE_INCH * inc_dist )
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, deg_inch , 0, velocity=fast_slo)#52*inc_dist

async def ARMFRONT(degrees, power):
    await motor.run_for_degrees(ARM_RIGHT,-degrees, power) #'-' is downPORT, DEGREES, POWER

async def ARMFRONT1(degrees, power):
    await motor.run_for_degrees(ARM_LEFT, -degrees,power)

async def ARM_MOTOR( arm_port, degrees, power):    # SHARE ARM FUNCTION?
    await motor.run_for_degrees(arm_port,degrees,power)

async def GYRO_INCH(g_inch, speed=400, gain=0.5):
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



async def MISSION_3():
    #await light_matrix.write('#3')
    # awaitARMFRONT(88,700)
    await GYRO_INCH(27,400)
    await RIGHT_GYRO(88,150)
    await GYRO_INCH(14,300)
    await LEFT_GYRO(88,100)
    await ARMFRONT(222,-150)
    sleep(0.5)
    await GYRO_INCH_BK(1,-100)
    await RIGHT_GYRO(120,200)
    await GYRO_INCH_BK(4.7,-100)
    await ARMFRONT(220,200)
    sleep(0.5)
    await GYRO_INCH(4.5,100)
    await ARMFRONT(100,-150)
    await LEFT_GYRO(25,100)
    await RIGHT_GYRO(25,100)
    await GYRO_INCH_BK(6.2,-100)
    await RIGHT_GYRO(75,400)
    await GYRO_INCH(30,400)


async def ARM():
    await ARMFRONT(90,200)

async def MISSION_12_SALVAGESHIP():
    await GYRO_INCH(24, 190)
    await ARMFRONT(100,100)
    await GYRO_INCH_BK(3, -300)
    await ARMFRONT(180,-100)
    await GYRO_INCH( 7, 300)
    await GYRO_INCH_BK(25, -300)


async def GREEN_THING():
    await WALL_SQUARE()
    await ARMFRONT(180,-400)
    await GYRO_INCH(27,390)
    await LEFT_GYRO(33,200)
    await GYRO_INCH_BK(2,-400)
#If going up too much make it more, and if it is going down too much make it less - Neil
#If turning too much make it more, and if turning to much make it less
    await ARMFRONT(180,400)
    await GYRO_INCH(6.5,200)
    sleep_ms(200)
    await ARMFRONT(220,-400)
    sleep_ms(200)
    await RIGHT_GYRO(10,200)
    await GYRO_INCH_BK(6.5,-200)
    await RIGHT_GYRO(45,200)
    await GYRO_INCH_BK(28,-300)
    await ARMFRONT(180,400)




async def ROW():
    await WALL_SQUARE()
    await GYRO_INCH(28.5,375)
    await LEFT_GYRO(20,300)
    await GYRO_INCH(1,300)
    await LEFT_GYRO(20,300)
    # await GYRO_INCH(0.5,200)
    # await MOV_INCHES(0.5,-200)
    await RIGHT_GYRO(25,300)
    await MOV_INCHES(3.5,-300)
    await RIGHT_GYRO(50,200)
    await MOV_INCHES(.5,-300)
    await ARMFRONT(160,300)
    await GYRO_INCH(1.5,200)
    await ARMFRONT(180,-300)
    await MOV_INCHES(4.41,-300)
    await LEFT_GYRO(40,200)
    await MOV_INCHES(30,-450)




async def TEST():
    await WALL_SQUARE()
    await ARMFRONT(-20,400)
    await ARMFRONT1(150,250)
    await GYRO_INCH(25.5,450)
    await RIGHT_GYRO(15,300)
    await LEFT_GYRO(2,200)
    await GYRO_INCH(2.5,200)
    await ARMFRONT1(-105,200)
    await ARMFRONT(-105,200)
    await LEFT_GYRO(35,200)
    await RIGHT_GYRO(45,200)
    await ARMFRONT1(100,300)
    await GYRO_INCH(-1,200)
    await RIGHT_GYRO(25,200)
    await GYRO_INCH(2,500)
    await ARMFRONT(-110,200)
    await GYRO_INCH(2,500)
    await ARMFRONT(100,200)
    await GYRO_INCH_BK(2,200)
    await LEFT_GYRO(40,200)
    await GYRO_INCH_BK(25,200)






async def SILO_old():
    await WALL_SQUARE()
    await GYRO_INCH(13.16,300)
    await ARMFRONT(300,-1100)
    await ARMFRONT(300,200)
    await ARMFRONT(300,-1100)
    await ARMFRONT(300,200)
    await ARMFRONT(300,-1100)
    await ARMFRONT(300,500)
    await ARMFRONT(300,-1100)
    await ARMFRONT(300,500)
    await MOV_INCHES(5,-500)
    await LEFT_GYRO(20,200)
    await GYRO_INCH(26,300)
    await LEFT_GYRO(95,200)
    await GYRO_INCH(1.9,100)
    await ARMFRONT(-300,200)
    sleep(0.25)
    await MOV_INCHES(2,-400)
    await RIGHT_GYRO(35,200)
    await GYRO_INCH(12,200)
    await RIGHT_GYRO(145,200)
    await ARMFRONT(8,125)
    await GYRO_INCH(5,100)

async def SILO():
    await WALL_SQUARE()
    await ARMFRONT(300,400)
    await GYRO_INCH(12.9,300)
    await ARMFRONT(300,-1500)
    await ARMFRONT(300,200)
    await ARMFRONT(300,-1500)
    await ARMFRONT(300,200)
    await ARMFRONT(300,-1500)
    await ARMFRONT(300,500)
    await ARMFRONT(300,-1500)
    await ARMFRONT(200,500)
    await MOV_INCHES(5,-500)
    await LEFT_GYRO(22,200)
    await GYRO_INCH(25.5,300)
    await LEFT_GYRO(35,200)
    await GYRO_INCH(2,200)
    await LEFT_GYRO(50,200)
    await GYRO_INCH(1.5,275)
    await ARMFRONT(100,-300) # changed from 120 to 100
    await RIGHT_GYRO(10,200)
    await RIGHT_GYRO(30,200)
    await GYRO_INCH(8,250)
    await ARMFRONT(100,200)
    await LEFT_GYRO(54,200)
    await GYRO_INCH(25,350)
    await RIGHT_GYRO(50,200)
    await GYRO_INCH(33,400)



async def SCALE_E():
    await WALL_SQUARE()
    await GYRO_INCH(22,400)
    await LEFT_GYRO(85,250)
    await GYRO_INCH(3,400)
    await ARMFRONT(120,-400)
    sleep(0.25)
    await RIGHT_GYRO(10,100)
    await LEFT_GYRO(5,500)
    await MOV_INCHES(3,-400)
    await ARMFRONT(17,-400)
    await ARMFRONT(15,100)
    await LEFT_GYRO(5,200)
    await ARMFRONT(15,100)
    await LEFT_GYRO(5,200)
    await ARMFRONT(15,100)
    await LEFT_GYRO(5,200)
    await ARMFRONT(15,100)


async def ARM_UP():
    await ARMFRONT(100,300)

async def ARM_DOWN():
    await ARMFRONT(-75,100)


async def ARM_ABS_PO( arm_port, power):    # MOTOR TO ABSOLUTE POSITION
    await motor.run_to_absolute_position(arm_port,0,power,direction=motor.SHORTEST_PATH,stop=motor.HOLD)

async def PREPARE():
    await ARM_ABS_PO(ARM_RIGHT, 150)




async def ARMMOVEGREENTHING():
    await ARMFRONT(200,-400)


async def NOGOODNAME():
    await WALL_SQUARE()

    await ARM_MOTOR(ARM_LEFT,-200,400)
    await ARM_MOTOR(ARM_RIGHT,200,400)

    await GYRO_INCH_BK(10,-200)

    await MOV_INCHES(4, 300)
    await MOV_INCHES(4,-300)

    await GYRO_INCH(5,200)

    await GYRO_INCH(5,200)

    await RIGHT_GYRO(45,100)

    await LEFT_GYRO(45,100)

MISSION_MAP = {    # CHATGPT SUGGESTED
    0: TEST,            # A FORGE &
    1: SILO,            # B SILO & SCALE
    2: GREEN_THING,    # C MAP REVEAL
    3: MISSION_12_SALVAGESHIP, # D SALVAGE
    4: MISSION_3,    # E MINE & STATUE
    5: PREPARE,        # F ABSOLUTE POSITION
    6: ARMMOVEGREENTHING,# G
    7: ARM_UP,        # H
    8: ARM_DOWN,        # I
    9: NOGOODNAME,    # J
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

async def main():
    motion_sensor.reset_yaw(0)
    sleep_ms(50)
    await light_matrix.write("TIMUR")
    count = 0
    #loop until stopped
    while TRUE:
        await light_matrix.write(PR_LETTER[count])
        if button.pressed(button.LEFT):        # DO mission if LEFT button pressed
            await wait_for_release(button.LEFT)    # wait for release
            await DO_MAP_MISSION(count)
            count = count + 0
        if button.pressed(button.RIGHT):        # SKIP mission if RIGHT button pressed
            await wait_for_release(button.RIGHT)    # wait for release
            count += 1
        if count==COUNT_MAX:                    # WRAP END OF LIST
            count=0
        time.sleep_ms(200)
        light.color(light.POWER, color.GREEN)

runloop.run(main())