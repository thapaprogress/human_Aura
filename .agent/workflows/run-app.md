---
description: Start both the Next.js frontend and the Python ML backend for the Aura app
---

### Prerequisites
- Node.js installed
- Python installed
- Prisma CLI installed

### Step 1: Start Frontend
1. Open a terminal
2. Navigate to `aura/`
3. Run `npm install`
4. Run `npx prisma generate`
5. Run `npm run dev`

### Step 2: Start Backend
1. Open a second terminal
2. Navigate to `aura/server/`
3. Run `pip install -r requirements.txt`
4. Run `python main.py`

### Step 3: Access the Application
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
