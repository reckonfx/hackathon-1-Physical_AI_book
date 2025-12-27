import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug', '1e1'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/config',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/config', 'f94'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/content',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/content', 'efb'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/globalData',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/globalData', '8ae'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/metadata',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/metadata', 'c6a'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/registry',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/registry', '02c'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/__docusaurus/debug/routes',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/__docusaurus/debug/routes', '083'),
    exact: true
  },
  {
    path: '/hackathon-1-Physical_AI_book/docs',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/docs', '71d'),
    routes: [
      {
        path: '/hackathon-1-Physical_AI_book/docs',
        component: ComponentCreator('/hackathon-1-Physical_AI_book/docs', '9c1'),
        routes: [
          {
            path: '/hackathon-1-Physical_AI_book/docs',
            component: ComponentCreator('/hackathon-1-Physical_AI_book/docs', '5e5'),
            routes: [
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/cross-platform-simulation-workflows',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/cross-platform-simulation-workflows', '51c'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/gazebo-physics-and-sensors',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/gazebo-physics-and-sensors', '14c'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/gazebo-robot-modeling',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/gazebo-robot-modeling', 'ada'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/intro',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/intro', '721'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/simulation-conclusion',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/simulation-conclusion', '5df'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/simulation-optimization',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/simulation-optimization', '975'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/unity-robotics-hub-integration',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/gazebo-unity-sim/unity-robotics-hub-integration', 'cd8'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/conclusion-and-next-steps',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/conclusion-and-next-steps', '054'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/interactive-tutorials',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/interactive-tutorials', '8a0'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/intro',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/intro', 'a03'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/isaac-ros-integration',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/isaac-ros-integration', 'e9c'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/isaac-sim-fundamentals',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/isaac-sim-fundamentals', 'ef0'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/nav2-navigation-stack',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/nav2-navigation-stack', '1bd'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/synthetic-data-generation',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/synthetic-data-generation', '8ea'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/vslam-implementation',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/isaac-ai-brain/vslam-implementation', 'cce'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/intro',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/intro', '85c'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-conclusion',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-conclusion', '84f'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-launch-systems',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-launch-systems', '19c'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-nodes-and-topics',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-nodes-and-topics', 'e6e'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-packages-and-workspaces',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-packages-and-workspaces', '85b'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-parameters-and-composition',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-parameters-and-composition', '2c2'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-services-and-actions',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/ros2-fundamentals/ros2-services-and-actions', '4b3'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/action-generation-and-execution',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/action-generation-and-execution', 'd08'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/intro',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/intro', '273'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/language-grounding-in-robotics',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/language-grounding-in-robotics', '975'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/perception-and-understanding',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/perception-and-understanding', '597'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/vla-conclusion-and-future-directions',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/vla-conclusion-and-future-directions', '28f'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/vla-integration-with-robot-platforms',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/vla-integration-with-robot-platforms', 'e3a'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/vla-models-overview',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/vla-models-overview', '2be'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/hackathon-1-Physical_AI_book/docs/vla-models/vla-training-workflows',
                component: ComponentCreator('/hackathon-1-Physical_AI_book/docs/vla-models/vla-training-workflows', '1b9'),
                exact: true,
                sidebar: "vlaSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/hackathon-1-Physical_AI_book/',
    component: ComponentCreator('/hackathon-1-Physical_AI_book/', '598'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
