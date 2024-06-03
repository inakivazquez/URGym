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
    id='URGym/CubesGrasp-v0',
    entry_point='urgym.envs.env_cubes_grasp_v0:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/CubesGrasp-v1',
    entry_point='urgym.envs.env_cubes_grasp_v1:CubesGrasp',
    max_episode_steps=20,
)

register(
    id='URGym/CubesGrasp-v2',
    entry_point='urgym.envs.env_cubes_grasp_v2:CubesGrasp',
    max_episode_steps=20,
)