import styles from '../SliderApp.module.css';

interface ColorSlidersProps {
  label: string;
  rgb: [number, number, number];
  luminance: number | null;
  onChange: (rgb: [number, number, number]) => void;
}

export function ColorSliders({ label, rgb, luminance, onChange }: ColorSlidersProps) {
  const handleChange = (index: number, value: number) => {
    const newRgb: [number, number, number] = [...rgb];
    newRgb[index] = value;
    onChange(newRgb);
  };

  const colorPreview = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;

  return (
    <div className={styles.sliderGroup}>
      <div className={styles.sliderGroupHeader}>
        <span className={styles.sliderGroupLabel}>{label}</span>
        <div 
          className={styles.colorPreview} 
          style={{ backgroundColor: colorPreview }}
          title={colorPreview}
        />
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>R</label>
        <input
          type="range"
          min={0}
          max={255}
          value={rgb[0]}
          onChange={(e) => handleChange(0, parseInt(e.target.value))}
          className={`${styles.slider} ${styles.sliderRed}`}
        />
        <span className={styles.sliderValue}>{rgb[0]}</span>
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>G</label>
        <input
          type="range"
          min={0}
          max={255}
          value={rgb[1]}
          onChange={(e) => handleChange(1, parseInt(e.target.value))}
          className={`${styles.slider} ${styles.sliderGreen}`}
        />
        <span className={styles.sliderValue}>{rgb[1]}</span>
      </div>
      
      <div className={styles.sliderRow}>
        <label className={styles.sliderLabel}>B</label>
        <input
          type="range"
          min={0}
          max={255}
          value={rgb[2]}
          onChange={(e) => handleChange(2, parseInt(e.target.value))}
          className={`${styles.slider} ${styles.sliderBlue}`}
        />
        <span className={styles.sliderValue}>{rgb[2]}</span>
      </div>
      
      {luminance !== null && (
        <div className={styles.luminanceValue}>
          Y: {luminance.toFixed(4)}
        </div>
      )}
    </div>
  );
}
