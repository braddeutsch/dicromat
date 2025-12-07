import type { Metadata, StartTestResponse, SubmitAnswerResponse, TestResults, ApiError } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData: ApiError = await response.json().catch(() => ({
        error: { code: 'UNKNOWN_ERROR', message: 'An unexpected error occurred' }
      }));
      throw new Error(errorData.error.message || 'Request failed');
    }
    return response.json();
  }

  async startTest(metadata?: Metadata): Promise<StartTestResponse> {
    const response = await fetch(`${this.baseUrl}/api/test/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ metadata }),
    });
    return this.handleResponse<StartTestResponse>(response);
  }

  getImageUrl(sessionId: string, imageNumber: number): string {
    return `${this.baseUrl}/api/test/${sessionId}/image/${imageNumber}`;
  }

  async submitAnswer(
    sessionId: string,
    imageNumber: number,
    userAnswer: number | null
  ): Promise<SubmitAnswerResponse> {
    const response = await fetch(`${this.baseUrl}/api/test/${sessionId}/answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_number: imageNumber,
        user_answer: userAnswer,
      }),
    });
    return this.handleResponse<SubmitAnswerResponse>(response);
  }

  async getResults(sessionId: string): Promise<TestResults> {
    const response = await fetch(`${this.baseUrl}/api/test/${sessionId}/results`);
    return this.handleResponse<TestResults>(response);
  }
}

export const api = new ApiService(API_BASE_URL);
