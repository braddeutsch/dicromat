import type { SliderParams, GenerateResponse, Preset } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function generateImage(params: SliderParams): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE_URL}/api/slider/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || 'Failed to generate image');
  }
  
  return response.json();
}

export async function matchLuminance(
  fg_rgb: [number, number, number],
  bg_rgb: [number, number, number]
): Promise<{ matched_fg_rgb: [number, number, number]; luminance_delta: number }> {
  const response = await fetch(`${API_BASE_URL}/api/slider/match-luminance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fg_rgb, bg_rgb }),
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || 'Failed to match luminance');
  }
  
  return response.json();
}

export async function getPresets(): Promise<Preset[]> {
  const response = await fetch(`${API_BASE_URL}/api/slider/presets`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch presets');
  }
  
  const data = await response.json();
  return data.presets;
}
