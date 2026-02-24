# Aura Camera App

A full-stack application that captures and analyzes aura energy using advanced biofeedback technology. Built with Next.js, TypeScript, Python, and FastAPI.

![Aura Camera](https://img.shields.io/badge/Aura-Camera-purple)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)

## Features

- **Camera Capture**: Real-time face detection and photo capture
- **Biofeedback Analysis**: Simulated biofeedback sensors for energy reading
- **Aura Generation**: AI-powered aura color profile and image generation
- **Personalized Readings**: Detailed interpretations of aura colors and meanings
- **Session Management**: Track and save aura sessions
- **Subscription System**: Free tier with upgrade options
- **Social Sharing**: Share aura photos and readings

## System Architecture

```mermaid
graph TD
    User([User]) <--> Frontend[Next.js Frontend]
    Frontend <--> API[FastAPI Backend]
    API <--> ML[AI/ML Processing Layer]
    API <--> DB[(PostgreSQL)]
    API <--> Redis[(Redis Cache)]
    ML <--> FaceDetect[MediaPipe Face Mesh]
    ML <--> BioSim[Biofeedback Simulator]
    ML <--> AuraGen[Aura Generation Engine]
    API <--> Cloudinary[Cloudinary Image Storage]
```

### Aura Zones

The application analyzes energy in specific zones around the subject:

- **Coronation**: Top of head energy (Crown)
- **Ascendant**: Right side (Receiving energy)
- **Descendant**: Left side (Giving energy)
- **Cathedra**: Bottom/base energy (Base/Root)
- **Etherea**: Surrounding vibrational field

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Accessible UI components
- **Zustand** - State management
- **Framer Motion** - Animations
- **MediaPipe** - Face detection

### Backend
- **FastAPI** - High-performance Python API
- **OpenCV** - Computer vision
- **MediaPipe** - Face mesh detection
- **Pillow** - Image processing
- **OpenAI** - Reading generation (optional)

### Database & Storage
- **PostgreSQL** - Primary database
- **Prisma** - ORM
- **Redis** - Caching
- **Cloudinary** - Image storage

### Payment
- **Stripe** - Subscription management

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aura-camera-app.git
   cd aura-camera-app
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your values
   ```

4. **Set up database**
   ```bash
   npx prisma migrate dev
   npx prisma generate
   npx prisma db seed
   ```

5. **Install Python dependencies**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

6. **Start development servers**

   Terminal 1 - Frontend:
   ```bash
   npm run dev
   ```

   Terminal 2 - Python API:
   ```bash
   cd server
   python main.py
   ```

7. **Open the app**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

### Docker Setup

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXT_PUBLIC_PYTHON_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5432/aura_camera
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-super-secret-jwt-key
NEXTAUTH_SECRET=your-super-secret-nextauth-key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
OPENAI_API_KEY=sk-...
```

### Python API (.env)

```env
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/aura_camera
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-super-secret-jwt-key
OPENAI_API_KEY=sk-...
```

## Project Structure

```
aura-camera-app/
├── src/                          # Next.js frontend
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   ├── hooks/                    # Custom hooks
│   ├── lib/                      # Utilities
│   ├── store/                    # Zustand stores
│   └── types/                    # TypeScript types
├── server/                       # Python ML API
│   ├── api/                      # API routes
│   ├── services/                 # Business logic
│   └── main.py                   # Entry point
├── prisma/                       # Database schema
├── public/                       # Static assets
└── docker-compose.yml            # Docker orchestration
```

## API Documentation

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/login | User login |
| POST | /api/auth/register | User registration |
| POST | /api/auth/logout | User logout |
| GET | /api/auth/me | Get current user |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/sessions | Create session |
| POST | /api/sessions/:id/capture | Capture photo |
| POST | /api/sessions/:id/biofeedback | Submit biofeedback |
| POST | /api/sessions/:id/generate | Generate aura |

### ML API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /face-detection/detect | Detect face |
| POST | /biofeedback/process | Process biofeedback |
| POST | /aura/generate | Generate aura |
| POST | /reading/generate | Generate reading |

## How It Works

### 1. Face Detection
- User positions face in camera frame
- MediaPipe Face Mesh detects 468 facial landmarks
- Alignment score calculated based on face position

### 2. Biofeedback Collection
- User holds position for 5 seconds
- Touch position and stability tracked
- Simulated GSR, HRV, and stress signals generated

### 3. Aura Generation
- Biofeedback data mapped to color profiles
- Aura image created with gradient overlays
- Color positioning determined by energy flow

### 4. Reading Generation
- AI or template-based interpretation
- Color meanings analyzed
- Personalized guidance provided

## Color Meanings

| Color | Keywords | Chakra |
|-------|----------|--------|
| Red | Energy, Passion, Strength | Root |
| Orange | Creativity, Joy, Confidence | Sacral |
| Yellow | Intellect, Optimism, Clarity | Solar Plexus |
| Green | Growth, Healing, Balance | Heart |
| Blue | Communication, Truth, Calm | Throat |
| Indigo | Intuition, Wisdom, Spirituality | Third Eye |
| Violet | Spirituality, Transformation | Crown |
| Pink | Love, Compassion, Gentleness | Heart |
| Gold | Wisdom, Enlightenment, Success | Solar Plexus / Crown |
| Silver | Intuition, Feminine Power, Clarity | Third Eye |
| Turquoise | Healing, Protection, Communication | Throat / Heart |
| Magenta | Release, Transformation, Passion | Crown |
| Emerald | Abundance, Healing, Growth | Heart |
| Citrine | Abundance, Personal Will, Joy | Solar Plexus |
| Amethyst | Spirituality, Peace, Intuition | Third Eye / Crown |
| Rose Quartz | Unconditional Love, Emotional Healing | Heart |
| Jade | Harmony, Balance, Prosperity | Heart |
| Amber | Vitality, Courage, Emotional Healing | Solar Plexus |

## Subscription Plans

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 1 reading/day |
| Weekly | $5.99 | 5 readings/day |
| Monthly | $19.99 | 10 readings/day |
| Yearly | $99.99 | 20 readings/day |

## Testing

```bash
# Run frontend tests
npm test

# Run Python tests
cd server
pytest

# Run e2e tests
npm run test:e2e
```

## Deployment

### Vercel (Frontend)

```bash
npm i -g vercel
vercel --prod
```

### Railway (Python API)

1. Push code to GitHub
2. Connect Railway to repo
3. Set environment variables
4. Deploy

### Production Checklist

- [ ] Set production environment variables
- [ ] Configure SSL certificates
- [ ] Set up monitoring (Sentry)
- [ ] Configure CDN (Cloudflare)
- [ ] Set up backups
- [ ] Load testing

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for face detection
- [shadcn/ui](https://ui.shadcn.com/) for UI components
- [Aurla](https://www.aurla.app/) for inspiration

## Support

For support, email support@auracamera.app or join our [Discord](https://discord.gg/auracamera).

---

Made with 💜 by the Aura Camera Team
