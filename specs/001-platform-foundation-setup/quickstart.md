# Quickstart: Platform Foundation Setup

## Prerequisites

- Node.js 20+ (LTS)
- git
- npm

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/codeWithHak/physical-ai-and-humanoid-robotics-textbook.git
   cd physical-ai-and-humanoid-robotics-textbook/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Local Development

Start the development server:

```bash
npm start
```

The site will be available at `http://localhost:3000`.

## Deployment

Deployments are automated via GitHub Actions.

1. Push changes to `main` branch.
2. GitHub Action `deploy` workflow triggers.
3. Site updates at `https://codeWithHak.github.io/physical-ai-and-humanoid-robotics-textbook/`.

## Project Structure

- `docusaurus.config.ts`: Site configuration.
- `src/pages/index.tsx`: Landing page component.
- `docs/`: Markdown content files.
- `static/`: Public assets.