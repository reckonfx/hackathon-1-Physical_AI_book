import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';


function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary')}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div>
          <Link
            className="button button--secondary button--lg"
            to="/docs/ros2-fundamentals/intro">
            Start Learning - Module 1: ROS2 Fundamentals
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A Comprehensive Guide to Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section>
          <div className="container">
            <div className="row">
              <div className="col col--4 padding-horiz--md">
                <h2>Module 1: ROS2 Fundamentals</h2>
                <p>Learn the fundamentals of Robot Operating System 2 (ROS2), including nodes, topics, services, actions, and launch systems.</p>
                <Link to="/docs/ros2-fundamentals/intro" className="button button--primary">
                  Go to Module 1
                </Link>
              </div>
              <div className="col col--4 padding-horiz--md">
                <h2>Module 2: Gazebo & Unity Simulation</h2>
                <p>Master physics simulation with Gazebo and Unity Robotics Hub integration for creating realistic robotic environments.</p>
                <Link to="/docs/gazebo-unity-sim/intro" className="button button--primary">
                  Go to Module 2
                </Link>
              </div>
              <div className="col col--4 padding-horiz--md">
                <h2>Module 3: The AI-Robot Brain (NVIDIA Isaac™)</h2>
                <p>Explore NVIDIA Isaac Sim and Isaac ROS integration for advanced robotic perception and navigation.</p>
                <Link to="/docs/isaac-ai-brain/intro" className="button button--primary">
                  Go to Module 3
                </Link>
              </div>
            </div>
            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--6 offset-3 padding-horiz--md">
                <h2>Module 4: Vision-Language-Action (VLA) Models</h2>
                <p>Discover Vision-Language-Action models for multimodal AI systems that integrate perception, understanding, and action.</p>
                <Link to="/docs/vla-models/intro" className="button button--primary">
                  Go to Module 4
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}