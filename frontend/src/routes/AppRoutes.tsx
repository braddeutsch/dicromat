import { Routes, Route, Navigate } from 'react-router-dom';
import { WelcomePage } from '../pages/WelcomePage';
import { TestPage } from '../pages/TestPage';
import { ResultsPage } from '../pages/ResultsPage';

function NotFound() {
  return (
    <div className="page">
      <div className="container text-center">
        <div className="card">
          <h1>404 - Page Not Found</h1>
          <p className="text-muted mt-2">The page you're looking for doesn't exist.</p>
          <a href="/" style={{ display: 'inline-block', marginTop: '1rem' }}>
            Go to Home
          </a>
        </div>
      </div>
    </div>
  );
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/test/:sessionId" element={<TestPage />} />
      <Route path="/results/:sessionId" element={<ResultsPage />} />
      <Route path="/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  );
}
