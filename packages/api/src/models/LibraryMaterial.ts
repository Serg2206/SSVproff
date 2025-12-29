import mongoose, { Document, Schema } from 'mongoose';

export interface ILibraryMaterial extends Document {
  title: string;
  author: string;
  description?: string;
  category?: string;
  filePath: string;
  uploadedAt: Date;
  uploadedBy?: string;
}

const libraryMaterialSchema: Schema = new Schema({
  title: {
    type: String,
    required: true,
  },
  author: {
    type: String,
    required: true,
  },
  description: {
    type: String,
  },
  category: {
    type: String,
  },
  filePath: {
    type: String,
    required: true,
  },
  uploadedAt: {
    type: Date,
    default: Date.now,
  },
  uploadedBy: {
    type: String,
  },
});

export default mongoose.model<ILibraryMaterial>('LibraryMaterial', libraryMaterialSchema);
