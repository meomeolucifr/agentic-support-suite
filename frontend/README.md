# Frontend Dashboard

## Purpose

Next.js admin dashboard for monitoring tickets, agent status, analytics, and managing the support system.

## Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app router
│   │   ├── page.tsx      # Dashboard home
│   │   ├── tickets/      # Ticket management
│   │   ├── analytics/    # Analytics dashboard
│   │   └── agents/       # Agent monitoring
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   └── styles/           # Styling
├── package.json
└── next.config.js
```

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts or Chart.js
- **State**: React Query / SWR
- **HTTP Client**: fetch or axios

## Key Components

### Dashboard Home
- Overview metrics
- Recent tickets
- Agent status
- Quick actions

### Ticket Management
- Ticket list with filters
- Ticket detail view
- Status updates
- Agent assignment

### Analytics
- Ticket volume trends
- Resolution rates
- Agent performance
- Customer satisfaction metrics

### Agent Monitoring
- Agent health status
- Processing times
- Error rates
- Performance metrics

## Usage Examples

### Development

```bash
cd frontend
npm install
npm run dev
```

### Production Build

```bash
npm run build
npm start
```

## Configuration

- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_ORCHESTRATOR_URL` - Orchestrator service URL

## Features

- Real-time ticket updates
- Agent status monitoring
- Analytics and reporting
- Responsive design
- Dark mode support (optional)



