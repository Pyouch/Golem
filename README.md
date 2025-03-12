## Project idea

The main idea is to make a game where we must code our spells.

You must write your spells in .mg files, in the "spells" directory. Then the game will see and compile 
all the spells into game's spells. 

By passing obstacles, you will find new primitive spells, used for coding your spells.


### The mg language

Not created yet 😅


### Overview of the code


The project is entirely made in python, with th library pygame for the graphics.


#### 3D engine

The 3D engine is made by orthogonal projection.

The engine has a buffer. You can add 3D primitives in the engine's buffer 
(`engine.add_buffer(Primitive(args))`).
When you want to draw, you run `engine.finalize()`. The engine will project the points, then compute the lights for the 
face, then transform it in a 2D primitive. Finally, he draws it (He has the graphic pipeline).

##### Lights

The lighting use the Phong model. 

There are 3 different types of lights:
- ambient (I call it radiance)
- diffuse (I call it lights)
- specular (I call it shine)

The radiance is a minimal quantity of light who everybody has.

The diffuse is the light coming directly from objects making light.

The Shine is the reflection on shiny surfaces.


## TODOs

### To implement


#### For the 3D engine

- Transform in 4D vectors
- Move the camera
- Make gradients (is it possible to do it easily with pygame ?)
- Shine from Phong model (for the lights)

#### For the game

- A compiler (or interpreter ?)
- Characters who can move
- A lot of other things, but I have not thought enough about the game himself 😂

### To optimize


#### The 10 functions more time-consuming (by cProfile):

- View.py:49(finalize)                             
- ViewEngine.py:136(finalize)          
- ViewEngine.py:130(draw_buffer)   
- ViewEngine.py:21(to_2d)
- ViewEngine.py:97(to_screen)       
- ViewEngine.py:105(color)   
- ViewEngine.py:108(_intensity)      
- Matrix.py:33(__mul__) 
- View.py:33(draw_terrain)         
- ViewEngine.py:118(_lights)

We have to optimize in priority the functions for vectors, used in all of this functions

#### Ideas to optimize:

- Make an implementation of vectors and matrices with numpy arrays.
- Filter the 3D primitives to remove the useless ones (not in the player's field of view)
- ? Add The 3D primitives in a heap instead of a list ?
