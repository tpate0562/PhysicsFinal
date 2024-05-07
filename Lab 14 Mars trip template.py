from vpython import sphere, vector, color, rate, scene, attach_trail, arrow, label, cos, sin, pi, mag, norm, hat

scene.width = 630
scene.height = 600
scene.userspin = False
scene.userzoom = True


# To use this file, (1) fill in the control panel with appropriate values, 
# then find and complete all 5 lines with a triple asterisk comment (***)
#
# Note that exponents are indicated by a double asterisk (**). Using a caret 
# symbol (^) will cause the program to behave unpredictably.
#
# Some VPython functions that might be helpful are:
# "norm(a)" or "hat(a)"  is a unit vector with the same direction as the vector "a"
# "mag(a)"   is a scalar that is the magnitude of the vector "a"

# Constants in metric units
jupiterdiameter = 6.78e6      # jupiter diameter
G = 6.67384e-11              # universal gravitational constant
AU = 1.496e11                # Astronomical unit (avg. dist from Sun to Earth--for length scale purposes)
msun = 1.989e30              # mass of Sol (sun)
mearth = 5.97219e24              # mass of Earth
mjupiter = 1.898e27           # mass of jupiter
mrocket = 815    
msaturn = 5.683e26          # mass of rocket

# *** Control panel (all quantities in metric units)
# *** To simplify the problem, set the z-component of 
# *** the initial positions and velocities below to zero

dt = 2 * 3600                          # time step
jupiterrocketdist = 500 * jupiterdiameter    # distance from jupiter considered a success
riearth = vector( 4.449401091798647E+10, 1.403470707888662E+08, -1.769063940881193E+04)                   # initial position of jupiter
viearth = vector(-2.893748681913718E+04, 8.702013674306697E+03,7.726695004177664E-01)
rijupiter = vector(-3.952668829569589E+11, 6.792547950520715E+11, 6.054681409011871E+09)                 # initial position of earth
vijupiter = vector(-1.144241460230606E+04, -5.972055209548326E+03, 2.807644771036928E+02)                     # initial velocity of earth
                    # initial velocity of jupiter
rirocket =vector(-3.804368981984373E+11, 5.917727238669536E+11, 8.206215977999300E+09)             #initial speed of rocket
virocket =  vector(-1.325519458837047E+04, 4.932879806883460E+03, 1.178862520211088E+01)          # launch angle of rocket (relative to +x axis)
risaturn = vector(-1.287092434829489E+12, 5.253855136589826E+11, 4.195904660432076E+10)
visaturn = vector(-4.172246290764435E+03, -8.964810326105848E+03, 3.222895141594253E+02)


# set up scene and objects


sun=sphere(pos=vector(0,0,0), radius=0.1*AU, color=color.yellow)

earth=sphere(pos=riearth, radius=0.01*AU, color=color.blue)
earthtrail=attach_trail(earth, radius=0.2*earth.radius, trail_type="points", interval=2, retain=1000)
earth.vel = viearth

jupiter=sphere(pos=rijupiter, radius=0.01*AU, color=color.red)
jupitertrail=attach_trail(jupiter, radius=0.2*jupiter.radius, trail_type="points", interval=2, retain=1000)
jupiter.vel = vijupiter

rocket=sphere(pos=rirocket, radius=0.05*AU, color=color.orange)
rockettrail=attach_trail(rocket, radius=0.2*rocket.radius, trail_type="points", interval=2, retain=1000)
rocket.vel = virocket

saturn=sphere(pos=risaturn, radius=0.03*AU, color=color.blue)
saturntrail=attach_trail(saturn, radius=0.2*rocket.radius, trail_type="points", interval=2, retain=1000)
saturn.vel = visaturn
scene.camera.follow(rocket)

# draw an arrow to show direction of initial velocity of rocket
rocketarrow1 = arrow(pos=earth.pos, axis=(sun.radius*2)*norm(virocket), color=color.white)


#set the scene
scene.range=1.3*mag(jupiter.pos)

#create display for timing information
tstr="Time: {:.0f} days".format(0)
tlabel=label(pos=vector(0,1.2*mag(jupiter.pos),0), text=tstr)

launchstr="Starting Date: 07302020."             # *** replace XXXXXXXX with your launch date

launchlabel=label(pos=vector(0,-1.2*mag(jupiter.pos),0), text=launchstr)


t=0

# *** add a comparison to the while statement below (inside the parentheses)
# *** so that the program will run until the rocket is within "jupiterrocketdist" of jupiter
while 1:
    rate(200)  # Controls the speed of the simulation

    # Gravitational force calculation
    def gravitational_force(m1, m2, r1, r2):
        # Vector from object 1 to object 2
        r = r2 - r1
        # Magnitude of the gravitational force
        f_mag = G * m1 * m2 / mag(r)**2
        # Direction of the force
        f_dir = norm(r)
        return f_mag * f_dir

    # Earth's motion
    f_earth_sun = gravitational_force(mearth, msun, earth.pos, sun.pos)
    earth.vel += f_earth_sun / mearth * dt
    earth.pos += earth.vel * dt

    # jupiter's motion
    f_jupiter_sun = gravitational_force(mjupiter, msun, jupiter.pos, sun.pos)
    jupiter.vel += f_jupiter_sun / mjupiter * dt
    jupiter.pos += jupiter.vel * dt
    f_saturn_sun = gravitational_force(msaturn, msun, saturn.pos, sun.pos)
    saturn.vel += f_saturn_sun / msaturn * dt
    saturn.pos += saturn.vel * dt

    # Rocket's motion
    f_rocket_sun = gravitational_force(mrocket, msun, rocket.pos, sun.pos)
    f_rocket_earth = gravitational_force(mrocket, mearth, rocket.pos, earth.pos)
    f_rocket_jupiter = gravitational_force(mrocket, mjupiter, rocket.pos, jupiter.pos)
    f_rocket_saturn = gravitational_force(mrocket, msaturn, rocket.pos, saturn.pos)
    total_force = f_rocket_sun + f_rocket_earth + f_rocket_jupiter + f_rocket_saturn
    rocket.vel += total_force / mrocket * dt
    rocket.pos += rocket.vel * dt
    print(mag(jupiter.pos) - mag(rocket.pos))

    # Update time and label
    t += dt
    tstr = "Time: {:.0f} days".format(t / (24 * 3600))
    tlabel.text = tstr

