import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTest } from '../context/useTest';
import { Button } from '../components/Button';
import type { Metadata } from '../types';
import styles from './WelcomePage.module.css';

export function WelcomePage() {
  const navigate = useNavigate();
  const { startTest, isLoading, error, clearError } = useTest();
  const [showMetadata, setShowMetadata] = useState(false);
  const [metadata, setMetadata] = useState<Metadata>({});

  const handleStartTest = async (e: FormEvent) => {
    e.preventDefault();
    clearError();
    
    try {
      const sessionId = await startTest(showMetadata ? metadata : undefined);
      navigate(`/test/${sessionId}`);
    } catch {
      // Error is handled by context
    }
  };

  return (
    <div className="page">
      <div className={`container ${styles.container}`}>
        <header className={styles.header}>
          <h1 className={styles.title}>DICROMAT</h1>
          <p className={styles.subtitle}>Color Vision Test</p>
        </header>

        <main className={`card ${styles.main}`}>
          <section className={styles.section}>
            <h2>What is this test?</h2>
            <p>
              This test screens for dichromism, a type of color blindness that affects 
              how you perceive certain colors. The test uses Ishihara-style plates to 
              detect protanopia (red-blindness), deuteranopia (green-blindness), and 
              tritanopia (blue-blindness).
            </p>
          </section>

          <section className={styles.section}>
            <h2>Instructions</h2>
            <ul className={styles.instructions}>
              <li>You will see 10 images with hidden numbers</li>
              <li>Enter the number you see (0-99)</li>
              <li>If you don't see a number, select "No number visible"</li>
              <li>Test takes approximately 3-5 minutes</li>
            </ul>
          </section>

          <form onSubmit={handleStartTest} className={styles.form}>
            <button
              type="button"
              className={styles.metadataToggle}
              onClick={() => setShowMetadata(!showMetadata)}
            >
              {showMetadata ? '- Hide' : '+ Show'} optional demographic info
            </button>

            {showMetadata && (
              <div className={styles.metadataForm}>
                <div className={styles.field}>
                  <label htmlFor="age-range">Age Range</label>
                  <select
                    id="age-range"
                    value={metadata.age_range || ''}
                    onChange={(e) => setMetadata({ ...metadata, age_range: e.target.value || undefined })}
                  >
                    <option value="">Prefer not to say</option>
                    <option value="under-18">Under 18</option>
                    <option value="18-24">18-24</option>
                    <option value="25-34">25-34</option>
                    <option value="35-44">35-44</option>
                    <option value="45-54">45-54</option>
                    <option value="55-64">55-64</option>
                    <option value="65+">65+</option>
                  </select>
                </div>

                <div className={styles.field}>
                  <label htmlFor="gender">Gender</label>
                  <select
                    id="gender"
                    value={metadata.gender || ''}
                    onChange={(e) => setMetadata({ ...metadata, gender: e.target.value || undefined })}
                  >
                    <option value="">Prefer not to say</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <label className={styles.checkboxField}>
                  <input
                    type="checkbox"
                    checked={metadata.previous_diagnosis || false}
                    onChange={(e) => setMetadata({ ...metadata, previous_diagnosis: e.target.checked })}
                  />
                  <span>I have been previously diagnosed with color blindness</span>
                </label>
              </div>
            )}

            {error && (
              <p className={styles.error} role="alert">{error}</p>
            )}

            <Button type="submit" size="large" isLoading={isLoading}>
              Start Test
            </Button>
          </form>
        </main>

        <footer className={styles.footer}>
          <p className="text-small text-muted">
            <strong>Disclaimer:</strong> This is a screening tool only and does not 
            replace professional medical diagnosis. Please consult an eye care 
            professional for a comprehensive evaluation.
          </p>
          <p className="text-small mt-4">
            <a href="/slider">Open Parameter Explorer (Slider App)</a>
          </p>
        </footer>
      </div>
    </div>
  );
}
