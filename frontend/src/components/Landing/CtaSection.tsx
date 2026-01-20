import React from 'react';
import Link from '@docusaurus/Link';
import { Bot } from 'lucide-react';
import styles from './CtaSection.module.css';

interface CtaSectionProps {
  href?: string;
}

export function CtaSection({ href = '/docs/preface' }: CtaSectionProps) {
  return (
    <section className={`landing-section landing-section--alt ${styles.cta}`}>
      <div className="landing-container">
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaHeadline}>Ready to Begin?</h2>
          <p className={styles.ctaSubheadline}>The Future is Physical AI</p>
          <p className={styles.ctaTagline}>Robots That Think, Move, and Collaborate</p>
          <p className={styles.ctaSupportingText}>
            Join the transition from AI confined to screens to AI that shapes the physical world alongside us.
          </p>

          <div className={styles.ctaBox}>
            <div className={styles.ctaBoxIcon}>
              <Bot size={40} />
            </div>
            <div className={styles.ctaBoxContent}>
              <h3 className={styles.ctaBoxTitle}>Start Your Physical AI Journey</h3>
              <p className={styles.ctaBoxSubtext}>
                From ROS 2 basics to autonomous humanoids with voice control
              </p>
            </div>
            <Link
              to={href}
              className={styles.ctaButton}
              aria-label="Get Started Free - Navigate to Preface"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default CtaSection;
