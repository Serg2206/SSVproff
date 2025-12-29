import mongoose, { Document, Schema } from 'mongoose';

export interface IConsultationRequest extends Document {
  name: string;
  email: string;
  phone?: string;
  topic: string;
  problemDescription: string;
  submittedAt: Date;
}

const consultationRequestSchema: Schema = new Schema({
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
  topic: {
    type: String,
    required: true,
  },
  problemDescription: {
    type: String,
    required: true,
  },
  submittedAt: {
    type: Date,
    default: Date.now,
  },
});

export default mongoose.model<IConsultationRequest>('ConsultationRequest', consultationRequestSchema);
