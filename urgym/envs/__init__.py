from gymnasium.envs.registration import register

register(
    id='URGym/Box-v0',
    entry_point='urgym.envs.env_box_v0:BoxManipulation',
    max_episode_steps=200,
    kwargs=dict(button_touch_mode='any')
)

register(
    id='URGym/CubesPush-v0',
    entry_point='urgym.envs.env_cubes_push_v0:CubesPush',
    max_episode_steps=50,
)

register(
    id='URGym/CubesPush-v1',
    entry_point='urgym.envs.env_cubes_push_v1:CubesPush',
    max_episode_steps=50,
)

register(
    id='URGym/CubesGrasp-v0',
    entry_point='urgym.envs.env_cubes_grasp_v0:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/CubesGrasp-v1',
    entry_point='urgym.envs.env_cubes_grasp_v1:CubesGrasp',
    max_episode_steps=20,
)

#
register(
    id='URGym/CubesGrasp-v2',
    entry_point='urgym.envs.env_cubes_grasp_v2:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/CubesGrasp-v3',
    entry_point='urgym.envs.env_cubes_grasp_v3:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/CubesGraspVertical-v3',
    entry_point='urgym.envs.env_cubes_grasp_v3:CubesGrasp',
    max_episode_steps=20,
    kwargs=dict(vertical_reward=True)
)

register(
    id='URGym/CubesGrasp-v4',
    entry_point='urgym.envs.env_cubes_grasp_v4:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/BallBalance-v0',
    entry_point='urgym.envs.env_ball_balance_v0:BallBalance',
    max_episode_steps=500,
)

register(
    id='URGym/TwoBallsBalance-v0',
    entry_point='urgym.envs.env_two_balls_balance_v0:TwoBallsBalance',
    max_episode_steps=500,
)

register(
    id='URGym/Golf-v0',
    entry_point='urgym.envs.env_golf_v0:Golf',
    max_episode_steps=100,
)

register(
    id='URGym/GolfJoints-v0',
    entry_point='urgym.envs.env_golf_joints_v0:Golf',
    max_episode_steps=100,
)