---
id: action-generation-and-execution
title: Action Generation and Execution
sidebar_position: 5
description: Converting multimodal inputs to robotic actions in VLA models
---

# Action Generation and Execution

<div className="vla-module">
  <p>This lesson covers converting multimodal inputs to robotic actions in Vision-Language-Action (VLA) models.</p>
</div>

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the action generation process in VLA models
- Implement action space mapping from multimodal inputs
- Design action execution pipelines for robotic systems
- Validate action generation performance
- Handle action constraints and safety considerations

## Prerequisites

- Understanding of VLA model architecture
- Completed language grounding lesson
- Knowledge of robotics control concepts
- Basic understanding of action spaces and kinematics

## Introduction to Action Generation

Action generation in VLA models refers to the process of converting multimodal inputs (vision, language, proprioception) into executable robotic actions. This is the final step in the VLA pipeline that translates perception and understanding into physical behavior.

### Key Components of Action Generation

1. **Feature Integration**: Combining multimodal features into action space
2. **Action Space Mapping**: Converting features to robot-specific actions
3. **Constraint Enforcement**: Ensuring actions are feasible and safe
4. **Execution Planning**: Sequencing actions for complex tasks
5. **Feedback Integration**: Incorporating execution results for refinement

### Action Generation Pipeline

```
Multimodal Input → Feature Fusion → Action Mapping → Constraint Application → Action Execution
     ↓                  ↓              ↓                ↓                    ↓
  Vision, Language,   Combined     Action Vector   Feasibility Check   Robot Command
  Proprioception     Representation    (6-DoF, etc.)     (Safety, Limits)     Execution
```

## Action Space Representation

### Continuous Action Spaces

Most robotic systems use continuous action spaces representing joint velocities, end-effector velocities, or Cartesian positions:

```python
#!/usr/bin/env python3
# action_spaces.py
# Action space representations for VLA models

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class ActionSpace:
    """Different action space representations"""

    def __init__(self, space_type="continuous", dimensions=6):
        self.space_type = space_type
        self.dimensions = dimensions

    def get_action_bounds(self):
        """Get action space bounds"""
        if self.space_type == "continuous":
            # Continuous actions: -1 to 1 normalized
            return torch.full((self.dimensions,), -1.0), torch.full((self.dimensions,), 1.0)
        elif self.space_type == "discrete":
            # Discrete actions: categorical
            return torch.arange(self.dimensions), torch.arange(self.dimensions)
        else:
            raise ValueError(f"Unknown action space type: {self.space_type}")

    def normalize_action(self, action):
        """Normalize action to [-1, 1] range"""
        if self.space_type == "continuous":
            # Assuming action is already in [-1, 1] or needs clipping
            return torch.clamp(action, -1.0, 1.0)
        else:
            # For discrete actions, return as-is
            return action

    def denormalize_action(self, normalized_action, robot_specific_params):
        """Convert normalized action to robot-specific action"""
        if self.space_type == "continuous":
            # Convert to robot-specific ranges based on robot parameters
            # Example: joint velocity, Cartesian velocity, etc.
            action_range = robot_specific_params.get('action_range', 1.0)
            return normalized_action * action_range
        else:
            return normalized_action

class ContinuousActionNetwork(nn.Module):
    """Network for generating continuous actions"""

    def __init__(self, input_dim=512, action_dim=6, hidden_dims=[256, 128]):
        super().__init__()

        self.input_dim = input_dim
        self.action_dim = action_dim
        self.hidden_dims = hidden_dims

        # Build network layers
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.1)
            ])
            prev_dim = hidden_dim

        # Output layer for actions
        layers.append(nn.Linear(prev_dim, action_dim))

        self.network = nn.Sequential(*layers)

        # Action normalization layer
        self.action_normalizer = nn.Tanh()  # Ensures output in [-1, 1]

    def forward(self, features):
        """
        Generate continuous actions from input features
        Args:
            features: (batch, input_dim) - multimodal features
        Returns:
            actions: (batch, action_dim) - normalized continuous actions
        """
        raw_actions = self.network(features)
        normalized_actions = self.action_normalizer(raw_actions)
        return normalized_actions

class DiscreteActionNetwork(nn.Module):
    """Network for generating discrete actions"""

    def __init__(self, input_dim=512, num_actions=10, hidden_dims=[256, 128]):
        super().__init__()

        self.input_dim = input_dim
        self.num_actions = num_actions
        self.hidden_dims = hidden_dims

        # Build network layers
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.1)
            ])
            prev_dim = hidden_dim

        # Output layer for action logits
        layers.append(nn.Linear(prev_dim, num_actions))

        self.network = nn.Sequential(*layers)

    def forward(self, features):
        """
        Generate discrete action logits from input features
        Args:
            features: (batch, input_dim) - multimodal features
        Returns:
            action_logits: (batch, num_actions) - action selection logits
        """
        action_logits = self.network(features)
        return action_logits

    def sample_action(self, features, temperature=1.0):
        """
        Sample action from the action distribution
        Args:
            features: (batch, input_dim) - multimodal features
            temperature: float - sampling temperature
        Returns:
            sampled_actions: (batch,) - sampled action indices
        """
        action_logits = self.forward(features)
        scaled_logits = action_logits / temperature

        # Apply softmax to get probabilities
        action_probs = F.softmax(scaled_logits, dim=-1)

        # Sample from the distribution
        sampled_actions = torch.multinomial(action_probs, 1).squeeze(-1)

        return sampled_actions, action_probs

# Example usage
def main():
    # Create continuous action network
    continuous_net = ContinuousActionNetwork(input_dim=512, action_dim=6)

    # Create discrete action network
    discrete_net = DiscreteActionNetwork(input_dim=512, num_actions=10)

    # Create dummy input features
    batch_size = 4
    input_features = torch.randn(batch_size, 512)

    # Generate continuous actions
    continuous_actions = continuous_net(input_features)
    print(f"Continuous actions shape: {continuous_actions.shape}")
    print(f"Continuous actions range: [{continuous_actions.min():.3f}, {continuous_actions.max():.3f}]")

    # Generate discrete actions
    action_logits = discrete_net(input_features)
    sampled_actions, action_probs = discrete_net.sample_action(input_features)

    print(f"Action logits shape: {action_logits.shape}")
    print(f"Sampled actions: {sampled_actions}")
    print(f"Action probabilities shape: {action_probs.shape}")
    print(f"Top action probabilities: {action_probs[0].topk(3)}")

if __name__ == "__main__":
    main()
```

## Multimodal Feature Fusion for Action Generation

### Feature Integration Techniques

```python
#!/usr/bin/env python3
# feature_fusion.py
# Multimodal feature fusion for action generation

import torch
import torch.nn as nn
import torch.nn.functional as F

class MultimodalFusion(nn.Module):
    """Fusion of visual, language, and proprioceptive features for action generation"""

    def __init__(self, visual_dim=512, language_dim=512, proprioceptive_dim=128, fused_dim=512):
        super().__init__()

        self.visual_dim = visual_dim
        self.language_dim = language_dim
        self.proprioceptive_dim = proprioceptive_dim
        self.fused_dim = fused_dim

        # Individual modality encoders
        self.visual_encoder = nn.Sequential(
            nn.Linear(visual_dim, fused_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        self.language_encoder = nn.Sequential(
            nn.Linear(language_dim, fused_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        self.proprioceptive_encoder = nn.Sequential(
            nn.Linear(proprioceptive_dim, fused_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        # Cross-attention fusion
        self.cross_attention = nn.MultiheadAttention(
            embed_dim=fused_dim,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )

        # Fusion network
        self.fusion_network = nn.Sequential(
            nn.Linear(fused_dim * 3, fused_dim * 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(fused_dim * 2, fused_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(fused_dim, fused_dim)
        )

        # Residual connection
        self.residual_proj = nn.Linear(fused_dim * 3, fused_dim)

        # Layer normalization
        self.norm = nn.LayerNorm(fused_dim)

    def forward(self, visual_features, language_features, proprioceptive_features):
        """
        Fuse multimodal features for action generation
        Args:
            visual_features: (batch, visual_dim) - visual features
            language_features: (batch, language_dim) - language features
            proprioceptive_features: (batch, proprioceptive_dim) - proprioceptive features
        Returns:
            fused_features: (batch, fused_dim) - fused multimodal features
        """
        # Encode each modality
        encoded_visual = self.visual_encoder(visual_features)
        encoded_language = self.language_encoder(language_features)
        encoded_proprio = self.proprioceptive_encoder(proprioceptive_features)

        # Stack modalities for attention
        modalities = torch.stack([encoded_visual, encoded_language, encoded_proprio], dim=1)
        # Shape: (batch, 3, fused_dim)

        # Apply cross-attention
        attended_modalities, attention_weights = self.cross_attention(modalities, modalities, modalities)

        # Flatten and concatenate
        flattened = attended_modalities.view(-1, 3 * self.fused_dim)

        # Apply fusion network
        fused_output = self.fusion_network(flattened)

        # Apply residual connection
        residual = self.residual_proj(flattened)
        fused_features = self.norm(fused_output + residual)

        return fused_features, attention_weights

class HierarchicalActionGenerator(nn.Module):
    """Hierarchical action generator with coarse-to-fine planning"""

    def __init__(self, fused_dim=512, coarse_action_dim=3, fine_action_dim=6):
        super().__init__()

        self.fused_dim = fused_dim
        self.coarse_action_dim = coarse_action_dim
        self.fine_action_dim = fine_action_dim

        # Coarse action prediction (high-level goals)
        self.coarse_action_net = nn.Sequential(
            nn.Linear(fused_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, coarse_action_dim),
            nn.Tanh()  # Normalize to [-1, 1]
        )

        # Fine action prediction (low-level motor commands)
        self.fine_action_net = nn.Sequential(
            nn.Linear(fused_dim + coarse_action_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, fine_action_dim),
            nn.Tanh()  # Normalize to [-1, 1]
        )

        # Action refinement network
        self.refinement_net = nn.Sequential(
            nn.Linear(fused_dim + fine_action_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, fine_action_dim)
        )

    def forward(self, fused_features):
        """
        Generate hierarchical actions
        Args:
            fused_features: (batch, fused_dim) - fused multimodal features
        Returns:
            coarse_actions: (batch, coarse_action_dim) - high-level actions
            fine_actions: (batch, fine_action_dim) - low-level actions
            refined_actions: (batch, fine_action_dim) - refined actions
        """
        # Generate coarse actions
        coarse_actions = self.coarse_action_net(fused_features)

        # Generate fine actions conditioned on coarse actions
        fine_input = torch.cat([fused_features, coarse_actions], dim=-1)
        fine_actions = self.fine_action_net(fine_input)

        # Refine actions based on multimodal context
        refine_input = torch.cat([fused_features, fine_actions], dim=-1)
        refined_actions = self.refinement_net(refine_input)

        # Combine with original fine actions
        final_actions = fine_actions + refined_actions

        return coarse_actions, fine_actions, final_actions

# Example usage
def main():
    # Create fusion module
    fusion_module = MultimodalFusion()

    # Create hierarchical action generator
    action_generator = HierarchicalActionGenerator()

    # Create dummy inputs
    batch_size = 2
    visual_features = torch.randn(batch_size, 512)
    language_features = torch.randn(batch_size, 512)
    proprioceptive_features = torch.randn(batch_size, 128)

    # Fuse features
    fused_features, attention_weights = fusion_module(visual_features, language_features, proprioceptive_features)

    print(f"Fused features shape: {fused_features.shape}")
    print(f"Attention weights shape: {attention_weights.shape}")

    # Generate hierarchical actions
    coarse_actions, fine_actions, refined_actions = action_generator(fused_features)

    print(f"Coarse actions shape: {coarse_actions.shape}")
    print(f"Fine actions shape: {fine_actions.shape}")
    print(f"Refined actions shape: {refined_actions.shape}")

    print(f"Sample coarse actions: {coarse_actions[0].detach().numpy()}")
    print(f"Sample fine actions: {fine_actions[0].detach().numpy()}")
    print(f"Sample refined actions: {refined_actions[0].detach().numpy()}")

if __name__ == "__main__":
    main()
```

## Action Constraint and Safety Enforcement

### Safety and Feasibility Checking

```python
#!/usr/bin/env python3
# action_constraints.py
# Action constraint and safety enforcement for VLA models

import torch
import torch.nn as nn
import numpy as np

class ActionConstraintEnforcer:
    """Enforce constraints on generated actions for safety and feasibility"""

    def __init__(self, robot_limits=None, safety_zones=None, joint_names=None):
        """
        Initialize constraint enforcer
        Args:
            robot_limits: Dict with joint limits {'joint_name': {'min': value, 'max': value}}
            safety_zones: List of safety zones to avoid
            joint_names: List of joint names
        """
        self.robot_limits = robot_limits or {}
        self.safety_zones = safety_zones or []
        self.joint_names = joint_names or []

    def enforce_joint_limits(self, actions, joint_indices=None):
        """
        Enforce joint limits on actions
        Args:
            actions: (batch, action_dim) - actions to constrain
            joint_indices: List of indices corresponding to joint actions
        Returns:
            constrained_actions: (batch, action_dim) - actions within limits
        """
        constrained_actions = actions.clone()

        if joint_indices:
            for i, joint_idx in enumerate(joint_indices):
                joint_name = self.joint_names[joint_idx] if joint_idx < len(self.joint_names) else f"joint_{joint_idx}"

                if joint_name in self.robot_limits:
                    min_val = self.robot_limits[joint_name]['min']
                    max_val = self.robot_limits[joint_name]['max']

                    # Clamp to limits
                    constrained_actions[:, joint_idx] = torch.clamp(
                        constrained_actions[:, joint_idx], min_val, max_val
                    )

        return constrained_actions

    def check_safety_zones(self, actions, current_state=None):
        """
        Check if actions would violate safety zones
        Args:
            actions: (batch, action_dim) - proposed actions
            current_state: (batch, state_dim) - current robot state
        Returns:
            safe_actions: (batch, action_dim) - safe actions
            violations: (batch,) - boolean tensor indicating violations
        """
        violations = torch.zeros(actions.size(0), dtype=torch.bool)

        # Simple implementation - in practice, you'd have more complex safety checks
        for i, action in enumerate(actions):
            for zone in self.safety_zones:
                # Check if action would move into safety zone
                # This is a simplified example - real implementation would check trajectory
                if zone['type'] == 'circular':
                    # Check distance from center
                    center = torch.tensor(zone['center'])
                    radius = zone['radius']
                    distance = torch.norm(action[:2] - center[:2])  # Assume first 2 dims are x,y
                    if distance < radius:
                        violations[i] = True
                elif zone['type'] == 'rectangular':
                    # Check if action is within rectangular bounds
                    min_bounds = torch.tensor(zone['min_bounds'])
                    max_bounds = torch.tensor(zone['max_bounds'])
                    if torch.any(action < min_bounds) or torch.any(action > max_bounds):
                        violations[i] = True

        return actions, violations

    def smooth_actions(self, actions, previous_actions=None, smoothing_factor=0.1):
        """
        Smooth actions to prevent jerky movements
        Args:
            actions: (batch, action_dim) - current actions
            previous_actions: (batch, action_dim) - previous actions
            smoothing_factor: float - smoothing coefficient
        Returns:
            smoothed_actions: (batch, action_dim) - smoothed actions
        """
        if previous_actions is None:
            return actions

        # Apply smoothing: new_action = (1-smoothing)*current + smoothing*previous
        smoothed_actions = (1 - smoothing_factor) * actions + smoothing_factor * previous_actions
        return smoothed_actions

class SafeActionGenerator(nn.Module):
    """Action generator with built-in safety enforcement"""

    def __init__(self, action_dim=6, hidden_dim=256, robot_limits=None):
        super().__init__()

        self.action_dim = action_dim
        self.hidden_dim = hidden_dim

        # Action generation network
        self.action_net = nn.Sequential(
            nn.Linear(512, hidden_dim),  # Input from multimodal fusion
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim)
        )

        # Action normalization
        self.action_normalizer = nn.Tanh()

        # Constraint enforcer
        self.constraint_enforcer = ActionConstraintEnforcer(robot_limits=robot_limits)

        # Store previous actions for smoothing
        self.register_buffer('previous_actions', torch.zeros(1, action_dim))

    def forward(self, fused_features, enforce_constraints=True, smooth_actions=True):
        """
        Generate safe actions from fused features
        Args:
            fused_features: (batch, feature_dim) - fused multimodal features
            enforce_constraints: bool - whether to enforce constraints
            smooth_actions: bool - whether to smooth actions
        Returns:
            safe_actions: (batch, action_dim) - safe, constrained actions
        """
        # Generate raw actions
        raw_actions = self.action_net(fused_features)
        normalized_actions = self.action_normalizer(raw_actions)

        safe_actions = normalized_actions

        if enforce_constraints:
            # Apply joint limits (assuming first few dimensions are joints)
            joint_indices = list(range(min(6, self.action_dim)))  # First 6 as example joint indices
            safe_actions = self.constraint_enforcer.enforce_joint_limits(safe_actions, joint_indices)

        if smooth_actions:
            # Smooth with previous actions
            batch_size = safe_actions.size(0)
            prev_actions_expanded = self.previous_actions.expand(batch_size, -1)
            safe_actions = self.constraint_enforcer.smooth_actions(
                safe_actions, prev_actions_expanded, smoothing_factor=0.1
            )

        # Update previous actions for next call
        self.previous_actions = safe_actions[0].unsqueeze(0)  # Store first in batch

        return safe_actions

# Example usage
def main():
    # Define robot limits
    robot_limits = {
        'joint_1': {'min': -1.5, 'max': 1.5},
        'joint_2': {'min': -1.0, 'max': 1.0},
        'joint_3': {'min': -2.0, 'max': 2.0},
        'joint_4': {'min': -1.5, 'max': 1.5},
        'joint_5': {'min': -1.0, 'max': 1.0},
        'joint_6': {'min': -2.5, 'max': 2.5}
    }

    # Create safe action generator
    safe_generator = SafeActionGenerator(action_dim=6, robot_limits=robot_limits)

    # Create dummy fused features
    batch_size = 2
    fused_features = torch.randn(batch_size, 512)

    # Generate safe actions
    safe_actions = safe_generator(fused_features)

    print(f"Safe actions shape: {safe_actions.shape}")
    print(f"Sample safe actions: {safe_actions[0].detach().numpy()}")
    print(f"Action limits check: min={safe_actions.min():.3f}, max={safe_actions.max():.3f}")

    # Test with multiple calls to see smoothing effect
    print("\nTesting smoothing over multiple calls:")
    for i in range(3):
        actions = safe_generator(fused_features)
        print(f"  Call {i+1} - Action range: [{actions.min():.3f}, {actions.max():.3f}]")

if __name__ == "__main__":
    main()
```

## Action Execution Planning

### Sequential Action Planning

```python
#!/usr/bin/env python3
# action_planning.py
# Sequential action planning for complex tasks

import torch
import torch.nn as nn
import numpy as np

class ActionPlanner(nn.Module):
    """Plan sequences of actions for complex tasks"""

    def __init__(self, action_dim=6, hidden_dim=256, max_sequence_length=20):
        super().__init__()

        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.max_sequence_length = max_sequence_length

        # Task embedding network
        self.task_embedder = nn.Sequential(
            nn.Linear(512, hidden_dim),  # From language/visual features
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        # Sequence generation LSTM
        self.sequence_lstm = nn.LSTM(
            input_size=hidden_dim + action_dim,  # Task + previous action
            hidden_size=hidden_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.1
        )

        # Action prediction for each step
        self.action_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Normalize to [-1, 1]
        )

        # Step completion predictor
        self.completion_predictor = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()  # Probability of step completion
        )

    def forward(self, task_features, current_state=None):
        """
        Plan a sequence of actions for a task
        Args:
            task_features: (batch, feature_dim) - task representation
            current_state: (batch, state_dim) - current robot state
        Returns:
            action_sequence: (batch, max_seq_len, action_dim) - planned actions
            completion_probs: (batch, max_seq_len) - completion probabilities
        """
        batch_size = task_features.size(0)

        # Embed task
        task_embed = self.task_embedder(task_features)  # (batch, hidden_dim)

        # Initialize sequence
        action_sequence = []
        completion_probs = []

        # Initialize previous action (start with zeros)
        prev_action = torch.zeros(batch_size, self.action_dim, device=task_features.device)

        # Plan sequence step by step
        for step in range(self.max_sequence_length):
            # Combine task embedding and previous action
            lstm_input = torch.cat([task_embed, prev_action], dim=-1).unsqueeze(1)
            # Shape: (batch, 1, hidden_dim + action_dim)

            # If this is the first step, initialize LSTM hidden state
            if step == 0:
                lstm_out, (hidden, cell) = self.sequence_lstm(lstm_input)
            else:
                lstm_out, (hidden, cell) = self.sequence_lstm(lstm_input, (hidden, cell))

            # Predict action for this step
            step_action = self.action_predictor(lstm_out.squeeze(1))  # (batch, action_dim)
            action_sequence.append(step_action)

            # Predict completion probability
            completion_prob = self.completion_predictor(lstm_out.squeeze(1)).squeeze(-1)  # (batch,)
            completion_probs.append(completion_prob)

            # Update previous action for next iteration
            prev_action = step_action

        # Stack sequences
        action_sequence = torch.stack(action_sequence, dim=1)  # (batch, max_seq_len, action_dim)
        completion_probs = torch.stack(completion_probs, dim=1)  # (batch, max_seq_len)

        return action_sequence, completion_probs

class HierarchicalActionPlanner(nn.Module):
    """Hierarchical action planner with high-level and low-level planning"""

    def __init__(self, action_dim=6, hidden_dim=256, max_high_level_steps=5, max_low_level_steps=10):
        super().__init__()

        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.max_high_level_steps = max_high_level_steps
        self.max_low_level_steps = max_low_level_steps

        # High-level planner (abstract goals)
        self.high_level_planner = nn.Sequential(
            nn.Linear(512, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        )

        # High-level goal predictor
        self.goal_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim)  # Abstract goal representation
        )

        # Low-level action generator for each high-level goal
        self.low_level_generator = nn.Sequential(
            nn.Linear(hidden_dim + action_dim, hidden_dim),  # Task + goal
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        )

        # Low-level action predictor
        self.low_level_action_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim),
            nn.Tanh()
        )

    def forward(self, task_features):
        """
        Generate hierarchical action plan
        Args:
            task_features: (batch, feature_dim) - task representation
        Returns:
            high_level_goals: (batch, max_high_steps, action_dim) - high-level goals
            low_level_actions: (batch, max_high_steps, max_low_steps, action_dim) - detailed actions
        """
        batch_size = task_features.size(0)

        # High-level planning
        # Repeat task features for sequence length
        repeated_task = task_features.unsqueeze(1).expand(-1, self.max_high_level_steps, -1)

        # Process through high-level planner
        high_level_out, _ = self.high_level_planner(repeated_task)

        # Predict high-level goals
        high_level_goals = self.goal_predictor(high_level_out)  # (batch, max_high_steps, action_dim)

        # Low-level planning for each high-level goal
        low_level_actions = []

        for goal_step in range(self.max_high_level_steps):
            # Get current goal
            current_goal = high_level_goals[:, goal_step, :].unsqueeze(1).expand(-1, self.max_low_level_steps, -1)

            # Combine task and goal for low-level planning
            low_level_input = torch.cat([
                task_features.unsqueeze(1).expand(-1, self.max_low_level_steps, -1),
                current_goal
            ], dim=-1)

            # Process through low-level generator
            low_level_out, _ = self.low_level_generator(low_level_input)

            # Predict low-level actions
            step_actions = self.low_level_action_predictor(low_level_out)  # (batch, max_low_steps, action_dim)
            low_level_actions.append(step_actions)

        # Stack low-level actions
        low_level_actions = torch.stack(low_level_actions, dim=1)  # (batch, max_high_steps, max_low_steps, action_dim)

        return high_level_goals, low_level_actions

# Example usage
def main():
    # Create action planner
    planner = ActionPlanner(action_dim=6, max_sequence_length=10)

    # Create hierarchical planner
    hier_planner = HierarchicalActionPlanner(action_dim=6)

    # Create dummy task features
    batch_size = 2
    task_features = torch.randn(batch_size, 512)

    # Plan sequential actions
    action_sequence, completion_probs = planner(task_features)

    print(f"Action sequence shape: {action_sequence.shape}")
    print(f"Completion probabilities shape: {completion_probs.shape}")
    print(f"Sample action sequence (first 3 steps):")
    for i in range(3):
        print(f"  Step {i}: {action_sequence[0, i].detach().numpy()}")

    # Plan hierarchical actions
    high_level_goals, low_level_actions = hier_planner(task_features)

    print(f"\nHigh-level goals shape: {high_level_goals.shape}")
    print(f"Low-level actions shape: {low_level_actions.shape}")
    print(f"Sample high-level goal: {high_level_goals[0, 0].detach().numpy()}")
    print(f"Sample low-level actions (first high-level step, first 2 low-level steps):")
    for i in range(2):
        print(f"  Low-level step {i}: {low_level_actions[0, 0, i].detach().numpy()}")

if __name__ == "__main__":
    main()
```

## Action Execution and Feedback Integration

### Closed-Loop Action Execution

```python
#!/usr/bin/env python3
# closed_loop_execution.py
# Closed-loop action execution with feedback integration

import torch
import torch.nn as nn
import numpy as np

class ClosedLoopActionExecutor:
    """Execute actions in closed-loop with feedback integration"""

    def __init__(self, action_generator, max_steps=100, tolerance=0.01):
        self.action_generator = action_generator
        self.max_steps = max_steps
        self.tolerance = tolerance

        # Store execution history
        self.execution_history = []

    def execute_task(self, task_features, initial_state, target_state, robot_interface):
        """
        Execute a task with closed-loop feedback
        Args:
            task_features: (feature_dim,) - task representation
            initial_state: (state_dim,) - initial robot state
            target_state: (state_dim,) - target robot state
            robot_interface: Robot interface object with execute_action method
        Returns:
            success: bool - whether task was completed successfully
            execution_log: list - execution history
        """
        current_state = initial_state.clone()
        step_count = 0
        success = False

        execution_log = []

        while step_count < self.max_steps:
            # Calculate remaining distance to target
            distance_to_target = torch.norm(current_state - target_state)

            # Check if task is complete
            if distance_to_target < self.tolerance:
                success = True
                break

            # Generate action based on current state and task
            # In practice, you'd combine task features with current state
            action_input = torch.cat([task_features, current_state])

            # This is simplified - in practice, you'd have a network that takes state + task
            with torch.no_grad():
                # Generate action (this is where you'd call your VLA model)
                action = self.action_generator(action_input)

            # Execute action through robot interface
            executed_action = robot_interface.execute_action(action)

            # Get feedback from robot
            new_state = robot_interface.get_current_state()

            # Log execution step
            step_log = {
                'step': step_count,
                'action': action.numpy(),
                'executed_action': executed_action.numpy(),
                'current_state': current_state.numpy(),
                'new_state': new_state.numpy(),
                'distance_to_target': distance_to_target.item(),
                'success': torch.norm(new_state - target_state) < self.tolerance
            }

            execution_log.append(step_log)

            # Update current state
            current_state = new_state
            step_count += 1

        return success, execution_log

class FeedbackIntegrator(nn.Module):
    """Integrate feedback into action generation"""

    def __init__(self, action_dim=6, hidden_dim=256, feedback_dim=128):
        super().__init__()

        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.feedback_dim = feedback_dim

        # Feedback processing network
        self.feedback_processor = nn.Sequential(
            nn.Linear(feedback_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim // 2, hidden_dim // 2)
        )

        # Action refinement network
        self.refinement_net = nn.Sequential(
            nn.Linear(512 + hidden_dim // 2, hidden_dim),  # Task + feedback
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim)
        )

        # Action adjustment predictor
        self.adjustment_predictor = nn.Sequential(
            nn.Linear(512 + hidden_dim // 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Adjustment in [-1, 1]
        )

    def forward(self, task_features, feedback_features, current_action):
        """
        Refine action based on feedback
        Args:
            task_features: (batch, feature_dim) - task representation
            feedback_features: (batch, feedback_dim) - feedback from execution
            current_action: (batch, action_dim) - current action
        Returns:
            refined_action: (batch, action_dim) - refined action
            adjustment: (batch, action_dim) - action adjustment
        """
        # Process feedback
        processed_feedback = self.feedback_processor(feedback_features)

        # Combine task and feedback
        combined_features = torch.cat([task_features, processed_feedback], dim=-1)

        # Predict adjustment
        adjustment = self.adjustment_predictor(combined_features)

        # Apply adjustment to current action
        refined_action = current_action + adjustment

        return refined_action, adjustment

class AdaptiveActionGenerator(nn.Module):
    """Adaptive action generator that learns from execution feedback"""

    def __init__(self, action_dim=6, hidden_dim=256):
        super().__init__()

        self.action_dim = action_dim
        self.hidden_dim = hidden_dim

        # Main action generator
        self.main_generator = nn.Sequential(
            nn.Linear(512, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()
        )

        # Error prediction network
        self.error_predictor = nn.Sequential(
            nn.Linear(512 + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Predicted error adjustment
        )

        # Adaptation network
        self.adaptation_net = nn.Sequential(
            nn.Linear(512 + action_dim + action_dim, hidden_dim),  # task + action + error
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()
        )

    def forward(self, task_features, previous_action=None, execution_error=None):
        """
        Generate action with adaptation based on past performance
        Args:
            task_features: (batch, feature_dim) - task representation
            previous_action: (batch, action_dim) - previous action taken
            execution_error: (batch, action_dim) - error from previous execution
        Returns:
            action: (batch, action_dim) - generated action
        """
        # Generate main action
        main_action = self.main_generator(task_features)

        if previous_action is not None and execution_error is not None:
            # Use error prediction to adapt
            adaptation_input = torch.cat([task_features, previous_action, execution_error], dim=-1)
            adaptation = self.adaptation_net(adaptation_input)
            action = main_action + adaptation
        else:
            action = main_action

        return action

# Example usage
def main():
    # Create adaptive action generator
    adaptive_generator = AdaptiveActionGenerator(action_dim=6)

    # Create feedback integrator
    feedback_integrator = FeedbackIntegrator(action_dim=6)

    # Create dummy inputs
    batch_size = 2
    task_features = torch.randn(batch_size, 512)
    feedback_features = torch.randn(batch_size, 128)
    current_action = torch.randn(batch_size, 6)
    previous_action = torch.randn(batch_size, 6)
    execution_error = torch.randn(batch_size, 6)

    # Generate adaptive action
    adaptive_action = adaptive_generator(task_features, previous_action, execution_error)

    print(f"Adaptive action shape: {adaptive_action.shape}")
    print(f"Sample adaptive action: {adaptive_action[0].detach().numpy()}")

    # Integrate feedback
    refined_action, adjustment = feedback_integrator(task_features, feedback_features, current_action)

    print(f"Refined action shape: {refined_action.shape}")
    print(f"Adjustment shape: {adjustment.shape}")
    print(f"Sample refined action: {refined_action[0].detach().numpy()}")
    print(f"Sample adjustment: {adjustment[0].detach().numpy()}")

if __name__ == "__main__":
    main()
```

## Hands-on Exercise: Action Generation System

### Exercise Objective
Implement a complete action generation and execution system for VLA models.

### Steps to Complete

1. Create a multimodal feature fusion network
2. Implement action space mapping with constraints
3. Add sequential planning capabilities
4. Integrate feedback mechanisms
5. Validate the action generation system

### Complete Action Generation System

```python
#!/usr/bin/env python3
# complete_action_system.py
# Complete action generation and execution system for VLA models

import torch
import torch.nn as nn
import torch.nn.functional as F

class CompleteActionGenerationSystem(nn.Module):
    """Complete action generation system for VLA models"""

    def __init__(self, visual_dim=512, language_dim=512, proprioceptive_dim=128, action_dim=6):
        super().__init__()

        self.action_dim = action_dim

        # Multimodal fusion
        self.fusion_module = MultimodalFusion(visual_dim, language_dim, proprioceptive_dim)

        # Hierarchical action generation
        self.hierarchical_generator = HierarchicalActionGenerator(
            fused_dim=512,  # Output of fusion module
            coarse_action_dim=3,
            fine_action_dim=action_dim
        )

        # Action planner
        self.action_planner = ActionPlanner(action_dim=action_dim)

        # Safe action generator
        self.safe_generator = SafeActionGenerator(action_dim=action_dim)

        # Feedback integrator
        self.feedback_integrator = FeedbackIntegrator(action_dim=action_dim)

        # Adaptive generator
        self.adaptive_generator = AdaptiveActionGenerator(action_dim=action_dim)

    def forward(self, visual_features, language_features, proprioceptive_features,
                feedback_features=None, previous_action=None, execution_error=None,
                plan_sequence=False, use_feedback=False, adapt_action=False):
        """
        Complete action generation pipeline
        Args:
            visual_features: (batch, visual_dim) - visual features
            language_features: (batch, language_dim) - language features
            proprioceptive_features: (batch, proprioceptive_dim) - proprioceptive features
            feedback_features: (batch, feedback_dim) - execution feedback (optional)
            previous_action: (batch, action_dim) - previous action (optional)
            execution_error: (batch, action_dim) - execution error (optional)
            plan_sequence: bool - whether to plan action sequence
            use_feedback: bool - whether to use feedback integration
            adapt_action: bool - whether to adapt based on past performance
        Returns:
            actions: (batch, action_dim) - generated actions
            additional_outputs: dict - additional outputs based on flags
        """
        # Fuse multimodal features
        fused_features, attention_weights = self.fusion_module(
            visual_features, language_features, proprioceptive_features
        )

        # Generate hierarchical actions
        coarse_actions, fine_actions, refined_actions = self.hierarchical_generator(fused_features)

        # Choose action based on hierarchy
        base_actions = refined_actions  # Use refined fine actions as base

        additional_outputs = {}

        if plan_sequence:
            # Plan action sequence
            action_sequence, completion_probs = self.action_planner(fused_features)
            additional_outputs['action_sequence'] = action_sequence
            additional_outputs['completion_probs'] = completion_probs

        if use_feedback and feedback_features is not None:
            # Integrate feedback
            feedback_refined, adjustment = self.feedback_integrator(
                language_features, feedback_features, base_actions
            )
            base_actions = feedback_refined
            additional_outputs['feedback_adjustment'] = adjustment

        if adapt_action and previous_action is not None and execution_error is not None:
            # Adapt based on past performance
            adapted_actions = self.adaptive_generator(
                language_features, previous_action, execution_error
            )
            base_actions = adapted_actions
            additional_outputs['adapted'] = True

        # Generate safe actions
        safe_actions = self.safe_generator(fused_features, enforce_constraints=True, smooth_actions=True)

        # Return the most refined action
        final_actions = safe_actions  # Use safe actions as final output

        return final_actions, additional_outputs

def main():
    # Create complete action generation system
    action_system = CompleteActionGenerationSystem()

    # Create dummy inputs
    batch_size = 2
    visual_features = torch.randn(batch_size, 512)
    language_features = torch.randn(batch_size, 512)
    proprioceptive_features = torch.randn(batch_size, 128)
    feedback_features = torch.randn(batch_size, 128)
    previous_action = torch.randn(batch_size, 6)
    execution_error = torch.randn(batch_size, 6)

    # Generate actions with all features
    actions, outputs = action_system(
        visual_features, language_features, proprioceptive_features,
        feedback_features=feedback_features,
        previous_action=previous_action,
        execution_error=execution_error,
        plan_sequence=True,
        use_feedback=True,
        adapt_action=True
    )

    print(f"Input shapes:")
    print(f"  Visual: {visual_features.shape}")
    print(f"  Language: {language_features.shape}")
    print(f"  Proprioceptive: {proprioceptive_features.shape}")

    print(f"\nOutput shapes:")
    print(f"  Actions: {actions.shape}")

    print(f"\nAdditional outputs:")
    for key, value in outputs.items():
        if isinstance(value, torch.Tensor):
            print(f"  {key}: {value.shape}")
        else:
            print(f"  {key}: {value}")

    print(f"\nSample actions: {actions[0].detach().numpy()}")
    print(f"Action range: [{actions.min():.3f}, {actions.max():.3f}]")

if __name__ == "__main__":
    main()
```

## Performance and Safety Considerations

### Efficient Action Generation

```python
#!/usr/bin/env python3
# efficient_action_generation.py
# Efficient implementation for action generation

import torch
import torch.nn as nn

class EfficientActionGenerator(nn.Module):
    """Efficient implementation of action generation"""

    def __init__(self, input_dim=512, action_dim=6):
        super().__init__()

        # Lightweight network for efficiency
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, action_dim)
        )

        # Lightweight normalization
        self.normalizer = nn.Tanh()

    def forward(self, features):
        """Efficient forward pass"""
        actions = self.network(features)
        normalized_actions = self.normalizer(actions)
        return normalized_actions

def main():
    print("Efficient Action Generation Implementation")

    # Create efficient action generator
    efficient_generator = EfficientActionGenerator(input_dim=512, action_dim=6)

    # Test with dummy input
    dummy_input = torch.randn(1, 512)
    actions = efficient_generator(dummy_input)

    print(f"Efficient action generator output shape: {actions.shape}")
    print(f"Sample actions: {actions[0].detach().numpy()}")

if __name__ == "__main__":
    main()
```

## Troubleshooting Action Generation Issues

### Common Issues and Solutions

1. **Action Space Mismatch**:
   - Ensure action dimensions match robot capabilities
   - Use proper normalization between networks
   - Validate action ranges before execution

2. **Safety Violations**:
   - Implement comprehensive constraint checking
   - Use safety-rated controllers for execution
   - Test extensively in simulation before real hardware

3. **Sequence Planning Issues**:
   - Break complex tasks into smaller subtasks
   - Use hierarchical planning approaches
   - Implement recovery mechanisms for failed steps

4. **Feedback Integration Problems**:
   - Ensure timely feedback processing
   - Use appropriate feedback weighting
   - Implement stability checks

## Summary

In this lesson, you learned:
- How to represent and generate actions in VLA models
- Techniques for multimodal feature fusion for action generation
- Methods for enforcing safety constraints and feasibility
- Sequential planning approaches for complex tasks
- Feedback integration for closed-loop execution
- Efficient implementation strategies

Action generation is the critical final step in VLA models that translates perception and understanding into physical behavior, requiring careful consideration of safety, feasibility, and execution constraints.

## References

- [Action Generation in Robotics](https://arxiv.org/abs/2209.09860)
- [Safe Reinforcement Learning for Robotics](https://arxiv.org/abs/2005.08815)
- [Hierarchical Action Planning](https://arxiv.org/abs/2105.14074)

## Author Information

<div className="author-info">
  <h3>Author: Aamir Ahmed Shamsi</h3>
  <p><strong>GIAIC ID:</strong> 00486031</p>
  <p>This lesson was created with assistance from Claude AI.</p>
</div>