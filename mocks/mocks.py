
optimization_mock_plan_stack = '''
{"tasks":[
  "move the gripper to cube_4 and avoid any collision with every cube",
  "close gripper",
  "move the gripper on top of cube_2 and avoid colliding with cube_2, cube_3 and cube_1",
  "open gripper",
  "move gripper to cube_3 and avoid collisions with every cube",
  "close gripper",
  "move gripper above of cube_4 and avoid collisions with every cube apart from cube_3",
  "open gripper",
  "move gripper to cube_1 and avoid collisions with every cube",
  "close gripper",
  "move gripper above cube_3 and avoid collisions with every cube apart from cube_1",
  "open gripper"
]}
'''

optimization_mock_plan_pyramid = '''
{"tasks":[
  "move the gripper to cube_4 and avoid any collision with every cube",
  "close gripper",
  "move the gripper next to cube_3 and avoid colliding with cube_2, cube_3 and cube_1",
  "open gripper",
  "move gripper to cube_2 and avoid collisions with every cube",
  "close gripper",
  "move gripper at a height above cube_3 and cube_4 and in between them. Also avoid collisions with every cube apart from cube_2",
  "open gripper"
]}
'''

optimization_mock_plan_L = '''
{"tasks":[
  "move the gripper to cube_4 and avoid any collision with every cube",
  "close gripper",
  "move the gripper to the left side (y axis) of cube_3 and avoid colliding with cube_1, cube_2 and cube_3",
  "open gripper",
  "move gripper to cube_2 and avoid collisions with every cube",
  "close gripper",
  "move gripper behind cube_3 and avoid collisions with cube_1, cube_3, cube_4",
  "open gripper",
  "move gripper to cube_1 and avoid collisions with every cube",
  "close gripper",
  "move gripper behind cube_2 and avoid colliding with cube_1, cube_3, cube_4",
  "open gripper",
]} 
'''

objective_mock_plan = '''
{"tasks":[
  "move the gripper above cube_4",
  "move gripper to the position of cube_4",
  "close gripper",
  "move the gripper above cube_2 and avoid collisions with every cube",
  "open gripper",
  "move gripper above cube_3 and avoid collisions with every cube",
  "move gripper to the position of cube_3",
  "close gripper",
  "move the gripper above cube_4 and avoid collisions with every cube",
  "open gripper",
  "move gripper to above cube_1 and avoid collisions with every cube",
  "move gripper to the position of cube_1",
  "close gripper",
  "move gripper above cube_3 and avoid collisions with every cube apart from cube_1",
  "open gripper"
]}
'''

optimization_mock_plan_clean_plate = '''
{"tasks":[
  "move the gripper to the sponge",
  "close gripper",
  "move the gripper up 0.03m with the sponge avoiding collision with the plate",
  "move the gripper 0.02m above the plate avoiding collision with the plate",
  "move the gripper in circular motion over the plate"
]}
'''

TP_move_table = '''
{"tasks":[
  "move left gripper to left handle and right gripper to right handle"
]}
'''

OD_mock = '''
{
  "objective": "ca.norm_2(x - sponge)**2",
  "constraints": [
    "0.03 - ca.norm_2(x - sponge)",
    "0.05 - ca.norm_2(x - plate)"
    ]
} 
''' 

OD_move_table = '''
{
  "objective": "ca.norm_2(x_left - (handle_left+np.array([0,0,0.05])))**2 + ca.norm_2(x_right - (handle_right+np.array([0,0,0.05])))**2",
  "constraints": [
    "0.07 - ca.norm_2(x_left - handle_left)",
    "0.07 - ca.norm_2(x_right - handle_right)"
    ]
} 
'''

nmpcMockOptions = {
  "nmpc_objective": objective_mock_plan,
  "stack": optimization_mock_plan_stack,
  "pyramid": optimization_mock_plan_pyramid,
  "L": optimization_mock_plan_L,
  "clean_plate": optimization_mock_plan_clean_plate,
  "OD": OD_mock,
  "OD_move_table": OD_move_table,
  "move_table": TP_move_table
}