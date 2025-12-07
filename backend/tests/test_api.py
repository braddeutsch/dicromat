import json
import pytest


class TestStartEndpoint:
    def test_start_test_creates_session(self, client):
        response = client.post('/api/test/start', json={})
        assert response.status_code == 201
        data = response.get_json()
        assert 'session_id' in data
        assert 'created_at' in data
        assert data['total_images'] == 10
    
    def test_start_test_with_metadata(self, client):
        metadata = {'age_range': '25-34', 'gender': 'prefer_not_to_say'}
        response = client.post('/api/test/start', json={'metadata': metadata})
        assert response.status_code == 201
    
    def test_start_test_no_body(self, client):
        response = client.post('/api/test/start')
        assert response.status_code == 201


class TestImageEndpoint:
    def test_get_image_returns_png(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.get(f'/api/test/{session_id}/image/1')
        assert response.status_code == 200
        assert response.content_type == 'image/png'
        assert len(response.data) > 0
    
    def test_get_image_invalid_number(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.get(f'/api/test/{session_id}/image/0')
        assert response.status_code == 400
        
        response = client.get(f'/api/test/{session_id}/image/11')
        assert response.status_code == 400
    
    def test_get_image_invalid_session(self, client):
        response = client.get('/api/test/invalid-session-id/image/1')
        assert response.status_code == 404
    
    def test_image_has_dichromism_type_header(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.get(f'/api/test/{session_id}/image/1')
        assert 'X-Dichromism-Type' in response.headers


class TestAnswerEndpoint:
    def test_submit_answer(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': 42}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['image_number'] == 1
        assert data['next_image'] == 2
        assert data['is_complete'] is False
    
    def test_submit_answer_null(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': None}
        )
        assert response.status_code == 201
    
    def test_duplicate_answer_rejected(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': 42}
        )
        
        response = client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': 43}
        )
        assert response.status_code == 409
    
    def test_invalid_answer_rejected(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        response = client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': 100}
        )
        assert response.status_code == 400
    
    def test_complete_test(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        for i in range(1, 10):
            client.post(
                f'/api/test/{session_id}/answer',
                json={'image_number': i, 'user_answer': 42}
            )
        
        response = client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 10, 'user_answer': 42}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['is_complete'] is True
        assert data['results_available'] is True
        assert data['next_image'] is None


class TestResultsEndpoint:
    def _complete_test(self, client, answers=None):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        for i in range(1, 11):
            answer = answers[i-1] if answers else 42
            client.post(
                f'/api/test/{session_id}/answer',
                json={'image_number': i, 'user_answer': answer}
            )
        
        return session_id
    
    def test_get_results_complete_test(self, client):
        session_id = self._complete_test(client)
        
        response = client.get(f'/api/test/{session_id}/results')
        assert response.status_code == 200
        data = response.get_json()
        assert 'session_id' in data
        assert 'total_correct' in data
        assert 'analysis' in data
        assert 'interpretation' in data
        assert 'answers' in data
        assert len(data['answers']) == 10
    
    def test_get_results_incomplete_test(self, client):
        start_response = client.post('/api/test/start', json={})
        session_id = start_response.get_json()['session_id']
        
        client.post(
            f'/api/test/{session_id}/answer',
            json={'image_number': 1, 'user_answer': 42}
        )
        
        response = client.get(f'/api/test/{session_id}/results')
        assert response.status_code == 409
    
    def test_results_include_analysis(self, client):
        session_id = self._complete_test(client)
        
        response = client.get(f'/api/test/{session_id}/results')
        data = response.get_json()
        
        analysis = data['analysis']
        assert 'color_vision_status' in analysis
        assert 'suspected_type' in analysis
        assert 'confidence' in analysis
        assert 'details' in analysis
