import React from 'react';
import Link from '@docusaurus/Link';
import { Brain, Network, Layers } from 'lucide-react';
import { CHAPTERS, type ChapterCard } from './data/chapters';
import styles from './JourneySection.module.css';

const iconMap: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Brain,
  Network,
  Layers,
};

interface JourneySectionProps {
  chapters?: ChapterCard[];
}

export function JourneySection({ chapters = CHAPTERS }: JourneySectionProps) {
  return (
    <section className={`landing-section ${styles.journey}`}>
      <div className="landing-container">
        <h2 className="landing-headline">Your Journey</h2>
        <p className="landing-subheadline">From Zero to Building Robots That Think</p>
        <p className="landing-supporting-text">
          Each step brings you closer to creating machines that move, sense, and understand
        </p>

        <div className={styles.cardsGrid}>
          {chapters.map((chapter) => {
            const IconComponent = chapter.icon ? iconMap[chapter.icon] : null;

            return (
              <Link
                key={chapter.id}
                to={chapter.href}
                className={styles.card}
                aria-label={`Go to ${chapter.title}`}
              >
                <article>
                  <div className={styles.cardHeader}>
                    {IconComponent && (
                      <div className={styles.iconWrapper}>
                        <IconComponent size={28} className={styles.icon} />
                      </div>
                    )}
                    <span className={styles.chapterNumber}>{chapter.number}</span>
                  </div>
                  <h3 className={styles.cardTitle}>{chapter.title}</h3>
                  <p className={styles.cardDescription}>{chapter.description}</p>
                  <span className={styles.cardArrow}>→</span>
                </article>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default JourneySection;
