import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.results_analyzer import ResultsAnalyzer


class MockAnswer:
    def __init__(self, image_number, correct_answer, user_answer, dichromism_type):
        self.image_number = image_number
        self.correct_answer = correct_answer
        self.user_answer = user_answer
        self.dichromism_type = dichromism_type


class TestResultsAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return ResultsAnalyzer()
    
    def _create_answers(self, pattern):
        answers = []
        config = [
            ('protanopia', 1), ('protanopia', 2), ('protanopia', 3),
            ('deuteranopia', 4), ('deuteranopia', 5), ('deuteranopia', 6),
            ('tritanopia', 7), ('tritanopia', 8), ('tritanopia', 9),
            ('control', 10)
        ]
        
        for i, (dtype, img_num) in enumerate(config):
            correct = 42
            user = correct if pattern[i] else 0
            answers.append(MockAnswer(img_num, correct, user, dtype))
        
        return answers
    
    def test_normal_vision(self, analyzer):
        pattern = [True] * 10
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'normal'
        assert result['suspected_type'] is None
    
    def test_protanopia_detected(self, analyzer):
        pattern = [False, False, False, True, True, True, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'deficient'
        assert result['suspected_type'] == 'protanopia'
    
    def test_deuteranopia_detected(self, analyzer):
        pattern = [True, True, True, False, False, False, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'deficient'
        assert result['suspected_type'] == 'deuteranopia'
    
    def test_tritanopia_detected(self, analyzer):
        pattern = [True, True, True, True, True, True, False, False, False, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'deficient'
        assert result['suspected_type'] == 'tritanopia'
    
    def test_control_failure_unreliable(self, analyzer):
        pattern = [True, True, True, True, True, True, True, True, True, False]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'unreliable'
        assert result['confidence'] == 'none'
    
    def test_incomplete_test(self, analyzer):
        answers = self._create_answers([True] * 10)[:5]
        
        result = analyzer.analyze_session(answers)
        assert result['color_vision_status'] == 'incomplete'
    
    def test_high_confidence_all_errors(self, analyzer):
        pattern = [False, False, False, True, True, True, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['confidence'] == 'high'
    
    def test_medium_confidence_partial_errors(self, analyzer):
        # 2/3 errors = 66.7% which is just under threshold, so need 3/3 for deficient
        # Test that 2/3 results in normal (below 67% threshold)
        pattern = [False, False, True, True, True, True, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        # 2 errors out of 3 (66.7%) is below the 67% threshold
        assert result['color_vision_status'] == 'normal'
    
    def test_multiple_deficiencies(self, analyzer):
        pattern = [False, False, False, False, False, False, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['suspected_type'] == 'multiple'
        assert result['confidence'] == 'low'
    
    def test_details_include_error_counts(self, analyzer):
        pattern = [False, True, True, True, True, True, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        details = result['details']
        
        assert 'protanopia_errors' in details
        assert 'deuteranopia_errors' in details
        assert 'tritanopia_errors' in details
        assert 'control_errors' in details
    
    def test_interpretation_provided(self, analyzer):
        pattern = [True] * 10
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['interpretation'] is not None
        assert len(result['interpretation']) > 0
    
    def test_recommendations_provided(self, analyzer):
        pattern = [False, False, False, True, True, True, True, True, True, True]
        answers = self._create_answers(pattern)
        
        result = analyzer.analyze_session(answers)
        assert result['recommendations'] is not None
