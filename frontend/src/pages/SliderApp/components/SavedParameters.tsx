import type { SavedParameter, SliderParams } from '../types';
import styles from '../SliderApp.module.css';

interface SavedParametersProps {
  savedParams: SavedParameter[];
  onLoad: (params: SliderParams) => void;
  onDelete: (id: string) => void;
  onExport: () => void;
}

export function SavedParameters({
  savedParams,
  onLoad,
  onDelete,
  onExport,
}: SavedParametersProps) {
  if (savedParams.length === 0) {
    return (
      <div className={styles.savedSection}>
        <h3>Saved Parameters</h3>
        <p className={styles.emptyMessage}>No saved parameters yet</p>
      </div>
    );
  }

  return (
    <div className={styles.savedSection}>
      <div className={styles.savedHeader}>
        <h3>Saved Parameters ({savedParams.length})</h3>
        <button onClick={onExport} className={styles.exportButton}>
          Export CSV
        </button>
      </div>
      
      <div className={styles.savedList}>
        {savedParams.map((saved, index) => (
          <div key={saved.id} className={styles.savedItem}>
            <div className={styles.savedItemHeader}>
              <span className={styles.savedItemIndex}>#{index + 1}</span>
              <span className={styles.savedItemTime}>
                {new Date(saved.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className={styles.savedItemColors}>
              <div 
                className={styles.colorSwatch}
                style={{ backgroundColor: `rgb(${saved.params.fg_rgb.join(',')})` }}
                title={`FG: ${saved.params.fg_rgb.join(', ')}`}
              />
              <div 
                className={styles.colorSwatch}
                style={{ backgroundColor: `rgb(${saved.params.bg_rgb.join(',')})` }}
                title={`BG: ${saved.params.bg_rgb.join(', ')}`}
              />
              <span className={styles.savedItemDelta}>
                ΔY: {Math.abs(saved.luminance_fg - saved.luminance_bg).toFixed(4)}
              </span>
            </div>
            {saved.note && (
              <div className={styles.savedItemNote}>{saved.note}</div>
            )}
            <div className={styles.savedItemActions}>
              <button 
                onClick={() => onLoad(saved.params)}
                className={styles.loadButton}
              >
                Load
              </button>
              <button 
                onClick={() => onDelete(saved.id)}
                className={styles.deleteButton}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
