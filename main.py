import force_sensor
import motor
from hub import port

while True:
   # Store the force of the Force Sensor in a variable.
   force = force_sensor.force(port.F)

   # Print the variable to the Console.
   print(force)

   # Run the motor and use the variable to set the velocity.
   motor.run(port.A, force)