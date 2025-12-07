import styles from '../SliderApp.module.css';

interface PatternSlidersProps {
  circleMeanSize: number;
  circleSizeVariance: number;
  patternDensity: number;
  onCircleMeanSizeChange: (value: number) => void;
  onCircleSizeVarianceChange: (value: number) => void;
  onPatternDensityChange: (value: number) => void;
}

export function PatternSliders({
  circleMeanSize,
  circleSizeVariance,
  patternDensity,
  onCircleMeanSizeChange,
  onCircleSizeVarianceChange,
  onPatternDensityChange,
}: PatternSlidersProps) {
  return (
    <div className={styles.sliderGroup}>
      <span className={styles.sliderGroupLabel}>Circle Parameters</span>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>Size</label>
        <input
          type="range"
          min={6}
          max={40}
          step={0.5}
          value={circleMeanSize}
          onChange={(e) => onCircleMeanSizeChange(parseFloat(e.target.value))}
          className={styles.slider}
        />
        <span className={styles.sliderValue}>{circleMeanSize.toFixed(1)} px</span>
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>Variance</label>
        <input
          type="range"
          min={0}
          max={60}
          step={1}
          value={circleSizeVariance * 100}
          onChange={(e) => onCircleSizeVarianceChange(parseFloat(e.target.value) / 100)}
          className={styles.slider}
        />
        <span className={styles.sliderValue}>{Math.round(circleSizeVariance * 100)}%</span>
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>Density</label>
        <input
          type="range"
          min={10}
          max={60}
          step={1}
          value={patternDensity * 100}
          onChange={(e) => onPatternDensityChange(parseFloat(e.target.value) / 100)}
          className={styles.slider}
        />
        <span className={styles.sliderValue}>{Math.round(patternDensity * 100)}%</span>
      </div>
    </div>
  );
}
