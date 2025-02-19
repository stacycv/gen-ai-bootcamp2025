def test_create_study_session(client):
    # Test missing fields
    response = client.post('/api/study-sessions', json={})
    assert response.status_code == 400
    
    # Test invalid group
    response = client.post('/api/study-sessions', json={
        'group_id': 999,
        'study_activity_id': 1
    })
    assert response.status_code == 404
    
    # Test invalid activity
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 999
    })
    assert response.status_code == 404
    
    # Test successful creation
    response = client.post('/api/study-sessions', json={
        'group_id': 1,
        'study_activity_id': 1
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['group_id'] == 1
    assert data['activity_id'] == 1
    assert 'start_time' in data
    assert 'end_time' in data
    assert 'group_name' in data
    assert 'activity_name' in data 