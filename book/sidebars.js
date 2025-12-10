// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  ros2Sidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS2 Fundamentals',
      items: [
        'ros2-fundamentals/intro',
        'ros2-fundamentals/ros2-nodes-and-topics',
        'ros2-fundamentals/ros2-services-and-actions',
        'ros2-fundamentals/ros2-launch-systems',
        'ros2-fundamentals/ros2-packages-and-workspaces',
        'ros2-fundamentals/ros2-parameters-and-composition',
        'ros2-fundamentals/ros2-conclusion'
      ],
    },
  ],

  gazeboSidebar: [
    {
      type: 'category',
      label: 'Module 2: Gazebo & Unity Simulation',
      items: [
        'gazebo-unity-sim/intro',
        'gazebo-unity-sim/gazebo-robot-modeling',
        'gazebo-unity-sim/gazebo-physics-and-sensors',
        'gazebo-unity-sim/unity-robotics-hub-integration',
        'gazebo-unity-sim/cross-platform-simulation-workflows',
        'gazebo-unity-sim/simulation-optimization',
        'gazebo-unity-sim/simulation-conclusion'
      ],
    },
  ],

  isaacSidebar: [
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'isaac-ai-brain/intro',
        'isaac-ai-brain/isaac-sim-fundamentals',
        'isaac-ai-brain/isaac-ros-integration',
        'isaac-ai-brain/vslam-implementation',
        'isaac-ai-brain/nav2-navigation-stack',
        'isaac-ai-brain/synthetic-data-generation',
        'isaac-ai-brain/interactive-tutorials',
        'isaac-ai-brain/conclusion-and-next-steps'
      ],
    },
  ],

  vlaSidebar: [
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) Models',
      items: [
        'vla-models/intro',
        'vla-models/vla-models-overview',
        'vla-models/perception-and-understanding',
        'vla-models/language-grounding-in-robotics',
        'vla-models/action-generation-and-execution',
        'vla-models/vla-training-workflows',
        'vla-models/vla-integration-with-robot-platforms',
        'vla-models/vla-conclusion-and-future-directions'
      ],
    },
  ],
};

module.exports = sidebars;