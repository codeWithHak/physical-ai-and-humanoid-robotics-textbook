import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import { JourneySection } from '../components/Landing/JourneySection';
import { WhySection } from '../components/Landing/WhySection';
import { HardwareTiers } from '../components/Landing/HardwareTiers';
import { CtaSection } from '../components/Landing/CtaSection';

import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroContainer}>
        {/* Left Column: Text */}
        <div className={styles.heroText}>
          <Heading as="h1" className={styles.heroTitle}>
            Learn to Build{' '}
            <span className={styles.highlight}>Intelligent Humanoid Robots</span>
          </Heading>
          <p className={styles.heroDescription}>
            PhysAI is the open-source textbook for Physical AI and Humanoid Robotics.
            Master the complete stack—from ROS 2 and simulation to vision-language models
            and real-world deployment.
          </p>
          <div className={styles.buttons}>
            <Link
              className={styles.primaryBtn}
              to="/docs/preface">
              START LEARNING
            </Link>
            <Link
              className={styles.secondaryBtn}
              to="https://github.com/codeWithHak/physai">
              VIEW ON GITHUB
            </Link>
          </div>
        </div>

        {/* Right Column: Visual */}
        <div className={styles.heroVisual}>
          <div className={styles.glowContainer}>
            <picture>
              <source
                srcSet="img/hero-banner.webp"
                type="image/webp"
              />
              <img
                src="img/hero-banner.png"
                alt="PhysAI Hero - Intelligent Humanoid Robot"
                className={styles.diagramImage}
                width={1600}
                height={1073}
                loading="eager"
              />
            </picture>
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
        <JourneySection />
        <WhySection />
        <HardwareTiers />
        <CtaSection />
      </main>
    </Layout>
  );
}
