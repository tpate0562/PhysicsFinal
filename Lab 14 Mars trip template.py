from vpython import sphere, vector, color, rate, scene, attach_trail, arrow, label, cos, sin, pi, mag, norm

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
marsdiameter = 6.78e6      # mars diameter
G = 6.67384e-11              # universal gravitational constant
AU = 1.496e11                # Astronomical unit (avg. dist from Sun to Earth--for length scale purposes)
msun = 1.989e30              # mass of Sol (sun)
mearth = 5.97219e24              # mass of Earth
mmars = 6.4185e23              # mass of Mars
mrocket = 1e4              # mass of rocket

# *** Control panel (all quantities in metric units)
# *** To simplify the problem, set the z-component of 
# *** the initial positions and velocities below to zero

dt = 2 * 3600                          # time step
marsrocketdist = 500 * marsdiameter    # distance from mars considered a success
riearth = vector(9.062260787481210e10, -1.202386386794547e11 ,0)                   # initial position of mars
viearth = vector(2.327335600544946e4, 1.782202031258401e4,0)
rimars = vector(1.837669141112841e11, -9.170458197260064e10,0)                 # initial position of earth
vimars = vector(1.178684789960390e4, 2.371545627374556e4,0)                     # initial velocity of earth
                    # initial velocity of mars
speedirocket = 5e3                         #initial speed of rocket
angleirocket =    6.881                        # launch angle of rocket (relative to +x axis)

virocket = speedirocket*vector(cos(angleirocket*pi/180),sin(angleirocket*pi/180),0)


# set up scene and objects


sun=sphere(pos=vector(0,0,0), radius=0.1*AU, color=color.yellow)

earth=sphere(pos=riearth, radius=0.05*AU, color=color.blue)
earthtrail=attach_trail(earth, radius=0.2*earth.radius, trail_type="points", interval=2, retain=1000)
earth.vel = viearth

mars=sphere(pos=rimars, radius=0.0001*AU, color=color.red)
marstrail=attach_trail(mars, radius=0.2*mars.radius, trail_type="points", interval=2, retain=1000)
mars.vel = vimars

rocket=sphere(pos=earth.pos, radius=0.0001*AU, color=color.orange)
rockettrail=attach_trail(rocket, radius=0.2*rocket.radius, trail_type="points", interval=2, retain=1000)
rocket.vel = earth.vel + virocket
scene.camera.follow(rocket)

# draw an arrow to show direction of initial velocity of rocket
rocketarrow1 = arrow(pos=earth.pos, axis=(sun.radius*2)*norm(virocket), color=color.white)


#set the scene
scene.range=1.3*mag(mars.pos)

#create display for timing information
tstr="Time: {:.0f} days".format(0)
tlabel=label(pos=vector(0,1.2*mag(mars.pos),0), text=tstr)

launchstr="Starting Date: 07302020."             # *** replace XXXXXXXX with your launch date

launchlabel=label(pos=vector(0,-1.2*mag(mars.pos),0), text=launchstr)


t=0

# *** add a comparison to the while statement below (inside the parentheses)
# *** so that the program will run until the rocket is within "marsrocketdist" of Mars
while mag(mars.pos - rocket.pos) > marsrocketdist*0.0005:
    rate(30)  # Controls the speed of the simulation

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

    # Mars's motion
    f_mars_sun = gravitational_force(mmars, msun, mars.pos, sun.pos)
    mars.vel += f_mars_sun / mmars * dt
    mars.pos += mars.vel * dt

    # Rocket's motion
    f_rocket_sun = gravitational_force(mrocket, msun, rocket.pos, sun.pos)
    f_rocket_earth = gravitational_force(mrocket, mearth, rocket.pos, earth.pos)
    f_rocket_mars = gravitational_force(mrocket, mmars, rocket.pos, mars.pos)
    total_force = f_rocket_sun + f_rocket_earth + f_rocket_mars
    rocket.vel += total_force / mrocket * dt
    rocket.pos += rocket.vel * dt

    # Update time and label
    t += dt
    tstr = "Time: {:.0f} days".format(t / (24 * 3600))
    tlabel.text = tstr
