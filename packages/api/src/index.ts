import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// --- Middleware ---
app.use(helmet());

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});
app.use(limiter);

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000', // Next.js dev
  credentials: true,
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// --- Routes ---
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK', service: 'SSV-Prof API' });
});

// .routes
// app.use('/api/library', libraryRoutes);
// app.use('/api/internship', internshipRoutes);
// app.use('/api/consultation', consultationRoutes);

// 404
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route Not Found' });
});

// --- MongoDB Connection ---
mongoose.connect(process.env.MONGODB_URI!)
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch((err) => console.error('❌ MongoDB connection error:', err));

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`🚀 SSV-Prof API server running on port ${PORT}`);
  console.log(`📋 Health check: http://localhost:${PORT}/health`);
});

export default app;
