prompt_tabletop_ui = '''
# Rules:
# 1. You MUST reply with executable code only. Every natural language comment will make the code invalid.
# 2. The code you write SHOULD NOT be contained in a code block. Write raw code.
# The following is a collection of examples.

# Python 2D robot control script
import numpy as np
from env_utils import put_first_on_second, get_obj_pos, get_obj_names, say, get_corner_name, get_side_name, is_obj_visible, stack_objects_in_order
from plan_utils import parse_obj_name, parse_position, parse_question, transform_shape_pts

objects = ['yellow_cube', 'green_cube', 'orange_cube', 'blue_cube']
# put the four cubes in a straight line
say('Ok - putting the cubes in a straight line')
red_cube_pos = get_obj_pos('red_cube')
blue_cube_target = get_pt_to_the_right(red_cube_pos)
move_obj_to_pos('blue_cube', blue_cube_target)
green_cube_target = get_pt_to_the_right(blue_cube_target)
move_obj_to_pos('green_cube', green_cube_target)
orange_cube_target = get_pt_to_the_right(green_cube_target)
move_obj_to_pos('orange_cube', orange_cube_target)
objects = ['yellow_cube', 'green_cube', 'orange_cube', 'blue_cube']

# put the four cubes in a vertical straight line
say('Ok - putting the cubes in a vertical straight line, asusming the red cube is at the bottom')
red_cube_pos = get_obj_pos('red_cube')
blue_cube_target = get_pt_in_front(red_cube_pos)
move_obj_to_pos('blue_cube', blue_cube_target)
green_cube_target = get_pt_in_front(blue_cube_target)
move_obj_to_pos('green_cube', green_cube_target)
orange_cube_target = get_pt_in_front(green_cube_target)
move_obj_to_pos('orange_cube', orange_cube_target)
objects = ['yellow_cube', 'green_cube', 'orange_cube', 'blue_cube']

# put the yellow cube on top of the green cube
say('Ok - putting the yellow cube on top of the green cube')
put_first_on_second('yellow_cube', 'green_cube')
objects = ['yellow_cube', 'green_cube', 'orange_cube', 'blue_cube']

# stack the blue cube on top of the orange cube
say('Ok - stacking the blue cube on top of the orange cube')
put_first_on_second('blue_cube', 'orange_cube')
objects = ['yellow_cube', 'green_cube', 'orange_cube', 'blue_cube']

# put the yellow cube next to the green cube
say('Ok - putting the yellow cube next to the green cube')
yellow_cube_target = get_pt_to_the_right(get_obj_pos('green_cube'))
move_obj_to_pos('yellow_cube', yellow_cube_target)
'''.strip()

prompt_parse_obj_name = '''
import numpy as np
from env_utils import get_obj_pos, parse_position
from utils import get_obj_positions_np

objects = ['blue block', 'cyan block', 'purple bowl', 'gray bowl', 'brown bowl', 'pink block', 'purple block']
# the block closest to the purple bowl.
block_names = ['blue block', 'cyan block', 'purple block']
block_positions = get_obj_positions_np(block_names)
closest_block_idx = get_closest_idx(points=block_positions, point=get_obj_pos('purple bowl'))
closest_block_name = block_names[closest_block_idx]
ret_val = closest_block_name
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# the blocks.
ret_val = ['brown block', 'blue block']
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# the brown objects.
ret_val = ['brown bowl', 'brown block']
objects = ['brown bowl', 'banana', 'brown block', 'apple', 'blue bowl', 'blue block']
# a fruit that's not the apple
fruit_names = ['banana', 'apple']
for fruit_name in fruit_names:
    if fruit_name != 'apple':
        ret_val = fruit_name
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# blocks above the brown bowl.
block_names = ['blue block', 'cyan block', 'purple block']
brown_bowl_pos = get_obj_pos('brown bowl')
use_block_names = []
for block_name in block_names:
    if get_obj_pos(block_name)[1] > brown_bowl_pos[1]:
        use_block_names.append(block_name)
ret_val = use_block_names
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# the blue block.
ret_val = 'blue block'
objects = ['blue block', 'cyan block', 'purple bowl', 'brown bowl', 'purple block']
# the block closest to the bottom right corner.
corner_pos = parse_position('bottom right corner')
block_names = ['blue block', 'cyan block', 'purple block']
block_positions = get_obj_positions_np(block_names)
closest_block_idx = get_closest_idx(points=block_positions, point=corner_pos)
closest_block_name = block_names[closest_block_idx]
ret_val = closest_block_name
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# the left most block.
block_names = ['green block', 'brown block', 'blue block']
block_positions = get_obj_positions_np(block_names)
left_block_idx = np.argsort(block_positions[:, 0])[0]
left_block_name = block_names[left_block_idx]
ret_val = left_block_name
objects = ['brown bowl', 'green block', 'brown block', 'green bowl', 'blue bowl', 'blue block']
# the bowl on near the top.
bowl_names = ['brown bowl', 'green bowl', 'blue bowl']
bowl_positions = get_obj_positions_np(bowl_names)
top_bowl_idx = np.argsort(block_positions[:, 1])[-1]
top_bowl_name = bowl_names[top_bowl_idx]
ret_val = top_bowl_name
objects = ['yellow bowl', 'purple block', 'yellow block', 'purple bowl', 'pink bowl', 'pink block']
# the third bowl from the right.
bowl_names = ['yellow bowl', 'purple bowl', 'pink bowl']
bowl_positions = get_obj_positions_np(bowl_names)
bowl_idx = np.argsort(block_positions[:, 0])[-3]
bowl_name = bowl_names[bowl_idx]
ret_val = bowl_name
'''.strip()

prompt_parse_position = '''
import numpy as np
from shapely.geometry import *
from shapely.affinity import *
from env_utils import denormalize_xy, parse_obj_name, get_obj_names, get_obj_pos

# a 30cm horizontal line in the middle with 3 points.
middle_pos = denormalize_xy([0.5, 0.5]) 
start_pos = middle_pos + [-0.3/2, 0]
end_pos = middle_pos + [0.3/2, 0]
line = make_line(start=start_pos, end=end_pos)
points = interpolate_pts_on_line(line=line, n=3)
ret_val = points
# a 20cm vertical line near the right with 4 points.
middle_pos = denormalize_xy([1, 0.5]) 
start_pos = middle_pos + [0, -0.2/2]
end_pos = middle_pos + [0, 0.2/2]
line = make_line(start=start_pos, end=end_pos)
points = interpolate_pts_on_line(line=line, n=4)
ret_val = points
# a diagonal line from the top left to the bottom right corner with 5 points.
top_left_corner = denormalize_xy([0, 1])
bottom_right_corner = denormalize_xy([1, 0])
line = make_line(start=top_left_corner, end=bottom_right_corner)
points = interpolate_pts_on_line(line=line, n=5)
ret_val = points
# a triangle with size 10cm with 3 points.
polygon = make_triangle(size=0.1, center=denormalize_xy([0.5, 0.5]))
points = get_points_from_polygon(polygon)
ret_val = points
# the corner closest to the sun colored block.
block_name = parse_obj_name('the sun colored block', f'objects = {get_obj_names()}')
corner_positions = np.array([denormalize_xy(pos) for pos in [[0, 0], [0, 1], [1, 1], [1, 0]]])
closest_corner_pos = get_closest_point(points=corner_positions, point=get_obj_pos(block_name))
ret_val = closest_corner_pos
# the side farthest from the right most bowl.
bowl_name = parse_obj_name('the right most bowl', f'objects = {get_obj_names()}')
side_positions = np.array([denormalize_xy(pos) for pos in [[0.5, 0], [0.5, 1], [1, 0.5], [0, 0.5]]])
farthest_side_pos = get_farthest_point(points=side_positions, point=get_obj_pos(bowl_name))
ret_val = farthest_side_pos
# a point above the third block from the bottom.
block_name = parse_obj_name('the third block from the bottom', f'objects = {get_obj_names()}')
ret_val = get_obj_pos(block_name) + [0.1, 0]
# a point 10cm left of the bowls.
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
bowl_positions = get_all_object_positions_np(obj_names=bowl_names)
left_obj_pos = bowl_positions[np.argmin(bowl_positions[:, 0])] + [-0.1, 0]
ret_val = left_obj_pos
# the bottom side.
bottom_pos = denormalize_xy([0.5, 0])
ret_val = bottom_pos
# the top corners.
top_left_pos = denormalize_xy([0, 1])
top_right_pos = denormalize_xy([1, 1])
ret_val = [top_left_pos, top_right_pos]
'''.strip()

prompt_parse_question = '''
from utils import get_obj_pos, get_obj_names, parse_obj_name, bbox_contains_pt, is_obj_visible

objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl', 'fruit', 'green block', 'black bowl']
# is the blue block to the right of the yellow bowl?
ret_val = get_obj_pos('blue block')[0] > get_obj_pos('yellow bowl')[0]
objects = ['yellow bowl', 'blue block', 'yellow block', 'blue bowl', 'fruit', 'green block', 'black bowl']
# how many yellow objects are there?
yellow_object_names = parse_obj_name('the yellow objects', f'objects = {get_obj_names()}')
ret_val = len(yellow_object_names)
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# is the pink block on the green bowl?
ret_val = bbox_contains_pt(container_name='green bowl', obj_name='pink block')
objects = ['pink block', 'green block', 'pink bowl', 'blue block', 'blue bowl', 'green bowl']
# what are the blocks left of the green bowl?
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
green_bowl_pos = get_obj_pos('green bowl')
left_block_names = []
for block_name in block_names:
  if get_obj_pos(block_name)[0] < green_bowl_pos[0]:
    left_block_names.append(block_name)
ret_val = left_block_names
objects = ['pink block', 'yellow block', 'pink bowl', 'blue block', 'blue bowl', 'yellow bowl']
# is the sun colored block above the blue bowl?
sun_block_name = parse_obj_name('sun colored block', f'objects = {get_obj_names()}')
sun_block_pos = get_obj_pos(sun_block_name)
blue_bowl_pos = get_obj_pos('blue bowl')
ret_val = sun_block_pos[1] > blue_bowl_pos[1]
objects = ['pink block', 'yellow block', 'pink bowl', 'blue block', 'blue bowl', 'yellow bowl']
# is the green block below the blue bowl?
ret_val = get_obj_pos('green block')[1] < get_obj_pos('blue bowl')[1]
'''.strip()

prompt_transform_shape_pts = '''
import numpy as np
from utils import get_obj_pos, get_obj_names, parse_position, parse_obj_name

# make it bigger by 1.5.
new_shape_pts = scale_pts_around_centroid_np(shape_pts, scale_x=1.5, scale_y=1.5)
# move it to the right by 10cm.
new_shape_pts = translate_pts_np(shape_pts, delta=[0.1, 0])
# move it to the top by 20cm.
new_shape_pts = translate_pts_np(shape_pts, delta=[0, 0.2])
# rotate it clockwise by 40 degrees.
new_shape_pts = rotate_pts_around_centroid_np(shape_pts, angle=-np.deg2rad(40))
# rotate by 30 degrees and make it slightly smaller
new_shape_pts = rotate_pts_around_centroid_np(shape_pts, angle=np.deg2rad(30))
new_shape_pts = scale_pts_around_centroid_np(new_shape_pts, scale_x=0.7, scale_y=0.7)
# move it toward the blue block.
block_name = parse_obj_name('the blue block', f'objects = {get_obj_names()}')
block_pos = get_obj_pos(block_name)
mean_delta = np.mean(block_pos - shape_pts, axis=1)
new_shape_pts = translate_pts_np(shape_pts, mean_delta)
'''.strip()

prompt_fgen = '''
# Rules:
# 1. You MUST reply with executable code only. Every natural language comment will make the code invalid.
# 2. The code you write SHOULD NOT be contained in a code block. Write raw code.
# The following is a collection of examples.

import numpy as np
from shapely.geometry import *
from shapely.affinity import *

from env_utils import get_obj_pos, get_obj_names
from ctrl_utils import put_first_on_second

# define function: total = get_total(xs=numbers).
def get_total(xs):
    return np.sum(xs)

# define function: y = eval_line(x, slope, y_intercept=0).
def eval_line(x, slope, y_intercept):
    return x * slope + y_intercept

# define function: pt = get_pt_to_the_left(pt, dist).
def get_pt_to_the_left(pt, dist=0.05):
    return list(np.array(pt) + np.array([0, , 0]))

# define function: pt = get_pt_to_the_top(pt, dist).
def get_pt_to_the_top(pt, dist=0.05):
    return list(np.array(pt) + np.array([0, 0, dist]))

# define function: pt = get_pt_behind(pt, dist).
def get_pt_behind(pt, dist=0.05):
    return list(np.array(pt) + np.array([-dist, 0, 0]))

# define function line = make_line_by_length(length=x).
def make_line_by_length(length):
  line = LineString([[0, 0, 0], [length, 0, 0]])
  return line

# define function: line = make_vertical_line_by_length(length=x).
def make_vertical_line_by_length(length):
  line = make_line_by_length(length)
  vertical_line = rotate(line, 90)
  return vertical_line

# define function: pt = interpolate_line(line, t=0.5).
def interpolate_line(line, t):
  pt = line.interpolate(t, normalized=True)
  return np.array(pt.coords[0])

# example: scale a line by 2.
line = make_line_by_length(1)
new_shape = scale(line, xfact=2, yfact=2)

# example: put object1 on top of object0.
put_first_on_second('object1', 'object0')

# example: get the position of the first object.
obj_names = get_obj_names()
pos_2d = get_obj_pos(obj_names[0])
'''.strip()

TP_PROMPT_CL = """
You are a helpful assistant in charge of controlling a robot manipulator.
There are 4 cubes (red, green, orange, blue) of height 0.04m in the scene with the robot. Your ultimate goal is to give instrcuctions to the robot in order to stack all cubes on top of the green cube.

At each step I will provide you with a description of the scene and the instruction you previously gave the robot. From these you will have to provide the next instruction to the robot. 

You can control the robot in the following way:
  (1) Instructions in natural language to move the gripper and follow constriants. Here's some examples:
      (a) move gripper 0.1m upwards
      (b) move gripper 0.05m above the red cube
      (c) move to the red cube and avoid collisions with the green cube
      (d) keep gripper at a height higher than 0.1m
  (2) open_gripper()
  (3) close_gripper()
      (a) you can firmly grasp an object only if the gripper is at the same position of the center of the object and the gripper is open.

Rules:
  (1) You MUST provide one instruction only at a time.
  (2) You MUST ALWAYS specificy which collisions the gripper has to avoid in your instructions.
  (3) The gripper MUST be at the same location of the center of the object to grasp it.
  (4) ALWAYS give your reasoning about the current scene and about your new instruction.
  (5) You MUST always respond with a json following this format:
      {
      "reasoning": `reasoning`,
      "instruction": `instruction`
      }
"""

TP_PROMPT_OL = """
You are a helpful assistant in charge of controlling a robot manipulator.
The user will give you a goal and you have to formulate a plan that the robot will follow to achieve the goal.

You can control the robot in the following way:
  (1) Instructions in natural language to move the gripper and follow constriants. Here's some examples:
  (2) open_gripper()
  (3) close_gripper()
      (a) you can firmly grasp an object only if the gripper is at the same position of the center of the object and the gripper is open.

Rules:
  (1) You MUST ALWAYS specificy which collisions the gripper has to avoid in your instructions.
  (2) You MUST always respond with a json following this format:
      {
        "tasks": ["task1", "task2", "task3", ...]
      }

Here are some general examples:

objects = ['coffee pod', 'coffee machine']
# Query: put the coffee pod into the coffee machine
{
  "tasks": ["move gripper to the coffee pod and avoid collisions with the coffee machine", "close_gripper()", "move the gripper above the coffee machine", "open_gripper()"]
}

objects = ['blue block', 'yellow block', 'mug']
# Query: place the blue block on the yellow block, and avoid the mug at all time.
{
  "tasks": ["move gripper to the blue block and avoid collisions with the yellow block and the mug", "close_gripper()", "move the gripper above the yellow block and avoid collisions with the yellow block and the mug", "open_gripper()"]
}

objects = ['apple', 'drawer handle', 'drawer']
# Query: put apple into the drawer.
{
  "tasks": ["move gripper to drawer handle and avoid collisions with apple and drawer", "close_gripper()", "move gripper 0.25m in the y direction", "open_gripper()", "move gripper to the apple and avoid collisions with the drawer and its handle", "close_gripper()", "move gripper above the drawer and avoid collisions with the drawer", "open_gripper()"]
}

objects = ['plate', 'fork', 'knife', 'glass]
# Query: Order the kitchen utensils on the table.
{
  "tasks": ["move gripper to the fork and avoid collisions with plate, knife, glass", "close_gripper()", "move gripper to the left side of the plate avoiding collisions with plate, knife, glass", "open_gripper()", "move gripper to the knife and avoid collisions with fork, plate, glass", "close_gripper()", "move gripper to the left side of the fork avoiding collisions with fork, plate, glass", "open_gripper()", "move gripper to the glass and avoid collisions with fork, plate, knife", "close_gripper()", "move gripper in front of the plate avoiding collisions with fork plate knife", "open_gripper()"]
}
"""


OD_PROMPT = """
You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

This is the scene description:
  (1) Casadi is used to program the MPC.
  (2) The variable `x` represents the gripper position of the gripper in 3D, i.e. (x, y, z).
  (2) The variable `x0` represents the initial gripper position at the current time step before any action is applied i.e. (x, y, z).
  (3) The orientation of the gripper around the z-axis is defined by variable `psi`.
  (4) The variable `t` represents the simulation time.
  (5) Each time I will also give you a list of objects you can interact with (i.e. objects = ['peach', 'banana']).
      (a) The position of each object is an array [x, y, z] obtained by adding `.position` (i.e. 'banana.position').
      (b) The size of each cube is a float obtained by adding '.size' (i.e. 'banana.size').
      (c) The rotaton around the z-axis is a float obtained by adding '.psi' (i.e. 'banana.psi').

Rules:
  (1) You MUST write every equality constraints such that it is satisfied if it is = 0:
    (a)  If you want to write "ca.norm_2(x) = 1" write it as  "1 - ca.norm_2(x)" instead.
  (2) You MUST write every inequality constraints such that it is satisfied if it is <= 0:
    (a)  If you want to write "ca.norm_2(x) >= 1" write it as  "1 - ca.norm_2(x)" instead. 
  (3) You MUST avoid colliding with an object if you're moving the gripper to that object, even if not specified in the query.
    (a) Also, avoid collision with an object if I instruct you to move the gripper to a position close (i.e. above or to the right) to that object.
    (b) For the other objects in the scene, if not specified in my instruction, you MUST NOT avoid collisions with them.
  (4) Use `t` in the inequalities especially when you need to describe motions of the gripper.

You must format your response into a json. Here are a few examples:

objects = ['object_1', 'object_2']
# Query: move the gripper to [0.2, 0.05, 0.2] and avoid collisions with object_2
{
  "objective": "ca.norm_2(x - np.array([0.2, 0.05, 0.2]))**2",
  "equality_constraints": [],
  "inequality_constraints": ["object_2.size - ca.norm_2(x - object_2.position)"]
}
Notice how the inequality constraint holds if <= 0.

objects = ['red_cube', 'yellow_cube']
# Query: move the gripper to red cube and avoid colliding with the yellow cube
{
  "objective": "ca.norm_2(x - red_cube.position)**2",
  "equality_constraints": [],
  "inequality_constraints": ["red_cube.size*0.85 - ca.norm_2(x - red_cube.position)", "yellow_cube.size - ca.norm_2(x - yellow_cube.position)"]
}
Notice the collision avoidance constraint with the red_cube despite not being specified in the query.

objects = ['coffee_pod', 'coffee_machine']
# Query: move gripper above the coffe pod and keep gripper at a height higher than 0.1m
{
  "objective": "ca.norm_2(x - (coffee_pod.position + np.array([-0.06, 0, 0])))**2",
  "equality_constraints": [],
  "inequality_constraints": ["coffee_pod.size - ca.norm_2(x - coffee_pod.position)", "0.1 - x[2]"]
}
Notice that there's no collision avoidance constraint with the coffee_machine because not in the query and because gripper is not moving to or nearby it.

objects = ['mug']
# Query: Move the gripper 0.1m upwards
{
  "objective": "ca.norm_2(x - (x0 + np.array([0, 0, 0.1])))**2",
  "equality_constraints": [],
  "inequality_constraints": []
}

objects = ['apple', 'pear']
# Query: move the gripper to apple and stay 0.04m away from pear
{
  "objective": "ca.norm_2(x - apple.position)**2",
  "equality_constraints": [],
  "inequality_constraints": ["apple.size*0.85 - ca.norm_2(x - apple.position)", "0.04 - ca.norm_2(x - pear.position)"]
}

objects = ['joystick', 'remote']
# Query: Move the gripper at constant speed along the x axis while keeping y and z fixed at 0.2m
{
  "objective": "ca.norm_2(x_left[0] - t)**2",
  "equality_constraints": ["np.array([0.2, 0.2]) - x[1:]"],
  "inequality_constraints": []
}

"""

"""
The robot will convert your instruction into a casadi optimization function and solve it using a MPC controller.

Notes:
  1. If the robot is doing something wrong (i.e. it's colliding with a cube) you have to specify that it has to avoid collisions with that specific cube.
  2. Be very meticoulous about the collisions to specify
  3. If you tell the robot to move the gripper to a cube avoiding collisions with it, you don't have to first instruct it to go above the cube and then lower the gripper to grasp it.
  4. The position of the gripper and the cubes is given in the format [x, y, z].
  5. Stacking the cubes means the cubes have to be on top of each other on the z axis.
"""

TP_PROMPT_VISION = """
You are a helpful assistant in charge of controlling a robot manipulator.

There are exactly 4 cubes that the robot can interact with: blue, red, green and orange. All cubes have the same side length of 0.06m.

Your ultimate goal is to give instrcuctions to the robot in order to stack all cubes on top of the green cube.
At each step I will provide you with the image of the current scene and the action that the robot has previously taken. 
The robot actions are in the format of an optimization function written in casadi that is solved by an MPC controller.

Everytime you recieve the image of the current scene you first have to describe accurately the scene, understand if the previous instruction was successful. If not you have to understand why and then provide the next instruction to the robot.

You can control the robot in the following way:
  1. instructions in natural language to move the gripper of the robot
    1.1. x meters from its current position or position of a cube in any direction (i.e. `move gripper 0.1m upwards`)
    1.2. to the center of an object (i.e. `move gripper to the center of the blue cube`)
    1.3. to a posistion avoiding collisions (i.e. `move gripper to [0.3, 0.2, 0.4] avoiding collisions with the red cube`)
  2. open_gripper()
  3. close_gripper()

Rules:
  1. You MUST provide one instruction only at a time
  2. You MUST make your decision only depending on the image provided at the current time step
  3. You MUST always provide the description of the scene before giving the instruction

Notes:
  1. If the robot is doing something wrong (i.e. it's colliding with a cube) you have to specify that it has to avoid collisions with that specific cube.
  2. Be very meticoulous about the collisions to specify
"""



# task planner prompt
OBJECTIVE_TASK_PLANNER_PROMPT = """
  You are a helpful assistant in charge of controlling a robot manipulator.
  Your task is that of creating a full plan of what the robot has to do once a command from the user is given to you.
  This is the description of the scene:
    - There are 4 different cubes that you can manipulate: blue_cube, green_cube, orange_cube, red_cube
    - All cubes have the same side length of 0.08m
    - If you want to pick a cube: first move the gripper above the cube and then lower it to be able to grasp the cube:
        Here's an example if you want to pick a cube:
        ~~~
        1. Go to a position above the cube
        2. Go to the position of the cube
        3. Close gripper
        4. ...
        ~~~
    - If you want to drop a cube: open the gripper and then move the gripper above the cube so to avoid collision. 
        Here's an example if you want to drop a cube at a location:
        ~~~
        1. Go to a position above the desired location 
        2. Open gripper to drop cube
        2. Go to a position above cube
        3. ...
        ~~~  
    - If you are dropping a cube always specify not to collide with other cubes.
  
  You can control the robot in the following way:
    1. move the gripper of the robot to a position
    2. open gripper
    3. close gripper
  
  {format_instructions}
  """

OPTIMIZATION_TASK_PLANNER_PROMPT_CUBES = """
You are a helpful assistant in charge of controlling a robot manipulator.
Your task is that of creating a full and precise plan of what the robot has to do once a command from the user is given to you.
This is the description of the scene:
  - There are 4 different cubes that you can manipulate: blue_cube, green_cube, orange_cube, red_cube
  - All cubes have the same side length of 0.09m
  - When moving the gripper specify which cubes it has to avoid collisions with
  - Make sure to avoid the cubes from colliding with each other when you pick and place them

You can control the robot in the following way:
  1. move the gripper of the robot
  2. open gripper
  3. close gripper

Rules:
  1. If you want to pick a cube you have to avoid colliding with all cubes, including the one to pick
  2. If you already picked a cube (i.e. you closed the gripper) then you must not avoid colliding with that specific cube

{format_instructions}
"""

OPTIMIZATION_TASK_PLANNER_PROMPT_CLEAN_PLATE = """
You are a helpful assistant in charge of controlling a robot manipulator.
Your task is that of creating a full and precise plan of what the robot has to do once a command from the user is given to you.
This is the description of the scene:
  - There are 2 objects on the table: sponge, plate.
  - The sponge has the shape of a cube with side length 0.03m
  - The plate has circular shape with radius of 0.05m.
  - When moving the gripper specify if it has to avoid collisions with any object

You can control the robot in the following way:
  1. move the gripper of the robot
  2. move the gripper in some defined motion
  3. open gripper
  4. close gripper

Rules:
  1. If you want to pick an object you have to avoid colliding with all objects, including the one to pick
  2. If you already picked an object then you must not avoid colliding with that specific object

{format_instructions}
"""

OPTIMIZATION_TASK_PLANNER_PROMPT_MOVE_TABLE = """
You are a helpful assistant in charge of controlling 2 robots.
Your task is that of creating a detailed and precise plan of what the robots have to do once a command from the user is given to you.

This is the description of the scene:
  - The robots are called: left robot and right robot.
  - There are is a table with 2 handles. The handles are called left handle and right handle and that's where the table can be picked from.
  - The table  has a length of 0.5m, width of 0.25m and height 0.25m.
  - The table has 4 legs with heiht of 0.25m.
  - There is also an obstacle on the floor which has cylindrical shape with radius 0.07m.
  - Both the obstacle and the table are rotated such that they are parallel to the y axis.
  - When moving the grippers specify if it has to avoid collisions with any object

You can control the robot in the following way:
  1. move the gripper of the robots
  2. move the grippers in some defined motion
  3. open grippers
  4. close grippers

Rules:
  1. If you want to pick an object you have to specify to avoid colliding with all objects, including the one to pick
  2. If you already picked an object then you must not specify avoid colliding with that specific object
  3. For each single task you MUST specify what BOTH robots have to do at the same time:
      Good:
      - Move the left robot to the left handle and move the right robot to the right handle
      Bad:
      - Move the left robot to the sink
      - Move the right robot above the sponge

{format_instructions}
"""

OPTIMIZATION_TASK_PLANNER_PROMPT_SPONGE = """
You are a helpful assistant in charge of controlling 2 robots.
Your task is that of creating a detailed and precise plan of what the robots have to do once a command from the user is given to you.

This is the description of the scene:
  - The robots are called: left robot and right robot.
  - There are 2 objects positioned on a table: container, sponge.
  - There is a sink a bit far from the table.
  - The sponge has the shape of a cube with side length 0.03m
  - The container has circular shape with radius of 0.05m.
  - The container can be picked from the container_handle which is located at [0.05m, 0, 0] with respect to the center of the container and has lenght of 0.1m
  - When moving the gripper specify if it has to avoid collisions with any object

You can control the robot in the following way:
  1. move the gripper of the robots
  2. move the grippers in some defined motion
  3. open grippers
  4. close grippers

Rules:
  1. If you want to pick an object you have to specify to avoid colliding with all objects, including the one to pick
  2. If you already picked an object then you must not specify avoid colliding with that specific object
  3. For each single task you MUST specify what BOTH robots have to do at the same time:
      Good:
      - Move the left robot to the sink and move the right robot above the sponge
      Bad:
      - Move the left robot to the sink
      - Move the right robot above the sponge

{format_instructions}
"""
# Move the sponge to the sink but since the sponge is wet you have to find a way to prevent water from falling onto the table 

# optimization designer prompt
OBJECTIVE_DESIGNER_PROMPT = """
  You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipultor.
  At each step, I will give you a task and you will have to return the objective that need to be applied to the MPC controller.

  This is the scene description:
    - The robot manipulator sits on a table and its gripper starts at a home position.
    - The MPC controller is used to generate a the trajectory of the gripper.
    - CVXPY is used to program the MPC and the state variable is called self.x
    - The state variable self.x[t] represents the position of the gripper in position x, y, z at timestep t.
    - The whole MPC horizon has length self.cfg.T = 15
    - There are 4 cubes on the table.
    - All cubes have side length of 0.08m.
    - At each timestep I will give you 1 task. You have to convert this task into an objective for the MPC.

  Here is example 1:
  ~~~
  Task: 
      move the gripper behind blue_cube
  Output:
      sum([cp.norm(xt - (blue_cube + np.array([-0.08, 0, 0]) )) for xt in self.x]) # gripper is moved 1 side lenght behind blue_cube
  ~~~

  {format_instructions}
  """


OPTIMIZATION_DESIGNER_PROMPT = """
  You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
  At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

  This is the scene description:
    - The robot manipulator sits on a table and its gripper starts at a home position.
    - The MPC controller is used to generate a the trajectory of the gripper.
    - CVXPY is used to program the MPC and the state variable is called self.x
    - The state variable self.x[t] represents the position of the gripper in position x, y, z at timestep t.
    - There are 4 cubes on the table.
    - All cubes have side length of 0.05m.
    - You are only allowed to use constraint inequalities and not equalities.

  Here is example 1:
  ~~~
  Task: 
      "move the gripper 0.1m behind blue_cube"
  Output:
      reward = "sum([cp.norm(xt - (blue_cube - np.array([0.1, 0.0, 0.0]))) for xt in self.x])" # gripper is moved 1 side lenght behind blue_cube
      constraints = [""]
  ~~~

  {format_instructions}
  """


# optimization designer prompt
NMPC_OBJECTIVE_DESIGNER_PROMPT = """
  You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipultor.
  At each step, I will give you a task and you will have to return the objective that need to be applied to the MPC controller.

  This is the scene description:
    - The robot manipulator sits on a table and its gripper starts at a home position.
    - The MPC controller is used to generate a the trajectory of the gripper.
    - Casadi is used to program the MPC and the state variable is called x
    - There are 4 cubes on the table.
    - All cubes have side length of 0.0468m.
    - At each timestep I will give you 1 task. You have to convert this task into an objective for the MPC.

  Here is example 1:
  ~~~
  Task: 
      move the gripper behind blue_cube
  Output:
      objective = "ca.norm_2(x - (blue_cube + np.array([-0.0468, 0, 0])))**2" 
  ~~~

  {format_instructions}
  """


NMPC_OPTIMIZATION_DESIGNER_PROMPT_CUBES = """
You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

This is the scene description:
  - The robot manipulator sits on a table and its gripper starts at a home position.
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x` represents the gripper position of the gripper in 3D, i.e. (x, y, z).
  - The variables `x0` represents the fixed position of the gripper before any action is applied.
  - The orientation of the gripper around the z-axis is defined by variable `psi`.
  - The variable `t` represents the simulation time.
  - There are 4 cubes on the table and the variables `red_cube` `blue_cube` `green_cube` `orange_cube` represent their postions in 3D.
  - The orientations around the z-axis of each cube are defined by variables `blue_cube_psi` `green_cube_psi` `orange_cube_psi` `red_cube_psi`.
  - All cubes have side length of 0.06m.

Rules:
  - You MUST write every equality constraints such that it is satisfied if it is = 0:
      If you want to write "ca.norm_2(x) = 1" write it as  "1 - ca.norm_2(x)" instead.
  - You MUST write every inequality constraints such that it is satisfied if it is <= 0:
      If you want to write "ca.norm_2(x) >= 1" write it as  "1 - ca.norm_2(x)" instead. 
  - You MUST provide the constraints as a list of strings.
  - The objective and constraints can be a function of `x`, `blue_cube`, `blue_cube_psi`, ... and/or `t`. 
  - Use `t` in the inequalities especially when you need to describe motions of the gripper.
  - If you want to avoid colliding with a cube, the right safety margin is half of its side length.


Example 1:
~~~
Task: 
    "move the gripper to [0.2, 0.05, 0.2] and avoid collisions with object_2"
Output:
    "objective": "ca.norm_2(x - np.array([0.2, 0.05, 0.2]))**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.04 - ca.norm_2(x - object_2)"]
~~~
Notice how the inequality constraint holds if <= 0.

Example 2:
~~~
Task: 
    "move the gripper to blue cube"
Output:
    "objective": "ca.norm_2(x - blue_cube)**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.03 - ca.norm_2(x - blue_cube)"]
~~~

Example 3:
~~~
Task: 
    "move gripper behind the blue cube and keep gripper at a height higher than 0.1m"
Output:
    "objective": "ca.norm_2(x - (blue_cube + np.array([-0.06, 0, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.1 - x[2]"]
~~~
Notice how the inequality constraint holds if <= 0.

Example 4:
~~~
Task: 
    "Move the gripper 0.1m upwards"
Output:
    "objective": "ca.norm_2(x - (x0 + np.array([0, 0, 0.1])))**2",
    "equality_constraints": [],
    "inequality_constraints": []
~~~

Example 5:
~~~
Task: 
    "move the gripper to object_1 and avoid collisions with object_2"
Output:
    "objective": "ca.norm_2(x - object_1)**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.03 - ca.norm_2(x - object_1)", "0.04 - ca.norm_2(x - object_2)"]
~~~

Example 6:
~~~
Task: 
    "Move the gripper at constant speed along the x axis while keeping y and z fixed at 0.2m"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2",
    "equality_constraints": ["np.array([0.2, 0.2]) - x[1:]"],
    "inequality_constraints": []
~~~


{format_instructions}
"""

"""
  - If you want to avoid colliding with a cube, use the following numbers for the collision avoidance inequality constraints of the cubes:
      - Cube you are going to grasp (specified in instruction): 0.035m
      - Cube you just released (specified in instruction): 0.045m
      - Any other cube: 0.045m
"""

NMPC_OBJECTIVE_DESIGNER_PROMPT_CUBES = """
You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
At each step, I will give you a task and you will have to return the objective function that needS to be applied to the MPC controller.

This is the scene description:
  - The robot manipulator sits on a table and its gripper starts at a home position.
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x` represents the gripper position of the gripper in 3D, i.e. (x, y, z).
  - The variables `x0` represents the fixed position of the gripper before any action is applied.
  - The variable `t` represents the simulation time.
  - There are 4 cubes on the table and the variables `blue_cube` `green_cube` `orange_cube` `red_cube` represent their postions in 3D.
  - All cubes have side length of 0.04685m.

Rules:
  - The objective can be a function of `x`, `sponge`, `plate` and/or `t`. 
  - Use `t` especially when you need to describe motions of the gripper.
    

Example 1:
~~~
Task: 
    "move gripper 0.03m behind the blue_cube"
Output:
    "objective": "ca.norm_2(x - (blue_cube + np.array([-0.03, 0, 0])))**2"
~~~

Example 2:
~~~
Task: 
    "Move the gripper at constant speed along the x axis"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2"
~~~

Example 3:
~~~
Task: 
    "Move the gripper 0.1m upwards"
Output:
    "objective": "ca.norm_2(x - (x0 + np.array([0, 0, 0.1])))**2"
~~~

  {format_instructions}
  """

NMPC_OPTIMIZATION_DESIGNER_PROMPT_CLEAN_PLATE = """
  You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
  At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x` represents the gripper position of the gripper in 3D, i.e. (x, y, z).
  - The variables `x0` represents the fixed position of the gripper before any action is applied.
  - The variable `t` represents the simulation time.
  - There variables `sponge` and `plate` represent the 3D position of a sponge and a plate located on the table.
  - The sponge has the shape of a cube and has side length of 0.03m.
  - The plate has circular shape and has radius of 0.05m.

Rules:
  - You MUST write every equality constraints such that it is satisfied if it is = 0:
      If you want to write "ca.norm_2(x) = 1" write it as  "1 - ca.norm_2(x)" instead.
  - You MUST write every inequality constraints such that it is satisfied if it is <= 0:
      If you want to write "ca.norm_2(x) >= 1" write it as  "1 - ca.norm_2(x)" instead. 
  - You MUST provide the constraints as a list of strings.
  - The objective and constraints can be a function of `x`, `sponge`, `plate` and/or `t`. 
  - Use `t` in the inequalities especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move gripper 0.03m behind the songe and keep gripper at a height higher than 0.1m"
Output:
    "objective": "ca.norm_2(x - (sponge + np.array([-0.03, 0, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.1 - ca.norm_2(x[2])"]
~~~
Notice how the inequality constraint holds if <= 0.

Example 2:
~~~
Task: 
    "Move the gripper at constant speed along the x axis while keeping y and z fixed at 0.2m"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2",
    "equality_constraints": ["np.array([0.2, 0.2]) - x[1:]"],
    "inequality_constraints": []
~~~

Example 3:
~~~
Task: 
    "Move the gripper 0.1m upwards"
Output:
    "objective": "ca.norm_2(x - (x0 + np.array([0, 0, 0.1])))**2",
    "equality_constraints": [],
    "inequality_constraints": []
~~~

{format_instructions}
"""

NMPC_OBJECTIVE_DESIGNER_PROMPT_CLEAN_PLATE = """
  You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling a robot manipulator. 
  At each step, I will give you a task and you will have to return the objective function that needs to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x` represents the gripper position of the gripper in 3D, i.e. (x, y, z).
  - The variables `x0` represents the fixed position of the gripper before any action is applied.
  - The variable `t` represents the simulation time.
  - There variables `sponge` and `plate` represent the 3D position of a sponge and a plate located on the table.
  - The sponge has the shape of a cube and has side length of 0.03m.
  - The plate has circular shape and has radius of 0.05m.

Rules:
  - The objective can be a function of `x`, `sponge`, `plate` and/or `t`. 
  - Use `t` in the especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move gripper 0.03m behind the sponge"
Output:
    "objective": "ca.norm_2(x - (sponge + np.array([-0.03, 0, 0])))**2"
~~~

Example 2:
~~~
Task: 
    "Move the gripper at constant speed along the x axis"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2"
~~~

Example 3:
~~~
Task: 
    "Move the gripper 0.1m upwards"
Output:
    "objective": "ca.norm_2(x - (x0 + np.array([0, 0, 0.1])))**2"
~~~

{format_instructions}
"""

NMPC_OPTIMIZATION_DESIGNER_PROMPT_MOVE_TABLE = """
You are a helpful assistant in charge of designing the optimization problem of a Model Predictive Controller (MPC) that is controlling 2 robot manipulators. 
At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x_left` represents the gripper position of the left robot in 3D, i.e. (x, y, z).
  - The variable `x_right` represents the gripper position of the right robot in 3D, i.e. (x, y, z).
  - The variables `x0_left` and `x0_right` represent the fixed position of the grippers before any action is applied.
  - There is a table of length 0.5m, width of 0.25m and height 0.25m. The variable `table` represents the position of the table center in 3D, i.e. (x,y,z)
  - The table has 4 legs with heiht of 0.25m.
  - The variables `handle_left` and `handle_right` represent the position of the table handles. The handles are located on top of the table.
  - The variable `obstacle` represents the position of an obstacle. The obstacle is on the floor and has cylindrical shape with radius 0.07m.
  - Both the obstacle and the table are rotated such that they are parallel to the y axis.
  - The variable `t` represents the simulation time.

Rules:
  - You MUST write every equality constraints such that it is satisfied if it is = 0:
      If you want to write "ca.norm_2(x) = 1" write it as  "1 - ca.norm_2(x)" instead.
  - You MUST write every inequality constraints such that it is satisfied if it is <= 0:
      If you want to write "ca.norm_2(x) >= 1" write it as  "1 - ca.norm_2(x)" instead. 
  - You MUST provide the constraints as a list of strings.
  - The objective and constraints can be a function of `x_left`, `x_right`, `table`, `handle_left`, `handle_right` and/or `t`. 
  - Use `t` in the inequalities especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move the left gripper 0.03m behind handle_left and keep gripper at a height higher than 0.1m"
Output:
    "objective": "ca.norm_2(x_left - (handle_left + np.array([-0.03, 0, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.1 - ca.norm_2(x_left[2])"]
~~~
Notice how the inequality constraint holds if <= 0.

Example 2:
~~~
Task: 
    "Move the left gripper at constant speed along the x axis while keeping y and z fixed at 0.2m and the right gripper in the opposite direction"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2 + ca.norm_2(x_right[0] + t)**2",
    "equality_constraints": ["np.array([0.2, 0.2]) - x_left[1:]", "np.array([0.2, 0.2]) - x_right[1:]"],
    "inequality_constraints": []
~~~

Example 3:
~~~
Task: 
    "Move the left gripper 0.1m upwards and the right gripper 0.2m to the right"
Output:
    "objective": "ca.norm_2(x_left - (x0_left + np.array([0, 0, 0.1])))**2 + ca.norm_2(x_right - (x0_right + np.array([0, -0.2, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": []
~~~

{format_instructions}
"""

NMPC_OBJECTIVE_DESIGNER_PROMPT_MOVE_TABLE = """
You are a helpful assistant in charge of designing the optimization problem of a Model Predictive Controller (MPC) that is controlling 2 robot manipulators. 
At each step, I will give you a task and you will have to return the objective function that needs to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the gripper.
  - Casadi is used to program the MPC.
  - The variable `x_left` represents the gripper position of the left robot in 3D, i.e. (x, y, z).
  - The variable `x_right` represents the gripper position of the right robot in 3D, i.e. (x, y, z).
  - The variables `x0_left` and `x0_right` represent the fixed position of the grippers before any action is applied.
  - There is a table of length 0.5m, width of 0.25m and height 0.25m. The variable `table` represents the position of the table center in 3D, i.e. (x,y,z)
  - The table has 4 legs with heiht of 0.25m.
  - The variables `handle_left` and `handle_right` represent the position of the table handles. The handles are located on top of the table.
  - The variable `obstacle` represents the position of an obstacle. The obstacle is on the floor and has cylindrical shape with radius 0.07m.
  - Both the obstacle and the table are rotated such that they are parallel to the y axis.
  - The variable `t` represents the simulation time.

Rules:
  - The objective and constraints can be a function of `x_left`, `x_right`, `table`, `handle_left`, `handle_right` and/or `t`. 
  - Use `t` especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move the left gripper 0.03m behind handle_left"
Output:
    "objective": "ca.norm_2(x_left - (handle_left + np.array([-0.03, 0, 0])))**2"
~~~

Example 2:
~~~
Task: 
    "Move the left gripper at constant speed along the x axis"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2 + ca.norm_2(x_right[0] + t)**2"
~~~

Example 3:
~~~
Task: 
    "Move the left gripper 0.1m upwards and the right gripper 0.2m to the right"
Output:
    "objective": "ca.norm_2(x_left - (x0_left + np.array([0, 0, 0.1])))**2 + ca.norm_2(x_right - (x0_right + np.array([0, -0.2, 0])))**2"
~~~

{format_instructions}
"""

NMPC_OPTIMIZATION_DESIGNER_PROMPT_SPONGE = """
You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling 2 robot manipulators. 
At each step, I will give you a task and you will have to return the objective and (optionally) the constraint functions that need to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the robot grippers.
  - Casadi is used to program the MPC.
  - The variable `x_left` represents the gripper position of the left robot in 3D, i.e. (x, y, z).
  - The variable `x_right` represents the gripper position of the right robot in 3D, i.e. (x, y, z).
  - The variables `x0_left` and `x0_right` represent the fixed position of the grippers before any action is applied.
  - The variables `container`, `sponge` and `sink` represent the position of a container, a sponge and a sink.
  - The container has circular shape with radius 0.05m, the sponge has cubic shape with side length of 0.05m.
  - The container can only be picked from the `container_handle` which is located at +[0.05, 0, 0] compared to the container.
  - The variable `t` represents the simulation time.

Rules:
  - You MUST write every equality constraints such that it is satisfied if it is = 0:
      If you want to write "ca.norm_2(x) = 1" write it as  "1 - ca.norm_2(x)" instead.
  - You MUST write every inequality constraints such that it is satisfied if it is <= 0:
      If you want to write "ca.norm_2(x) >= 1" write it as  "1 - ca.norm_2(x)" instead. 
  - You MUST provide the constraints as a list of strings.
  - The objective and constraints can be a function of `x_left`, `x_right`, `container`, `container_handle`, `sponge`, `sink` and/or `t`. 
  - Use `t` in the inequalities especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move the left gripper 0.03m behind container_handle and keep gripper at a height higher than 0.1m"
Output:
    "objective": "ca.norm_2(x_left - (container_handle + np.array([-0.03, 0, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": ["0.1 - ca.norm_2(x_left[2])"]
~~~
Notice how the inequality constraint holds if <= 0.

Example 2:
~~~
Task: 
    "Move the left gripper at constant speed along the x axis while keeping y and z fixed at 0.2m and the right gripper in the opposite direction"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2 + ca.norm_2(x_right[0] + t)**2",
    "equality_constraints": ["np.array([0.2, 0.2]) - x_left[1:]", "np.array([0.2, 0.2]) - x_right[1:]"],
    "inequality_constraints": []
~~~

Example 3:
~~~
Task: 
    "Move the left gripper 0.1m upwards and the right gripper 0.2m to the right"
Output:
    "objective": "ca.norm_2(x_left - (x0_left + np.array([0, 0, 0.1])))**2 + ca.norm_2(x_right - (x0_right + np.array([0, -0.2, 0])))**2",
    "equality_constraints": [],
    "inequality_constraints": []
~~~

{format_instructions}
"""

NMPC_OBJECTIVE_DESIGNER_PROMPT_SPONGE = """
You are a helpful assistant in charge of designing the optimization problem for an MPC controller that is controlling 2 robot manipulators. 
At each step, I will give you a task and you will have to return the objective and function that needs to be applied to the MPC controller.

This is the scene description:
  - The MPC controller is used to generate the trajectory of the robot grippers.
  - Casadi is used to program the MPC.
  - The variable `x_left` represents the gripper position of the left robot in 3D, i.e. (x, y, z).
  - The variable `x_right` represents the gripper position of the right robot in 3D, i.e. (x, y, z).
  - The variables `x0_left` and `x0_right` represent the fixed position of the grippers before any action is applied.
  - The variables `container`, `sponge` and `sink` represent the position of a container, a sponge and a sink.
  - The container has circular shape with radius 0.05m, the sponge has cubic shape with side length of 0.05m.
  - The container can only be picked from the `container_handle` which is located at +[0.05, 0, 0] compared to the container.
  - The variable `t` represents the simulation time.

Rules:
  - The objective and constraints can be a function of `x_left`, `x_right`, `container`, `container_handle`, `sponge`, `sink` and/or `t`. 
  - Use `t` in the inequalities especially when you need to describe motions of the gripper.

Example 1:
~~~
Task: 
    "move the left gripper 0.03m behind container_handle"
Output:
    "objective": "ca.norm_2(x_left - (container_handle + np.array([-0.03, 0, 0])))**2"
~~~

Example 2:
~~~
Task: 
    "Move the left gripper at constant speed along the x axis while keeping y and z fixed at 0.2m and the right gripper in the opposite direction"
Output:  
    "objective": "ca.norm_2(x_left[0] - t)**2 + ca.norm_2(x_right[0] + t)**2"
~~~

Example 3:
~~~
Task: 
    "Move the left gripper 0.1m upwards and the right gripper 0.2m to the right"
Output:
    "objective": "ca.norm_2(x_left - (x0_left + np.array([0, 0, 0.1])))**2 + ca.norm_2(x_right - (x0_right + np.array([0, -0.2, 0])))**2"
~~~

{format_instructions}
"""


PROMPTS = {
    "TP_OL": {
        "Cubes": TP_PROMPT_OL
    },
    "TP_CL": {
        "Cubes": TP_PROMPT_CL
    },
    "OD": {
        "Cubes": OD_PROMPT,
    },
}

TP_PROMPTS = {
  "stack": TP_PROMPT_CL,
  "pyramid": TP_PROMPT_CL,
  "L": TP_PROMPT_CL,
  "reverse": TP_PROMPT_CL,
  "clean_plate": OPTIMIZATION_TASK_PLANNER_PROMPT_CLEAN_PLATE,
  "move_table": OPTIMIZATION_TASK_PLANNER_PROMPT_MOVE_TABLE,
  "sponge": OPTIMIZATION_TASK_PLANNER_PROMPT_SPONGE
}

OD_PROMPTS = {
  "stack": NMPC_OPTIMIZATION_DESIGNER_PROMPT_CUBES,
  "pyramid": NMPC_OPTIMIZATION_DESIGNER_PROMPT_CUBES,
  "L": NMPC_OPTIMIZATION_DESIGNER_PROMPT_CUBES,
  "reverse": NMPC_OPTIMIZATION_DESIGNER_PROMPT_CUBES,
  "clean_plate": NMPC_OPTIMIZATION_DESIGNER_PROMPT_CLEAN_PLATE,
  "move_table": NMPC_OPTIMIZATION_DESIGNER_PROMPT_MOVE_TABLE,
  "sponge": NMPC_OPTIMIZATION_DESIGNER_PROMPT_SPONGE
}
