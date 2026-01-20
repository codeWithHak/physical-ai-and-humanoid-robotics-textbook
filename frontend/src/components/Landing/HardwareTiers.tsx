import React from 'react';
import { Monitor, Cloud, Play } from 'lucide-react';
import { HARDWARE_TIERS, type HardwareTier } from './data/tiers';
import styles from './HardwareTiers.module.css';

const tierIcons: Record<number, React.ComponentType<{ size?: number; className?: string }>> = {
  1: Monitor,
  2: Cloud,
  3: Play,
};

interface HardwareTiersProps {
  tiers?: HardwareTier[];
}

export function HardwareTiers({ tiers = HARDWARE_TIERS }: HardwareTiersProps) {
  return (
    <section className={`landing-section ${styles.hardware}`}>
      <div className="landing-container">
        <h2 className="landing-headline">Start Where You Are</h2>
        <p className="landing-subheadline">No Expensive Hardware Required</p>
        <p className="landing-supporting-text">
          Begin building today with just your browser. Scale up when you're ready.
        </p>

        <div className={styles.tiersGrid}>
          {tiers.map((tier) => {
            const IconComponent = tierIcons[tier.id];

            return (
              <article
                key={tier.id}
                className={`${styles.tierCard} ${tier.isRecommended ? styles.recommended : ''}`}
                aria-label={`${tier.name} tier: ${tier.label}`}
              >
                {tier.isRecommended && (
                  <div className={styles.recommendedBadge}>RECOMMENDED</div>
                )}

                <div className={styles.tierHeader}>
                  <div className={styles.tierNumber}>{tier.id}</div>
                  {IconComponent && (
                    <IconComponent size={24} className={styles.tierIcon} />
                  )}
                </div>

                <h3 className={styles.tierName}>{tier.name}</h3>
                <p className={styles.tierLabel}>{tier.label}</p>
                <p className={styles.tierBenefit}>{tier.benefit}</p>

                <div className={styles.tierDetails}>
                  <p className={styles.tierRequirements}>{tier.requirements}</p>
                  {tier.note && (
                    <p className={styles.tierNote}>{tier.note}</p>
                  )}
                </div>

                <div className={styles.tierCost}>
                  <span className={styles.costLabel}>Cost:</span>
                  <span className={styles.costValue}>{tier.cost}</span>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default HardwareTiers;
