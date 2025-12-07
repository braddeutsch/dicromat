import { useState } from 'react';
import { api } from '../services/api';
import styles from './TestImage.module.css';

interface TestImageProps {
  sessionId: string;
  imageNumber: number;
}

export function TestImage({ sessionId, imageNumber }: TestImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const imageUrl = api.getImageUrl(sessionId, imageNumber);

  const handleLoad = () => {
    setIsLoading(false);
    setHasError(false);
  };

  const handleError = () => {
    setIsLoading(false);
    setHasError(true);
  };

  const handleRetry = () => {
    setIsLoading(true);
    setHasError(false);
  };

  return (
    <div className={styles.container}>
      {isLoading && (
        <div className={styles.skeleton}>
          <div className={styles.spinner} />
          <span className="sr-only">Loading image...</span>
        </div>
      )}
      
      {hasError ? (
        <div className={styles.error}>
          <p>Failed to load image</p>
          <button className={styles.retryButton} onClick={handleRetry}>
            Retry
          </button>
        </div>
      ) : (
        <img
          key={`${sessionId}-${imageNumber}`}
          src={imageUrl}
          alt={`Color blindness test plate ${imageNumber}`}
          className={`${styles.image} ${isLoading ? styles.hidden : ''}`}
          onLoad={handleLoad}
          onError={handleError}
        />
      )}
    </div>
  );
}
