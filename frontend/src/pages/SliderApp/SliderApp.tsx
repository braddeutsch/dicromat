import { useState, useEffect, useCallback, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
  ImageDisplay,
  ColorSliders,
  PatternSliders,
  NoiseSliders,
  LuminanceDisplay,
  DichromatToggle,
  SavedParameters,
  PresetSelector,
} from './components';
import { generateImage, matchLuminance, getPresets } from './api';
import type { SliderParams, SavedParameter, Preset, GenerateResponse } from './types';
import { DEFAULT_PARAMS } from './types';
import styles from './SliderApp.module.css';

const STORAGE_KEY = 'slider-app-saved-params';

function loadSavedParams(): SavedParameter[] {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

function saveSavedParams(params: SavedParameter[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(params));
}

export function SliderApp() {
  const [params, setParams] = useState<SliderParams>(DEFAULT_PARAMS);
  const [imageData, setImageData] = useState<GenerateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isMatching, setIsMatching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedParams, setSavedParams] = useState<SavedParameter[]>(loadSavedParams);
  const [presets, setPresets] = useState<Preset[]>([]);
  
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const initialLoadRef = useRef(false);

  useEffect(() => {
    getPresets().then(setPresets).catch(console.error);
  }, []);

  const doGenerate = useCallback(async (p: SliderParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await generateImage(p);
      setImageData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate image');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const debouncedGenerate = useCallback((p: SliderParams) => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    debounceRef.current = setTimeout(() => {
      doGenerate(p);
    }, 150);
  }, [doGenerate]);

  useEffect(() => {
    if (!initialLoadRef.current) {
      initialLoadRef.current = true;
      doGenerate(DEFAULT_PARAMS);
    }
  }, [doGenerate]);

  const updateParams = useCallback((updates: Partial<SliderParams>) => {
    setParams(prev => {
      const newParams = { ...prev, ...updates };
      debouncedGenerate(newParams);
      return newParams;
    });
  }, [debouncedGenerate]);

  const handleMatchLuminance = async () => {
    setIsMatching(true);
    try {
      const result = await matchLuminance(params.fg_rgb, params.bg_rgb);
      updateParams({ fg_rgb: result.matched_fg_rgb });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to match luminance');
    } finally {
      setIsMatching(false);
    }
  };

  const handleSave = () => {
    const note = prompt('Add a note (optional):');
    const newSaved: SavedParameter = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      params: { ...params },
      note: note || undefined,
      luminance_fg: imageData?.luminance_fg ?? 0,
      luminance_bg: imageData?.luminance_bg ?? 0,
    };
    const updated = [...savedParams, newSaved];
    setSavedParams(updated);
    saveSavedParams(updated);
  };

  const handleLoad = (loadedParams: SliderParams) => {
    setParams(loadedParams);
    doGenerate(loadedParams);
  };

  const handleDelete = (id: string) => {
    const updated = savedParams.filter(p => p.id !== id);
    setSavedParams(updated);
    saveSavedParams(updated);
  };

  const handleExport = () => {
    const headers = [
      'timestamp', 'fg_r', 'fg_g', 'fg_b', 'bg_r', 'bg_g', 'bg_b',
      'circle_mean_size', 'circle_size_variance', 'noise_offset', 'noise_variance',
      'pattern_density', 'luminance_fg', 'luminance_bg', 'note'
    ];
    const rows = savedParams.map(s => [
      s.timestamp,
      s.params.fg_rgb[0], s.params.fg_rgb[1], s.params.fg_rgb[2],
      s.params.bg_rgb[0], s.params.bg_rgb[1], s.params.bg_rgb[2],
      s.params.circle_mean_size, s.params.circle_size_variance,
      s.params.noise_offset, s.params.noise_variance, s.params.pattern_density,
      s.luminance_fg, s.luminance_bg, s.note || ''
    ]);
    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `slider-params-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    if (confirm('Reset all parameters to defaults?')) {
      setParams(DEFAULT_PARAMS);
      doGenerate(DEFAULT_PARAMS);
    }
  };

  const handlePresetSelect = (presetParams: Partial<SliderParams>) => {
    const newParams = { ...params, ...presetParams };
    setParams(newParams);
    doGenerate(newParams);
  };

  return (
    <div className={styles.page}>
      <Link to="/" className={styles.backLink}>
        &larr; Back to Home
      </Link>
      
      <header className={styles.header}>
        <h1>Slider App - Parameter Explorer</h1>
        <p>Interactive colorblind test image parameter exploration</p>
      </header>

      {error && <div className={styles.errorMessage}>{error}</div>}

      <div className={styles.container}>
        <div className={styles.leftPanel}>
          <ImageDisplay
            imageBase64={imageData?.image_base64 ?? null}
            isLoading={isLoading}
          />
          
          <SavedParameters
            savedParams={savedParams}
            onLoad={handleLoad}
            onDelete={handleDelete}
            onExport={handleExport}
          />
        </div>

        <div className={styles.rightPanel}>
          <div className={styles.controlsCard}>
            <ColorSliders
              label="Foreground RGB"
              rgb={params.fg_rgb}
              luminance={imageData?.luminance_fg ?? null}
              onChange={(rgb) => updateParams({ fg_rgb: rgb })}
            />
            
            <ColorSliders
              label="Background RGB"
              rgb={params.bg_rgb}
              luminance={imageData?.luminance_bg ?? null}
              onChange={(rgb) => updateParams({ bg_rgb: rgb })}
            />

            <LuminanceDisplay
              luminanceFg={imageData?.luminance_fg ?? null}
              luminanceBg={imageData?.luminance_bg ?? null}
              luminanceDelta={imageData?.luminance_delta ?? null}
              onMatchLuminance={handleMatchLuminance}
              isMatching={isMatching}
            />
          </div>

          <div className={styles.controlsCard}>
            <PatternSliders
              circleMeanSize={params.circle_mean_size}
              circleSizeVariance={params.circle_size_variance}
              patternDensity={params.pattern_density}
              onCircleMeanSizeChange={(v) => updateParams({ circle_mean_size: v })}
              onCircleSizeVarianceChange={(v) => updateParams({ circle_size_variance: v })}
              onPatternDensityChange={(v) => updateParams({ pattern_density: v })}
            />
            
            <NoiseSliders
              noiseOffset={params.noise_offset}
              noiseVariance={params.noise_variance}
              onNoiseOffsetChange={(v) => updateParams({ noise_offset: v })}
              onNoiseVarianceChange={(v) => updateParams({ noise_variance: v })}
            />
          </div>

          <div className={styles.controlsCard}>
            <DichromatToggle
              enabled={params.simulate_dichromat}
              type={params.dichromat_type}
              onEnabledChange={(v) => updateParams({ simulate_dichromat: v })}
              onTypeChange={(v) => updateParams({ dichromat_type: v })}
            />
            
            {presets.length > 0 && (
              <PresetSelector
                presets={presets}
                onSelect={handlePresetSelect}
              />
            )}

            <div className={styles.actionButtons}>
              <button onClick={handleSave} className={styles.saveButton}>
                Save Parameters
              </button>
              <button onClick={handleReset} className={styles.resetButton}>
                Reset to Defaults
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
