import { createContext } from 'react';
import type { Metadata, Answer } from '../types';

export interface TestContextType {
  sessionId: string | null;
  currentImageNumber: number;
  totalImages: number;
  answers: Answer[];
  isTestComplete: boolean;
  isLoading: boolean;
  error: string | null;
  startTest: (metadata?: Metadata) => Promise<string>;
  submitAnswer: (imageNumber: number, userAnswer: number | null) => Promise<boolean>;
  resetTest: () => void;
  clearError: () => void;
}

export const TestContext = createContext<TestContextType | null>(null);
