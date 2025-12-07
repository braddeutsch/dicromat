import type { Preset, SliderParams } from '../types';
import styles from '../SliderApp.module.css';

interface PresetSelectorProps {
  presets: Preset[];
  onSelect: (params: Partial<SliderParams>) => void;
}

export function PresetSelector({ presets, onSelect }: PresetSelectorProps) {
  return (
    <div className={styles.presetSection}>
      <label className={styles.presetLabel}>Load Preset:</label>
      <select
        onChange={(e) => {
          const preset = presets.find(p => p.name === e.target.value);
          if (preset) {
            onSelect(preset.params);
          }
          e.target.value = '';
        }}
        className={styles.select}
        defaultValue=""
      >
        <option value="" disabled>Select a preset...</option>
        {presets.map((preset) => (
          <option key={preset.name} value={preset.name}>
            {preset.name}
          </option>
        ))}
      </select>
    </div>
  );
}
