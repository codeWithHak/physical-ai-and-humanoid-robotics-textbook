export interface HardwareTier {
  id: number;
  name: string;
  label: string;
  benefit: string;
  requirements: string;
  note?: string;
  cost: string;
  isRecommended: boolean;
}

export const HARDWARE_TIERS: HardwareTier[] = [
  {
    id: 1,
    name: "Workstation",
    label: "Full Local Setup",
    benefit: "Best Experience",
    requirements: "RTX 4070 Ti+, 64GB RAM, Ubuntu 22.04",
    note: "Run Isaac Sim locally with full performance",
    cost: "~$2,500+ hardware",
    isRecommended: false
  },
  {
    id: 2,
    name: "Cloud + Edge",
    label: "Hybrid Approach",
    benefit: "Flexible",
    requirements: "AWS/Azure GPU instances for simulation, Jetson kit for physical deployment",
    cost: "~$200/quarter cloud + $700 Jetson",
    isRecommended: true
  },
  {
    id: 3,
    name: "Simulation Only",
    label: "Learning Focus",
    benefit: "Lowest Cost",
    requirements: "Cloud-based simulation without physical hardware",
    note: "Complete the theory and simulation modules",
    cost: "Cloud compute only",
    isRecommended: false
  }
];
