import mongoose, { Document, Schema } from 'mongoose';

export interface IInternshipApplication extends Document {
  name: string;
  email: string;
  phone?: string;
  specialization: string;
  experience?: string;
  goals?: string;
  submittedAt: Date;
}

const internshipApplicationSchema: Schema = new Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  phone: {
    type: String,
  },
  specialization: {
    type: String,
    required: true,
  },
  experience: {
    type: String,
  },
  goals: {
    type: String,
  },
  submittedAt: {
    type: Date,
    default: Date.now,
  },
});

export default mongoose.model<IInternshipApplication>('InternshipApplication', internshipApplicationSchema);
