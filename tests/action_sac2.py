from typing import Any, Dict, Iterator, List, Optional, Tuple, Type, Union

import torch as th
import torch.nn as nn

from gymnasium import spaces

from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.noise import ActionNoise
from stable_baselines3.sac.policies import Actor, SACPolicy
from stable_baselines3.sac.sac import SAC
from stable_baselines3.common.type_aliases import GymEnv, Schedule
from stable_baselines3.common.torch_layers import (
    BaseFeaturesExtractor,
    CombinedExtractor,
    FlattenExtractor,
    NatureCNN,
    create_mlp,
    get_actor_critic_arch,
)

class SuperNet(nn.Module):
    def __init__(self, features_dim:int, action_layers:list, n_nodes:int=64):
        super(SuperNet, self).__init__()
        
        # Subnets specific for each action
        self.subnet_action = nn.ModuleList()

        for i in range(len(action_layers)):
            # Add the subnets for each action
            self.subnet_action.extend([nn.Sequential(
                nn.Linear(features_dim, n_nodes),
                nn.ReLU(),
                nn.Linear(n_nodes, action_layers[i][0]),
                action_layers[i][1]() 
            )])

    def forward(self, x):
        action_outputs = th.cat([subnet_action(x) for subnet_action in self.subnet_action], dim=1)
        return action_outputs
        
class AdvancedActor(Actor):
    def __init__(
        self,
        observation_space: spaces.Space,
        action_space: spaces.Box,
        net_arch: List[int],
        features_extractor: nn.Module,
        features_dim: int,
        activation_fn: Type[nn.Module] = nn.ReLU,
        use_sde: bool = False,
        log_std_init: float = -3,
        full_std: bool = True,
        use_expln: bool = False,
        clip_mean: float = 2.0,
        normalize_images: bool = True,
        action_config: Optional[Dict[str, Any]] = None,
    ):
        super(AdvancedActor, self).__init__(observation_space, action_space, net_arch, features_extractor, features_dim, activation_fn, 
                                            use_sde, log_std_init, full_std, use_expln, clip_mean, normalize_images)
        
        n_nodes = action_config['n_nodes']
        action_layers = action_config['layers']
        self.latent_pi = SuperNet(features_dim=features_dim, action_layers=action_layers, n_nodes=n_nodes).to(self.device)
    
class AdvancedSACPolicy(SACPolicy):
    def __init__(
        self,
        observation_space: spaces.Space,
        action_space: spaces.Box,
        lr_schedule: Schedule,
        net_arch: Optional[Union[List[int], Dict[str, List[int]]]] = None,
        activation_fn: Type[nn.Module] = nn.ReLU,
        use_sde: bool = False,
        log_std_init: float = -3,
        use_expln: bool = False,
        clip_mean: float = 2.0,
        features_extractor_class: Type[BaseFeaturesExtractor] = FlattenExtractor,
        features_extractor_kwargs: Optional[Dict[str, Any]] = None,
        normalize_images: bool = True,
        optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
        optimizer_kwargs: Optional[Dict[str, Any]] = None,
        n_critics: int = 2,
        share_features_extractor: bool = False,
        action_config: Optional[Dict[str, Any]] = None,
    ):
        self.action_config = action_config # Here as it is used during the super() call
        super(AdvancedSACPolicy, self).__init__(observation_space, action_space, lr_schedule, net_arch, activation_fn, use_sde, log_std_init, use_expln, clip_mean, features_extractor_class, features_extractor_kwargs, normalize_images, optimizer_class, optimizer_kwargs, n_critics, share_features_extractor)

    def make_actor(self, features_extractor: Optional[BaseFeaturesExtractor] = None) -> AdvancedActor:
        actor_kwargs = self._update_features_extractor(self.actor_kwargs, features_extractor)
        actor = AdvancedActor(**actor_kwargs, action_config=self.action_config).to(self.device)
        actor.mu = nn.Identity()
        return actor


class A_SAC(SAC):
    policy: AdvancedSACPolicy
    actor: AdvancedActor

    def __init__(
        self,
        policy: Union[str, Type[SACPolicy]],
        env: Union[GymEnv, str],
        learning_rate: Union[float, Schedule] = 3e-4,
        buffer_size: int = 1_000_000,  # 1e6
        learning_starts: int = 100,
        batch_size: int = 256,
        tau: float = 0.005,
        gamma: float = 0.99,
        train_freq: Union[int, Tuple[int, str]] = 1,
        gradient_steps: int = 1,
        action_noise: Optional[ActionNoise] = None,
        replay_buffer_class: Optional[Type[ReplayBuffer]] = None,
        replay_buffer_kwargs: Optional[Dict[str, Any]] = None,
        optimize_memory_usage: bool = False,
        ent_coef: Union[str, float] = "auto",
        target_update_interval: int = 1,
        target_entropy: Union[str, float] = "auto",
        use_sde: bool = False,
        sde_sample_freq: int = -1,
        use_sde_at_warmup: bool = False,
        stats_window_size: int = 100,
        tensorboard_log: Optional[str] = None,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
    ):        
        
        super().__init__(policy, env, learning_rate, buffer_size, learning_starts, batch_size, tau, gamma, train_freq, gradient_steps, action_noise, replay_buffer_class, replay_buffer_kwargs, optimize_memory_usage, ent_coef, target_update_interval, target_entropy, use_sde, sde_sample_freq, use_sde_at_warmup, stats_window_size, tensorboard_log, policy_kwargs, verbose, seed, device, _init_setup_model)

