import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/physical-ai-book/docs',
    component: ComponentCreator('/physical-ai-book/docs', '12c'),
    routes: [
      {
        path: '/physical-ai-book/docs',
        component: ComponentCreator('/physical-ai-book/docs', 'cc1'),
        routes: [
          {
            path: '/physical-ai-book/docs',
            component: ComponentCreator('/physical-ai-book/docs', '9be'),
            routes: [
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/cross-platform-simulation-workflows',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/cross-platform-simulation-workflows', 'e64'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/gazebo-physics-and-sensors',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/gazebo-physics-and-sensors', '90d'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/gazebo-robot-modeling',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/gazebo-robot-modeling', '643'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/intro',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/intro', 'a57'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/simulation-conclusion',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/simulation-conclusion', 'f64'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/simulation-optimization',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/simulation-optimization', 'd82'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/gazebo-unity-sim/unity-robotics-hub-integration',
                component: ComponentCreator('/physical-ai-book/docs/gazebo-unity-sim/unity-robotics-hub-integration', '6ed'),
                exact: true,
                sidebar: "gazeboSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/conclusion-and-next-steps',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/conclusion-and-next-steps', '0e9'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/interactive-tutorials',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/interactive-tutorials', '1bd'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/intro',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/intro', '530'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/isaac-ros-integration',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/isaac-ros-integration', '9b0'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/isaac-sim-fundamentals',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/isaac-sim-fundamentals', 'b27'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/nav2-navigation-stack',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/nav2-navigation-stack', 'f19'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/synthetic-data-generation',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/synthetic-data-generation', '5ee'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/isaac-ai-brain/vslam-implementation',
                component: ComponentCreator('/physical-ai-book/docs/isaac-ai-brain/vslam-implementation', '880'),
                exact: true,
                sidebar: "isaacSidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/intro',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/intro', '785'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-conclusion',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-conclusion', '1fc'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-launch-systems',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-launch-systems', 'a58'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-nodes-and-topics',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-nodes-and-topics', 'e4a'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-packages-and-workspaces',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-packages-and-workspaces', '068'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-parameters-and-composition',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-parameters-and-composition', '73c'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/ros2-fundamentals/ros2-services-and-actions',
                component: ComponentCreator('/physical-ai-book/docs/ros2-fundamentals/ros2-services-and-actions', 'f43'),
                exact: true,
                sidebar: "ros2Sidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/action-generation-and-execution',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/action-generation-and-execution', 'f1c'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/intro',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/intro', 'ba3'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/language-grounding-in-robotics',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/language-grounding-in-robotics', '48c'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/perception-and-understanding',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/perception-and-understanding', '606'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/vla-conclusion-and-future-directions',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/vla-conclusion-and-future-directions', 'a3c'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/vla-integration-with-robot-platforms',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/vla-integration-with-robot-platforms', 'aba'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/vla-models-overview',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/vla-models-overview', '992'),
                exact: true,
                sidebar: "vlaSidebar"
              },
              {
                path: '/physical-ai-book/docs/vla-models/vla-training-workflows',
                component: ComponentCreator('/physical-ai-book/docs/vla-models/vla-training-workflows', '7e8'),
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
    path: '/physical-ai-book/',
    component: ComponentCreator('/physical-ai-book/', 'f23'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
