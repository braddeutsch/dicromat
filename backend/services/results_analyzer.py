from typing import List, Dict, Any
from models.answer import Answer


class ResultsAnalyzer:
    DICHROMISM_TYPES = ['protanopia', 'deuteranopia', 'tritanopia']
    
    def analyze_session(self, answers: List[Answer]) -> Dict[str, Any]:
        if len(answers) != 10:
            return {
                'color_vision_status': 'incomplete',
                'suspected_type': None,
                'confidence': 'none',
                'details': {},
                'interpretation': 'Test incomplete. Please answer all 10 images.',
                'recommendations': None
            }
        
        answers_by_type = {t: [] for t in self.DICHROMISM_TYPES}
        answers_by_type['control'] = []
        
        for answer in answers:
            if answer.dichromism_type in answers_by_type:
                answers_by_type[answer.dichromism_type].append(answer)
        
        control_answers = answers_by_type.get('control', [])
        control_correct = all(
            a.user_answer == a.correct_answer for a in control_answers
        ) if control_answers else True
        
        if not control_correct:
            return {
                'color_vision_status': 'unreliable',
                'suspected_type': None,
                'confidence': 'none',
                'details': self._calculate_details(answers_by_type),
                'interpretation': 'Test results are unreliable. The control image was answered incorrectly, which may indicate random guessing, visual impairment, or poor viewing conditions.',
                'recommendations': 'Please retake the test in proper lighting conditions, ensuring you can see the screen clearly.'
            }
        
        error_rates = {}
        for dichromism_type in self.DICHROMISM_TYPES:
            type_answers = answers_by_type[dichromism_type]
            if type_answers:
                errors = sum(1 for a in type_answers if a.user_answer != a.correct_answer)
                error_rates[dichromism_type] = errors / len(type_answers)
            else:
                error_rates[dichromism_type] = 0.0
        
        details = self._calculate_details(answers_by_type)
        
        suspected_types = [t for t, rate in error_rates.items() if rate >= 0.67]
        
        if not suspected_types:
            return {
                'color_vision_status': 'normal',
                'suspected_type': None,
                'confidence': 'high' if all(rate <= 0.33 for rate in error_rates.values()) else 'medium',
                'details': details,
                'interpretation': 'Your color vision appears to be normal. You were able to correctly identify numbers across all color combinations tested.',
                'recommendations': 'No further action needed. Your color perception is within normal range.'
            }
        
        if len(suspected_types) == 1:
            suspected = suspected_types[0]
            rate = error_rates[suspected]
            confidence = 'high' if rate == 1.0 else 'medium'
            
            type_names = {
                'protanopia': 'protanopia (red color blindness)',
                'deuteranopia': 'deuteranopia (green color blindness)',
                'tritanopia': 'tritanopia (blue color blindness)'
            }
            
            return {
                'color_vision_status': 'deficient',
                'suspected_type': suspected,
                'confidence': confidence,
                'details': details,
                'interpretation': f'Results suggest {type_names[suspected]}. You had difficulty identifying numbers in {int(rate * 3)} of 3 images designed to detect this condition.',
                'recommendations': 'Consider consulting an eye care professional for comprehensive color vision testing. This screening test is not a medical diagnosis.'
            }
        
        return {
            'color_vision_status': 'deficient',
            'suspected_type': 'multiple',
            'confidence': 'low',
            'details': details,
            'interpretation': f'Results suggest possible color vision deficiency affecting multiple color ranges ({", ".join(suspected_types)}). This pattern is uncommon.',
            'recommendations': 'Please consult an eye care professional for comprehensive color vision testing to determine the specific nature of your color vision.'
        }
    
    def _calculate_details(self, answers_by_type: Dict[str, List[Answer]]) -> Dict[str, int]:
        details = {}
        for dichromism_type in self.DICHROMISM_TYPES + ['control']:
            type_answers = answers_by_type.get(dichromism_type, [])
            errors = sum(1 for a in type_answers if a.user_answer != a.correct_answer)
            details[f'{dichromism_type}_errors'] = errors
        return details
