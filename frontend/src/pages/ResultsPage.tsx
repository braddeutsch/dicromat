import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import { Button } from '../components/Button';
import type { TestResults } from '../types';
import styles from './ResultsPage.module.css';

export function ResultsPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [results, setResults] = useState<TestResults | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;

    const fetchResults = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await api.getResults(sessionId);
        setResults(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load results');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [sessionId]);

  if (isLoading) {
    return (
      <div className="page">
        <div className={`container ${styles.container}`}>
          <div className={`card ${styles.loading}`}>
            <div className={styles.spinner} />
            <p>Loading your results...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !results) {
    return (
      <div className="page">
        <div className={`container ${styles.container}`}>
          <div className={`card ${styles.errorCard}`}>
            <h1>Error</h1>
            <p className="text-muted mt-2">{error || 'Results not found'}</p>
            <Link to="/">
              <Button variant="primary" className="mt-4">Start New Test</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const { analysis } = results;
  const statusClass = analysis.color_vision_status === 'normal' 
    ? styles.statusNormal 
    : analysis.color_vision_status === 'deficient' 
      ? styles.statusDeficient 
      : styles.statusInconclusive;

  return (
    <div className="page">
      <div className={`container ${styles.container}`}>
        <header className={styles.header}>
          <h1>DICROMAT - Your Results</h1>
        </header>

        <main>
          <section className={`card ${styles.summaryCard}`}>
            <div className={`${styles.statusBadge} ${statusClass}`}>
              {analysis.color_vision_status === 'normal' ? (
                <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 6L9 17l-5-5" />
                </svg>
              ) : analysis.color_vision_status === 'deficient' ? (
                <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </div>

            <h2 className={styles.statusTitle}>
              Your Color Vision: <span className={statusClass}>
                {analysis.color_vision_status.charAt(0).toUpperCase() + analysis.color_vision_status.slice(1)}
              </span>
            </h2>

            {analysis.suspected_type && (
              <p className={styles.suspectedType}>
                Suspected Type: <strong>{analysis.suspected_type}</strong>
              </p>
            )}

            <p className={styles.confidence}>
              Confidence: <strong>{analysis.confidence.charAt(0).toUpperCase() + analysis.confidence.slice(1)}</strong>
            </p>

            <p className={styles.score}>
              Score: {results.total_correct} / {results.total_images} correct
            </p>
          </section>

          <section className={`card ${styles.interpretationCard}`}>
            <h3>What does this mean?</h3>
            <p>{results.interpretation}</p>
          </section>

          <section className={`card ${styles.answersCard}`}>
            <h3>Your Answers</h3>
            <div className={styles.answersTable}>
              <div className={styles.answersHeader}>
                <span>Image</span>
                <span>Type</span>
                <span>Your Answer</span>
                <span>Correct</span>
                <span>Result</span>
              </div>
              {results.answers.map((answer) => (
                <div 
                  key={answer.image_number} 
                  className={`${styles.answerRow} ${answer.is_correct ? styles.correct : styles.incorrect}`}
                >
                  <span>#{answer.image_number}</span>
                  <span className={styles.type}>{answer.dichromism_type}</span>
                  <span>{answer.user_answer ?? 'None'}</span>
                  <span>{answer.correct_answer}</span>
                  <span className={styles.resultIcon}>
                    {answer.is_correct ? (
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    )}
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className={`card ${styles.recommendationsCard}`}>
            <h3>Recommendations</h3>
            <p>{results.recommendations}</p>
          </section>

          <div className={styles.actions}>
            <Link to="/">
              <Button variant="primary" size="large">Take Test Again</Button>
            </Link>
          </div>
        </main>
      </div>
    </div>
  );
}
