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
mrocket = 815              # mass of rocket

# *** Control panel (all quantities in metric units)
# *** To simplify the problem, set the z-component of 
# *** the initial positions and velocities below to zero

dt = 2 * 3600                          # time step
jupiterrocketdist = 500 * jupiterdiameter    # distance from jupiter considered a success
riearth = vector(1.447214054379151E+11, -4.423991320885015E+10, -1.062619063954428E+07)                   # initial position of jupiter
viearth = vector(8.148892366116470E+03, 2.840375889886787E+04, 1.639043726347822E+00)
rijupiter = vector(1.055355055205870E+11, 7.546173434489038E+11, -5.471696100017726E+09)                 # initial position of earth
vijupiter = vector(-1.309430711064983E+04, 2.413277002306963E+03, 2.833049104713701E+02)                     # initial velocity of earth
                    # initial velocity of jupiter
virocket =vector(1.621225177117242E+04, 4.048629375968122E+04, 8.055511810827731E+02)             #initial speed of rocket
rirocket =  vector(1.447289329190070E+11, -4.424029803569365E+10, -1.103055189367570E+07)          # launch angle of rocket (relative to +x axis)




# set up scene and objects


sun=sphere(pos=vector(0,0,0), radius=0.1*AU, color=color.yellow)

earth=sphere(pos=riearth, radius=0.05*AU, color=color.blue)
earthtrail=attach_trail(earth, radius=0.2*earth.radius, trail_type="points", interval=2, retain=1000)
earth.vel = viearth

jupiter=sphere(pos=rijupiter, radius=0.08*AU, color=color.red)
jupitertrail=attach_trail(jupiter, radius=0.2*jupiter.radius, trail_type="points", interval=2, retain=1000)
jupiter.vel = vijupiter

rocket=sphere(pos=rirocket, radius=0.05*AU, color=color.orange)
rockettrail=attach_trail(rocket, radius=0.2*rocket.radius, trail_type="points", interval=2, retain=1000)
rocket.vel = virocket
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

    # Rocket's motion
    f_rocket_sun = gravitational_force(mrocket, msun, rocket.pos, sun.pos)
    f_rocket_earth = gravitational_force(mrocket, mearth, rocket.pos, earth.pos)
    f_rocket_jupiter = gravitational_force(mrocket, mjupiter, rocket.pos, jupiter.pos)
    total_force = f_rocket_sun + f_rocket_earth + f_rocket_jupiter
    rocket.vel += total_force / mrocket * dt
    rocket.pos += rocket.vel * dt

    # Update time and label
    t += dt
    tstr = "Time: {:.0f} days".format(t / (24 * 3600))
    tlabel.text = tstr
    print(mag(rocket.pos-jupiter.pos))
