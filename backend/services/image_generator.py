import hashlib
import io
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class ImageGenerator:
    IMAGE_SIZE = 400
    DOT_COUNT_MIN = 500
    DOT_COUNT_MAX = 800
    DOT_SIZE_MIN = 8
    DOT_SIZE_MAX = 20
    
    COLOR_PALETTES = {
        'protanopia': {
            'background': (200, 100, 100),
            'foreground': (100, 180, 100),
        },
        'deuteranopia': {
            'background': (100, 180, 100),
            'foreground': (200, 100, 100),
        },
        'tritanopia': {
            'background': (100, 100, 200),
            'foreground': (220, 220, 100),
        },
        'control': {
            'background': (150, 150, 150),
            'foreground': (50, 50, 50),
        }
    }
    
    TEST_CONFIG = [
        {'type': 'protanopia', 'numbers': [12, 29, 42, 57, 74]},
        {'type': 'protanopia', 'numbers': [12, 29, 42, 57, 74]},
        {'type': 'protanopia', 'numbers': [12, 29, 42, 57, 74]},
        {'type': 'deuteranopia', 'numbers': [8, 15, 35, 63, 88]},
        {'type': 'deuteranopia', 'numbers': [8, 15, 35, 63, 88]},
        {'type': 'deuteranopia', 'numbers': [8, 15, 35, 63, 88]},
        {'type': 'tritanopia', 'numbers': [5, 26, 45, 69, 96]},
        {'type': 'tritanopia', 'numbers': [5, 26, 45, 69, 96]},
        {'type': 'tritanopia', 'numbers': [5, 26, 45, 69, 96]},
        {'type': 'control', 'numbers': [7, 16, 23, 38, 52]},
    ]
    
    def __init__(self, seed_salt='dicromat-salt'):
        self.seed_salt = seed_salt
    
    def _get_seed(self, session_id: str, image_number: int) -> int:
        seed_str = f"{self.seed_salt}-{session_id}-{image_number}"
        return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    
    def get_test_config(self, session_id: str, image_number: int) -> dict:
        if image_number < 1 or image_number > 10:
            raise ValueError("image_number must be between 1 and 10")
        
        config = self.TEST_CONFIG[image_number - 1]
        seed = self._get_seed(session_id, image_number)
        rng = random.Random(seed)
        
        correct_answer = rng.choice(config['numbers'])
        
        return {
            'dichromism_type': config['type'],
            'correct_answer': correct_answer
        }
    
    def _vary_color(self, base_color: tuple, rng: random.Random, variation: int = 25) -> tuple:
        return tuple(
            max(0, min(255, c + rng.randint(-variation, variation)))
            for c in base_color
        )
    
    def _create_number_mask(self, number: int, size: int) -> np.ndarray:
        img = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(img)
        
        text = str(number)
        font_size = size // 2
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2 - bbox[0]
        y = (size - text_height) // 2 - bbox[1]
        
        draw.text((x, y), text, fill=255, font=font)
        
        return np.array(img)
    
    def generate_test_image(
        self,
        session_id: str,
        image_number: int,
        dichromism_type: str = None,
        correct_answer: int = None
    ) -> bytes:
        if dichromism_type is None or correct_answer is None:
            config = self.get_test_config(session_id, image_number)
            dichromism_type = config['dichromism_type']
            correct_answer = config['correct_answer']
        
        seed = self._get_seed(session_id, image_number)
        rng = random.Random(seed)
        
        size = self.IMAGE_SIZE
        img = Image.new('RGB', (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        palette = self.COLOR_PALETTES[dichromism_type]
        number_mask = self._create_number_mask(correct_answer, size)
        
        center = size // 2
        radius = (size // 2) - 10
        
        dot_count = rng.randint(self.DOT_COUNT_MIN, self.DOT_COUNT_MAX)
        
        for _ in range(dot_count):
            angle = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0, radius)
            x = int(center + r * np.cos(angle))
            y = int(center + r * np.sin(angle))
            
            dot_size = rng.randint(self.DOT_SIZE_MIN, self.DOT_SIZE_MAX)
            
            if 0 <= x < size and 0 <= y < size and number_mask[y, x] > 128:
                base_color = palette['foreground']
            else:
                base_color = palette['background']
            
            color = self._vary_color(base_color, rng)
            
            draw.ellipse(
                [x - dot_size//2, y - dot_size//2, x + dot_size//2, y + dot_size//2],
                fill=color
            )
        
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([10, 10, size-10, size-10], fill=255)
        
        result = Image.new('RGB', (size, size), (255, 255, 255))
        result.paste(img, mask=mask)
        
        buffer = io.BytesIO()
        result.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()
