export interface SliderParams {
  fg_rgb: [number, number, number];
  bg_rgb: [number, number, number];
  circle_mean_size: number;
  circle_size_variance: number;
  noise_offset: number;
  noise_variance: number;
  pattern_density: number;
  simulate_dichromat: boolean;
  dichromat_type: 'deuteranopia' | 'protanopia' | 'tritanopia';
  seed?: number;
}

export interface GenerateResponse {
  image_base64: string;
  luminance_fg: number;
  luminance_bg: number;
  luminance_delta: number;
}

export interface SavedParameter {
  id: string;
  timestamp: string;
  params: SliderParams;
  note?: string;
  luminance_fg: number;
  luminance_bg: number;
}

export interface Preset {
  name: string;
  description: string;
  params: Omit<SliderParams, 'simulate_dichromat' | 'dichromat_type' | 'seed'>;
}

export const DEFAULT_PARAMS: SliderParams = {
  fg_rgb: [150, 120, 140],
  bg_rgb: [145, 145, 145],
  circle_mean_size: 20,
  circle_size_variance: 0.30,
  noise_offset: 0.0,
  noise_variance: 0.08,
  pattern_density: 0.25,
  simulate_dichromat: false,
  dichromat_type: 'deuteranopia',
};
