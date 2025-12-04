import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Course Introduction - Coming Soon 🚀
          </Link>
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
        <div className="container">
            <div style={{textAlign: 'center', padding: '4rem 0'}}>
                <h2>🚧 Under Construction 🚧</h2>
                <p>We are building the comprehensive guide to the future of robotics.</p>
            </div>
        </div>
      </main>
    </Layout>
  );
}
