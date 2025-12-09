import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '1a2'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '9f5'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '58f'),
            routes: [
              {
                path: '/docs/module-4-vla/comprehensive-exercises',
                component: ComponentCreator('/docs/module-4-vla/comprehensive-exercises', 'c16'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/cross-references',
                component: ComponentCreator('/docs/module-4-vla/cross-references', 'efe'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/glossary',
                component: ComponentCreator('/docs/module-4-vla/glossary', '402'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/lesson-1-vla-fundamentals',
                component: ComponentCreator('/docs/module-4-vla/lesson-1-vla-fundamentals', '065'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/lesson-2-vla-capstone',
                component: ComponentCreator('/docs/module-4-vla/lesson-2-vla-capstone', '24c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/worked-examples',
                component: ComponentCreator('/docs/module-4-vla/worked-examples', '4bc'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
