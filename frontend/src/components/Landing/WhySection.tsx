import React from 'react';
import styles from './WhySection.module.css';

export function WhySection() {
  return (
    <section className={`landing-section landing-section--alt ${styles.why}`}>
      <div className="landing-container">
        <h2 className="landing-headline">Why This Matters</h2>
        <p className="landing-subheadline">Build Machines That Free Up Your Time</p>
        <p className="landing-supporting-text">
          Robots that handle physical tasks while you focus on what matters most
        </p>

        <div className={styles.content}>
          <div className={styles.valueProps}>
            <div className={styles.valueProp}>
              <div className={styles.valuePropIcon}>🤖</div>
              <h3 className={styles.valuePropTitle}>Physical Intelligence</h3>
              <p className={styles.valuePropText}>
                Move beyond chatbots to robots that interact with the real world
              </p>
            </div>
            <div className={styles.valueProp}>
              <div className={styles.valuePropIcon}>⚡</div>
              <h3 className={styles.valuePropTitle}>Practical Skills</h3>
              <p className={styles.valuePropText}>
                Learn ROS 2, simulation, and deployment with hands-on projects
              </p>
            </div>
            <div className={styles.valueProp}>
              <div className={styles.valuePropIcon}>🚀</div>
              <h3 className={styles.valuePropTitle}>Future-Ready</h3>
              <p className={styles.valuePropText}>
                Position yourself at the forefront of the robotics revolution
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default WhySection;
