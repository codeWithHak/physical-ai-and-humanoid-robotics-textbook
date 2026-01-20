export interface ChapterCard {
  id: number;
  number: string;
  title: string;
  description: string;
  href: string;
  icon?: string;
}

export const CHAPTERS: ChapterCard[] = [
  {
    id: 1,
    number: "Chapter 1",
    title: "Embodied Intelligence",
    description: "The Great Transition from digital AI to physical machines that move, sense, and act.",
    href: "/docs/chapter-01-foundations/great-transition",
    icon: "Brain"
  },
  {
    id: 2,
    number: "Chapter 2",
    title: "Robotic Nervous System",
    description: "Master ROS 2 - the middleware that connects sensors, actuators, and AI planners.",
    href: "/docs/chapter-02-robotic-nervous-system/why-middleware",
    icon: "Network"
  },
  {
    id: 3,
    number: "Chapter 3",
    title: "Digital Twin",
    description: "Build virtual robots in simulation before deploying to the physical world.",
    href: "/docs/chapter-03-digital-twin/mirror-world",
    icon: "Layers"
  }
];
