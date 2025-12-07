import { useState, useCallback, type ReactNode } from 'react';
import { api } from '../services/api';
import type { Answer } from '../types';
import type { Metadata } from '../types';
import { TestContext } from './TestContextType';

export function TestProvider({ children }: { children: ReactNode }) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentImageNumber, setCurrentImageNumber] = useState(1);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [isTestComplete, setIsTestComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalImages = 10;

  const startTest = useCallback(async (metadata?: Metadata): Promise<string> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.startTest(metadata);
      setSessionId(response.session_id);
      setCurrentImageNumber(1);
      setAnswers([]);
      setIsTestComplete(false);
      return response.session_id;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to start test';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const submitAnswer = useCallback(async (imageNumber: number, userAnswer: number | null): Promise<boolean> => {
    if (!sessionId) {
      setError('No active session');
      return false;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await api.submitAnswer(sessionId, imageNumber, userAnswer);
      
      setAnswers(prev => [...prev, { imageNumber, userAnswer }]);
      
      if (response.is_complete) {
        setIsTestComplete(true);
        return true;
      }
      
      if (response.next_image) {
        setCurrentImageNumber(response.next_image);
      }
      return false;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to submit answer';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  const resetTest = useCallback(() => {
    setSessionId(null);
    setCurrentImageNumber(1);
    setAnswers([]);
    setIsTestComplete(false);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return (
    <TestContext.Provider
      value={{
        sessionId,
        currentImageNumber,
        totalImages,
        answers,
        isTestComplete,
        isLoading,
        error,
        startTest,
        submitAnswer,
        resetTest,
        clearError,
      }}
    >
      {children}
    </TestContext.Provider>
  );
}


