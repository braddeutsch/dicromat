import styles from '../SliderApp.module.css';

interface LuminanceDisplayProps {
  luminanceFg: number | null;
  luminanceBg: number | null;
  luminanceDelta: number | null;
  onMatchLuminance: () => void;
  isMatching: boolean;
}

export function LuminanceDisplay({
  luminanceFg,
  luminanceBg,
  luminanceDelta,
  onMatchLuminance,
  isMatching,
}: LuminanceDisplayProps) {
  const isMatched = luminanceDelta !== null && luminanceDelta < 0.01;
  
  return (
    <div className={styles.luminanceSection}>
      <div className={styles.luminanceRow}>
        <span>Foreground Y:</span>
        <span>{luminanceFg !== null ? luminanceFg.toFixed(4) : '-'}</span>
      </div>
      <div className={styles.luminanceRow}>
        <span>Background Y:</span>
        <span>{luminanceBg !== null ? luminanceBg.toFixed(4) : '-'}</span>
      </div>
      <div className={`${styles.luminanceRow} ${styles.luminanceDelta}`}>
        <span>Delta Y:</span>
        <span className={isMatched ? styles.matched : ''}>
          {luminanceDelta !== null ? luminanceDelta.toFixed(4) : '-'}
          {isMatched && ' ✓'}
        </span>
      </div>
      <button 
        onClick={onMatchLuminance}
        disabled={isMatching}
        className={styles.matchButton}
      >
        {isMatching ? 'Matching...' : 'Match Luminance'}
      </button>
    </div>
  );
}
