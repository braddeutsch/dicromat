import styles from '../SliderApp.module.css';

interface NoiseSlidersProps {
  noiseOffset: number;
  noiseVariance: number;
  onNoiseOffsetChange: (value: number) => void;
  onNoiseVarianceChange: (value: number) => void;
}

export function NoiseSliders({
  noiseOffset,
  noiseVariance,
  onNoiseOffsetChange,
  onNoiseVarianceChange,
}: NoiseSlidersProps) {
  return (
    <div className={styles.sliderGroup}>
      <span className={styles.sliderGroupLabel}>Noise Parameters</span>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>Offset</label>
        <input
          type="range"
          min={-8}
          max={8}
          step={1}
          value={noiseOffset * 100}
          onChange={(e) => onNoiseOffsetChange(parseFloat(e.target.value) / 100)}
          className={styles.slider}
        />
        <span className={styles.sliderValue}>{noiseOffset.toFixed(2)}</span>
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>Variance</label>
        <input
          type="range"
          min={0}
          max={25}
          step={1}
          value={noiseVariance * 100}
          onChange={(e) => onNoiseVarianceChange(parseFloat(e.target.value) / 100)}
          className={styles.slider}
        />
        <span className={styles.sliderValue}>{noiseVariance.toFixed(2)}</span>
      </div>
    </div>
  );
}
