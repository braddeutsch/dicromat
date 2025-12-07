import { useContext } from 'react';
import { TestContext } from './TestContextType';

export function useTest() {
  const context = useContext(TestContext);
  if (!context) {
    throw new Error('useTest must be used within a TestProvider');
  }
  return context;
}
