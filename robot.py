import numpy as np
from llm import LLM, VLM
from core import AbstractRobot
from controller import Controller
from typing import Tuple, List, Dict
from config.config import RobotConfig, TPConfig, ODConfig


class Robot(AbstractRobot):
  def __init__(self, env_info:Tuple[List], cfg=RobotConfig()) -> None:
    self.cfg = cfg

    self.gripper = 1. # 1 means the gripper is open
    self.gripper_timer = 0
    self.TP = VLM(TPConfig(self.cfg.task))
    self.OD = LLM(ODConfig(self.cfg.task))
    
    self.MPC = Controller(env_info)

  def init_states(self, observation:Dict[str, np.ndarray], t:float):
      """ Update simulation time and current state of MPC controller"""
      self.MPC.init_states(observation, t)

  def _open_gripper(self):
    self.gripper = 0.
    self.gripper_timer = 0

  def _close_gripper(self):
    self.gripper = -1.

  def plan_task(self, user_message:str, base64_image=None) -> str:
    """ Runs the Task Planner by passing the user message and the current frame """
    return self.TP.run(user_message, base64_image)

  def solve_task(self, plan:str) -> str:
    """ Applies and returns the optimization designed by the Optimization Designer """
    # if custom function is called apply that
    if "open_gripper" in plan.lower():
      self._open_gripper()
      #simulate_stream("OD", "\n```\n open_gripper()\n```\n")
      return "\n```\n open_gripper()\n```\n"
    elif "close_gripper" in plan.lower():
      self._close_gripper()
      #simulate_stream("OD", "\n```\n close_gripper()\n```\n")
      return "\n```\n close_gripper()\n```\n"
    # catch if reply cannot be parsed. i.e. when askin the LLM a question
    try:
      # design optimization functions
      optimization = self.OD.run(plan)
      # apply optimization functions to MPC
      self.MPC.setup_controller(optimization)
      return optimization.pretty_print()
    except Exception as e:
      print(f"Error: {e}")
      return "ERROR"

  def step(self):
    action = []
    # compute actions from controller (single or dual robot)
    control: List[np.ndarray] = self.MPC.step()
    for u in control:
      action.append(np.hstack((u, self.gripper)))  
    
    # Logic for opening and closing gripper
    if self.gripper==0 and self.gripper_timer>self.cfg.open_gripper_time: 
      self.gripper = 1.
    else:
      self.gripper_timer += 1

    return action

  def retrieve_trajectory(self):
    return self.MPC.retrieve_trajectory()
    
    
    