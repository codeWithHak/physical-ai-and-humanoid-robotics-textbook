import React, { useState } from 'react';
import styles from './styles.module.css';

const urdfSnippet = `<robot name="arm">
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </visual>
  </link>

  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>
  </joint>

  <link name="upper_arm">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.5"/>
      </geometry>
    </visual>
  </link>
</robot>`;

export default function UrdfExplorer() {
  const [highlightedElement, setHighlightedElement] = useState<string | null>(null);

  const handleMouseEnter = (elementName: string) => {
    setHighlightedElement(elementName);
  };

  const handleMouseLeave = () => {
    setHighlightedElement(null);
  };

  // Helper to create interactive code lines
  const CodeLine = ({ content, elementName, type }: { content: string, elementName?: string, type?: 'link' | 'joint' }) => {
    if (!elementName) {
      return <div className={styles.codeLine}>{content}</div>;
    }
    
    return (
      <div 
        className={`${styles.codeLine} ${styles.interactive} ${highlightedElement === elementName ? styles.active : ''}`}
        onMouseEnter={() => handleMouseEnter(elementName)}
        onMouseLeave={handleMouseLeave}
      >
        {content}
      </div>
    );
  };

  return (
    <div className={styles.container}>
      <div className={styles.codePanel}>
        <pre className={styles.codeBlock}>
          <code>
            <div className={styles.codeLine}>&lt;robot name="arm"&gt;</div>
            <CodeLine content='  &lt;link name="base_link"&gt;' elementName="base_link" type="link" />
            <div className={styles.codeLine}>    &lt;visual&gt;</div>
            <div className={styles.codeLine}>      &lt;geometry&gt;</div>
            <div className={styles.codeLine}>        &lt;cylinder length="0.6" radius="0.2"/&gt;</div>
            <div className={styles.codeLine}>      &lt;/geometry&gt;</div>
            <div className={styles.codeLine}>    &lt;/visual&gt;</div>
            <div className={styles.codeLine}>  &lt;/link&gt;</div>
            <div className={styles.codeLine}> </div>
            <CodeLine content='  &lt;joint name="shoulder_joint" type="revolute"&gt;' elementName="shoulder_joint" type="joint" />
            <div className={styles.codeLine}>    &lt;parent link="base_link"/&gt;</div>
            <div className={styles.codeLine}>    &lt;child link="upper_arm"/&gt;</div>
            <div className={styles.codeLine}>  &lt;/joint&gt;</div>
            <div className={styles.codeLine}> </div>
            <CodeLine content='  &lt;link name="upper_arm"&gt;' elementName="upper_arm" type="link" />
            <div className={styles.codeLine}>    &lt;visual&gt;</div>
            <div className={styles.codeLine}>      &lt;geometry&gt;</div>
            <div className={styles.codeLine}>        &lt;box size="0.1 0.1 0.5"/&gt;</div>
            <div className={styles.codeLine}>      &lt;/geometry&gt;</div>
            <div className={styles.codeLine}>    &lt;/visual&gt;</div>
            <div className={styles.codeLine}>  &lt;/link&gt;</div>
            <div className={styles.codeLine}>&lt;/robot&gt;</div>
          </code>
        </pre>
      </div>
      <div className={styles.visualPanel}>
        <svg viewBox="0 0 200 300" className={styles.robotSvg}>
          {/* Base Link */}
          <rect 
            x="70" y="220" width="60" height="60" 
            className={`${styles.svgElement} ${highlightedElement === 'base_link' ? styles.activeSvg : ''}`}
          />
          <text x="100" y="255" textAnchor="middle" className={styles.label}>Base</text>

          {/* Shoulder Joint */}
          <circle 
            cx="100" y="220" r="10" 
            className={`${styles.svgElement} ${highlightedElement === 'shoulder_joint' ? styles.activeSvg : ''}`}
          />
          
          {/* Upper Arm */}
          <rect 
            x="80" y="120" width="40" height="90" 
            className={`${styles.svgElement} ${highlightedElement === 'upper_arm' ? styles.activeSvg : ''}`}
          />
          <text x="100" y="165" textAnchor="middle" className={styles.label}>Upper Arm</text>
        </svg>
      </div>
    </div>
  );
}