from vpython import *
#GlowScript 2.7 VPython

# SETUP

#scene.bind('keydown', keydown_fun)       # Function for key presses
#scene.bind('keyup', keyup_fun)           # Function for key un-presses
scene.background = vec(0.57, 0.72, 1)     # Light blue
scene.ambient= color.gray(0.4)
scene.width = 1000                        # Make the 3D canvas larger
scene.height = 550



"""Using van der Waals radii from
   https://www.reed.edu/chemistry/ROCO/Geometry/vdw_radius.html
   and colors from https://en.wikipedia.org/wiki/CPK_coloring
"""
ELEMENTS = {'H': [1.2,  vec(0.8, 0.8, 0.8)],  # near-white
            'C': [1.7,  vec(0.1, 0.1, 0.1)],  # near-black
            'N': [1.5,  vec(0, 0, 1)],        # blue
            'O': [1.4,  vec(1, 0, 0)],        # red
            'F': [1.35, vec(0, 1, 0.3)],      # bright green        
            'P': [1.9,  vec(1, 0.65, 0)],     # orange
            'S': [1.85, vec(1, 1, 0)],        # yellow
            'Cl':[1.8,  vec(0, 0.8, 0)]       # dark green
            }

vscale = 4
v = {0: vec(0, 0, 0),
     1: vec(1,  0, -1/sqrt(2)) * vscale,
     2: vec(-1, 0, -1/sqrt(2)) * vscale,
     3: vec(0,  1,  1/sqrt(2)) * vscale,
     4: vec(0, -1,  1/sqrt(2)) * vscale
    }
# Magnitude = 2 * sqrt(3./8) * vscale


# MOLECULE DEFINITIONS
"""
Every atom is defined in relation to an existing atom to which it bonds.
The first atom is the "root" and so only requires a type; each proceeding
atom takes 3 arguments: type,  the parent/reference atom's index, and the
vector specifying its relative location (and optional bond type integer).
You can also add additional bonds (eg to close loops) with three arguments:
the integer bond type and the indices of the two bonded atoms.
"""

butane = ['C',              # 0
         ['C', 0, v[1]],    # 1
         ['C', 1, -v[2]],   # 2
         ['C', 2, v[1]],    # 3
         ['H', 0, v[2]*.7], # Hydrogenating... Should I automate this?
         ['H', 0, v[3]*.7],
         ['H', 0, v[4]*.7],
         ['H', 1, -v[3]*.7],
         ['H', 1, -v[4]*.7],
         ['H', 2, v[3]*.7],
         ['H', 2, v[4]*.7],
         ['H', 3, -v[2]*.7],
         ['H', 3, -v[3]*.7],
         ['H', 3, -v[4]*.7],
         ]
         
cyclo6 = ['C',
         ['C', 0, v[3]],
         ['C', 1, -v[1]],
         ['C', 2, v[4]],
         ['C', 3, -v[3]],
         ['C', 4, v[1]],
         [1, 0, 5]
         ]



# OBJECT CREATION

def make_molecule(start, molecule):
    """
    Creates compound object from molecule definition
    """
    
    atomobjs = [ make_atom(center = start, type = molecule[0]) ]
    atompos =  [ start ]
    bondobjs = [ ]
    
    for atom in molecule[1:]:
        
        if atom[0] in ELEMENTS:
            
            oldpos = atompos[ atom[1] ]
            newpos = oldpos + atom[2]
            
            atompos.append( newpos )
            atomobjs.append( make_atom( center = newpos, type = atom[0] ) )
        
            bondtype = 1
            if len(atom) > 3: bondtype = atom[3]
                
            bondobjs.append( make_bond( start = oldpos, end = newpos, type = bondtype ))
        
        else:
            bondobjs.append( make_bond( start = atompos[atom[1]], end = atompos[atom[2]], type = atom[0] ))
    
    molecule = compound(bondobjs + atomobjs, pos = start)
    return molecule
    
    
    
def make_atom(center, type):
    """
    Creates atom with vector center and string type
    of atomic symbol referencing the elements dict 
    """
    return sphere(pos = center, radius = ELEMENTS[type][0], color = ELEMENTS[type][1])


    
def make_bond(start, end, type=1):
    """
    Creates bond from vector position start to end
    Type is int 1 or 2 inidicating single/double bond
    """
    along = vector( end.x-start.x, end.y-start.y, end.z-start.z )
    
    if type == 1:
        bond = cylinder(pos = start, axis = along, color = color.white, radius = 0.6, opacity = 0.6)
        
    elif type == 2:
        offset = cross(along, vec(along.x, along.y, along.z+1)).hat*0.5
          # Offset is perpendicular to along, used to space out double bond
          # .hat normalizes to length 1, then scale to get desired gap
        bond1 = cylinder(pos = start+offset, axis = along, color = color.white, radius = 0.4, opacity = 0.6)
        bond2 = cylinder(pos = start-offset, axis = along, color = color.white, radius = 0.4, opacity = 0.6)
        bond = compound([bond1, bond2])
    
    return bond
    





ground = box(pos = vec(0, -20, 0), size = vec(40, 0.2, 40), opacity = 0.3)

moleculeA = make_molecule( start = vec(-6,0,0), molecule = cyclo6 )


frame = 0
RATE = 100                      # The number of times the while loop runs each second
dt = 1.0/(1.0*RATE)             # The time step each time through the while loop
scene.autoscale = False         # Avoids changing the view automatically
scene.forward = vec(0, -3, -2)  # Ask for a bird's-eye view of the scene...


while True:

    rate(RATE)   # maximum number of times per second the while loop runs
    frame += 1

    moleculeA.rotate( angle = 0.01, axis = vec(1, 0, 1) )
