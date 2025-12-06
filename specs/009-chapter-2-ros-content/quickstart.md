# Quickstart: Chapter 2 Interactive Components

This document provides integration scenarios for the new interactive components being developed for Chapter 2.

## Component: `<RosTerminal />`

### Scenario 1: Basic Usage

This component can be embedded directly into any MDX file.

```jsx
import RosTerminal from '@site/src/components/RosTerminal';

<RosTerminal />
```

### Scenario 2: Pre-defining supported commands

The component will have a default set of commands, but can be configured with a specific set for a given context.

```jsx
import RosTerminal from '@site/src/components/RosTerminal';

const supportedCommands = {
  "ros2 node list": {
    output: "/camera\n/perception\n/planner"
  },
  "ros2 topic list": {
    output: "/camera/image_raw\n/odometry\n/cmd_vel"
  }
};

<RosTerminal commands={supportedCommands} />
```

## Component: `<ConceptCard />`

### Scenario 1: Basic Usage

This component will take two children, the "conceptual" view and the "technical" view.

```jsx
import ConceptCard from '@site/src/components/ConceptCard';

<ConceptCard>
  <div name="Conceptual">
    <!-- Conceptual Diagram (e.g., img, text) -->
    <img src="/img/conceptual-diagram.png" alt="Conceptual Diagram" />
  </div>
  <div name="Technical">
    <!-- Technical Diagram (e.g., Mermaid, code block) -->
    <Mermaid>
      {`
        graph TD
          A[Client] -->|TCP| B(Server)
      `}
    </Mermaid>
  </div>
</ConceptCard>
```

