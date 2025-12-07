import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import { RagChat } from '../components/RagChat';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroContainer}>
        {/* Left Column: Text */}
        <div className={styles.heroText}>
          <Heading as="h1" className={styles.heroTitle}>
            {siteConfig.title}
          </Heading>
          <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={styles.primaryBtn}
              to="/docs/preface">
              GET STARTED
            </Link>
            <Link
              className={styles.secondaryBtn}
              to="https://github.com/codeWithHak/physical-ai-and-humanoid-robotics-textbook">
              GITHUB
            </Link>
          </div>
        </div>

        {/* Right Column: Visual */}
        <div className={styles.heroVisual}>
          <div className={styles.glowContainer}>
            <img 
              src="img/undraw_docusaurus_mountain.svg" 
              alt="RoboLearn Schematic" 
              className={styles.diagramImage}
            />
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="The open-source textbook for Physical AI and Humanoid Robotics.">
      <HomepageHeader />
      <main>
        {/* Main content area - currently empty per "Clean Slate" requirement */}
      </main>
      <RagChat />
    </Layout>
  );
}