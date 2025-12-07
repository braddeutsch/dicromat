"""Image generator for the Slider App - Parameter Explorer."""

import io
import random
from PIL import Image, ImageDraw
import numpy as np

from utils.luminance import calculate_luminance
from utils.dichromat_sim import simulate_image


class SliderImageGenerator:
    """Generate colorblind test images with configurable parameters."""
    
    IMAGE_SIZE = 500
    
    DEFAULT_PARAMS = {
        'fg_rgb': [150, 120, 140],
        'bg_rgb': [145, 145, 145],
        'circle_mean_size': 20,
        'circle_size_variance': 0.30,
        'noise_offset': 0.0,
        'noise_variance': 0.08,
        'pattern_density': 0.25,
    }
    
    def generate(
        self,
        fg_rgb: list,
        bg_rgb: list,
        circle_mean_size: float = 20,
        circle_size_variance: float = 0.30,
        noise_offset: float = 0.0,
        noise_variance: float = 0.08,
        pattern_density: float = 0.25,
        simulate_dichromat: bool = False,
        dichromat_type: str = 'deuteranopia',
        seed: int = None
    ) -> dict:
        """
        Generate a test image with the specified parameters.
        
        Returns dict with:
            - image_base64: Base64-encoded PNG image
            - luminance_fg: Foreground luminance (Y)
            - luminance_bg: Background luminance (Y)
            - luminance_delta: |Y_fg - Y_bg|
        """
        if seed is not None:
            rng = random.Random(seed)
            np_rng = np.random.RandomState(seed)
        else:
            rng = random.Random()
            np_rng = np.random.RandomState()
        
        size = self.IMAGE_SIZE
        img = Image.new('RGB', (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        radius = (size // 2) - 10
        
        num_dots = int(pattern_density * (size * size) / (circle_mean_size ** 2))
        num_dots = max(100, min(5000, num_dots))
        
        circle_pattern = self._create_circle_pattern(size, radius)
        
        placed_dots = []
        max_attempts = num_dots * 10
        attempts = 0
        
        while len(placed_dots) < num_dots and attempts < max_attempts:
            attempts += 1
            
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0, radius)
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            
            size_variance = circle_mean_size * circle_size_variance
            dot_size = rng.gauss(circle_mean_size, size_variance)
            dot_size = max(3, min(50, dot_size))
            
            if not (0 <= x < size and 0 <= y < size):
                continue
            
            if self._check_collision(x, y, dot_size, placed_dots):
                continue
            
            is_foreground = circle_pattern[y, x] > 128
            
            if is_foreground:
                base_color = tuple(fg_rgb)
            else:
                base_color = tuple(bg_rgb)
            
            noise = np_rng.normal(noise_offset, noise_variance)
            color = self._apply_grayscale_noise(base_color, noise)
            
            draw.ellipse(
                [x - dot_size/2, y - dot_size/2, x + dot_size/2, y + dot_size/2],
                fill=color
            )
            
            placed_dots.append((x, y, dot_size))
        
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([10, 10, size-10, size-10], fill=255)
        
        result = Image.new('RGB', (size, size), (255, 255, 255))
        result.paste(img, mask=mask)
        
        if simulate_dichromat:
            img_array = np.array(result)
            simulated = simulate_image(img_array, dichromat_type)
            result = Image.fromarray(simulated)
        
        buffer = io.BytesIO()
        result.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        import base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        luminance_fg = calculate_luminance(*fg_rgb)
        luminance_bg = calculate_luminance(*bg_rgb)
        luminance_delta = abs(luminance_fg - luminance_bg)
        
        return {
            'image_base64': image_base64,
            'luminance_fg': round(luminance_fg, 4),
            'luminance_bg': round(luminance_bg, 4),
            'luminance_delta': round(luminance_delta, 4)
        }
    
    def _create_circle_pattern(self, size: int, radius: int) -> np.ndarray:
        """Create a circular pattern mask (simple ring pattern)."""
        y, x = np.ogrid[:size, :size]
        center = size // 2
        dist_from_center = np.sqrt((x - center)**2 + (y - center)**2)
        
        inner_radius = radius * 0.3
        outer_radius = radius * 0.7
        
        mask = ((dist_from_center >= inner_radius) & 
                (dist_from_center <= outer_radius))
        
        result = np.zeros((size, size), dtype=np.uint8)
        result[mask] = 255
        return result
    
    def _check_collision(self, x: int, y: int, size: float, placed_dots: list) -> bool:
        """Check if a dot would overlap with existing dots."""
        for dx, dy, dsize in placed_dots:
            distance_sq = (x - dx) ** 2 + (y - dy) ** 2
            min_distance = (size + dsize) / 2 * 0.8
            if distance_sq < min_distance ** 2:
                return True
        return False
    
    def _apply_grayscale_noise(self, color: tuple, noise: float) -> tuple:
        """Apply grayscale noise to a color."""
        noise_value = int(noise * 255)
        return tuple(
            max(0, min(255, c + noise_value))
            for c in color
        )
