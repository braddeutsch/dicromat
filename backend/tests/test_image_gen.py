import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.image_generator import ImageGenerator
from PIL import Image
import io


class TestImageGenerator:
    @pytest.fixture
    def generator(self):
        return ImageGenerator()
    
    def test_generate_image_returns_bytes(self, generator):
        image_bytes = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        assert isinstance(image_bytes, bytes)
        assert len(image_bytes) > 0
    
    def test_generated_image_is_valid_png(self, generator):
        image_bytes = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        img = Image.open(io.BytesIO(image_bytes))
        assert img.format == 'PNG'
        assert img.size == (400, 400)
    
    def test_same_seed_produces_same_image(self, generator):
        image1 = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        image2 = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        assert image1 == image2
    
    def test_different_seed_produces_different_image(self, generator):
        image1 = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        image2 = generator.generate_test_image(
            session_id='test-session-456',
            image_number=1
        )
        assert image1 != image2
    
    def test_different_image_number_produces_different_image(self, generator):
        image1 = generator.generate_test_image(
            session_id='test-session-123',
            image_number=1
        )
        image2 = generator.generate_test_image(
            session_id='test-session-123',
            image_number=2
        )
        assert image1 != image2
    
    def test_get_test_config_returns_valid_config(self, generator):
        config = generator.get_test_config('test-session', 1)
        assert 'dichromism_type' in config
        assert 'correct_answer' in config
        assert config['dichromism_type'] in ['protanopia', 'deuteranopia', 'tritanopia', 'control']
        assert 0 <= config['correct_answer'] <= 99
    
    def test_all_image_numbers_valid(self, generator):
        for i in range(1, 11):
            config = generator.get_test_config('test-session', i)
            image = generator.generate_test_image('test-session', i)
            assert config is not None
            assert image is not None
    
    def test_invalid_image_number_raises(self, generator):
        with pytest.raises(ValueError):
            generator.get_test_config('test-session', 0)
        with pytest.raises(ValueError):
            generator.get_test_config('test-session', 11)
    
    def test_image_number_dichromism_mapping(self, generator):
        for i in range(1, 4):
            config = generator.get_test_config('test-session', i)
            assert config['dichromism_type'] == 'protanopia'
        
        for i in range(4, 7):
            config = generator.get_test_config('test-session', i)
            assert config['dichromism_type'] == 'deuteranopia'
        
        for i in range(7, 10):
            config = generator.get_test_config('test-session', i)
            assert config['dichromism_type'] == 'tritanopia'
        
        config = generator.get_test_config('test-session', 10)
        assert config['dichromism_type'] == 'control'
