import styles from '../SliderApp.module.css';

interface DichromatToggleProps {
  enabled: boolean;
  type: 'deuteranopia' | 'protanopia' | 'tritanopia';
  onEnabledChange: (enabled: boolean) => void;
  onTypeChange: (type: 'deuteranopia' | 'protanopia' | 'tritanopia') => void;
}

export function DichromatToggle({
  enabled,
  type,
  onEnabledChange,
  onTypeChange,
}: DichromatToggleProps) {
  return (
    <div className={styles.dichromatSection}>
      <label className={styles.checkboxLabel}>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => onEnabledChange(e.target.checked)}
        />
        <span>Simulate Dichromat View</span>
      </label>
      
      {enabled && (
        <select
          value={type}
          onChange={(e) => onTypeChange(e.target.value as typeof type)}
          className={styles.select}
        >
          <option value="deuteranopia">Deuteranopia (Red-Green)</option>
          <option value="protanopia">Protanopia (Red-Green)</option>
          <option value="tritanopia">Tritanopia (Blue-Yellow)</option>
        </select>
      )}
    </div>
  );
}
