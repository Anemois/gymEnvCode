from gymnasium.envs.registration import register

register(
    id='HSREnv-v1',
    entry_point='HSREnv.envs:environment',
    max_episode_steps=500
)