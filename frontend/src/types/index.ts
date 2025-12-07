export interface Metadata {
  age_range?: string;
  gender?: string;
  previous_diagnosis?: boolean;
}

export interface StartTestResponse {
  session_id: string;
  created_at: string;
  total_images: number;
}

export interface SubmitAnswerResponse {
  success: boolean;
  image_number: number;
  next_image: number | null;
  is_complete: boolean;
  results_available: boolean;
}

export interface AnswerDetail {
  image_number: number;
  correct_answer: number;
  user_answer: number | null;
  is_correct: boolean;
  dichromism_type: string;
}

export interface ResultsAnalysis {
  color_vision_status: 'normal' | 'deficient' | 'inconclusive';
  suspected_type: string | null;
  confidence: 'high' | 'medium' | 'low';
  details: {
    protanopia_errors: number;
    deuteranopia_errors: number;
    tritanopia_errors: number;
    normal_errors: number;
  };
}

export interface TestResults {
  session_id: string;
  completed_at: string | null;
  total_correct: number;
  total_images: number;
  analysis: ResultsAnalysis;
  interpretation: string;
  recommendations: string;
  answers: AnswerDetail[];
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

export interface Answer {
  imageNumber: number;
  userAnswer: number | null;
}
