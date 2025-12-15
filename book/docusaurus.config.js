// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide by Aamir Ahmed Shamsi with Claude AI',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://reckonfx.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/hackathon-1-Physical_AI_book/',

  // GitHub pages deployment config.
  organizationName: 'reckonfx',
  projectName: 'hackathon-1-Physical_AI_book',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/aamirahmedshamsi/physical-ai-book/edit/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'ros2Sidebar',
            position: 'left',
            label: 'Module 1 - ROS2',
          },
          {
            type: 'docSidebar',
            sidebarId: 'gazeboSidebar',
            position: 'left',
            label: 'Module 2 - Gazebo',
          },
          {
            type: 'docSidebar',
            sidebarId: 'isaacSidebar',
            position: 'left',
            label: 'Module 3 - Isaac',
          },
          {
            type: 'docSidebar',
            sidebarId: 'vlaSidebar',
            position: 'left',
            label: 'Module 4 - VLA',
          },
          {
            href: 'https://github.com/aamirahmedshamsi/physical-ai-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'ROS2 Fundamentals',
                to: '/docs/ros2-fundamentals/intro',
              },
              {
                label: 'Gazebo & Unity Simulation',
                to: '/docs/gazebo-unity-sim/intro',
              },
              {
                label: 'AI-Robot Brain (Isaac)',
                to: '/docs/isaac-ai-brain/intro',
              },
              {
                label: 'VLA Models',
                to: '/docs/vla-models/intro',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/aamirahmedshamsi/physical-ai-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Aamir Ahmed Shamsi (GIAIC ID: 00486031). Built with Claude AI assistance.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;