import { useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useTest } from '../context/useTest';
import { TestImage } from '../components/TestImage';
import { AnswerInput } from '../components/AnswerInput';
import { ProgressBar } from '../components/ProgressBar';
import styles from './TestPage.module.css';

export function TestPage() {
  const { sessionId: paramSessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const {
    sessionId,
    currentImageNumber,
    totalImages,
    isLoading,
    error,
    submitAnswer,
    clearError,
  } = useTest();

  useEffect(() => {
    if (!paramSessionId || (sessionId && paramSessionId !== sessionId)) {
      navigate('/', { replace: true });
    }
  }, [paramSessionId, sessionId, navigate]);

  const handleSubmitAnswer = async (answer: number | null) => {
    clearError();
    try {
      const isComplete = await submitAnswer(currentImageNumber, answer);
      if (isComplete) {
        navigate(`/results/${sessionId}`, { replace: true });
      }
    } catch {
      // Error is handled by context
    }
  };

  if (!sessionId || sessionId !== paramSessionId) {
    return (
      <div className="page">
        <div className={`container ${styles.errorContainer}`}>
          <div className="card text-center">
            <h1>Session Not Found</h1>
            <p className="text-muted mt-2">Please start a new test.</p>
            <Link to="/" className={styles.homeLink}>Go to Home</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className={`container ${styles.container}`}>
        <header className={styles.header}>
          <h1 className={styles.title}>DICROMAT</h1>
          <span className={styles.progress}>{currentImageNumber} / {totalImages}</span>
        </header>

        <main className={`card ${styles.main}`}>
          <div className={styles.imageSection}>
            <TestImage sessionId={sessionId} imageNumber={currentImageNumber} />
          </div>

          <div className={styles.inputSection}>
            <AnswerInput
              onSubmit={handleSubmitAnswer}
              isSubmitting={isLoading}
              imageNumber={currentImageNumber}
            />

            {error && (
              <p className={styles.error} role="alert">{error}</p>
            )}
          </div>
        </main>

        <footer className={styles.footer}>
          <ProgressBar current={currentImageNumber - 1} total={totalImages} />
        </footer>
      </div>
    </div>
  );
}
