import React, { useState } from 'react';
import styles from './styles.module.css';

export default function ConceptCard({ children }) {
  const [isTechnical, setIsTechnical] = useState(false);

  const conceptualView = React.Children.toArray(children).find(
    (child) => child.props.name === 'Conceptual'
  );
  const technicalView = React.Children.toArray(children).find(
    (child) => child.props.name === 'Technical'
  );

  return (
    <div className={styles.conceptCard}>
      <div className={styles.toggleContainer}>
        <button
          className={`${styles.toggleButton} ${!isTechnical ? styles.active : ''}`}
          onClick={() => setIsTechnical(false)}
        >
          Conceptual
        </button>
        <button
          className={`${styles.toggleButton} ${isTechnical ? styles.active : ''}`}
          onClick={() => setIsTechnical(true)}
        >
          Technical
        </button>
      </div>
      <div className={styles.content}>
        {isTechnical ? technicalView : conceptualView}
      </div>
    </div>
  );
}