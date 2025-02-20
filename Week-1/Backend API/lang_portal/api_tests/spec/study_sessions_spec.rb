require 'spec_helper'

RSpec.describe 'Study Sessions API' do
  describe 'POST /study-sessions' do
    let(:valid_params) do
      {
        group_id: 1,
        study_activity_id: 1
      }
    end

    context 'with valid parameters' do
      before do
        @response = HTTP.post(
          api_url('/study-sessions'),
          json: valid_params
        )
      end

      it 'returns 201 status code' do
        expect(response.code).to eq(201)
      end

      it 'returns created study session' do
        expect(json_response).to include(
          'id',
          'group_id',
          'study_activity_id',
          'created_at'
        )
      end
    end

    context 'with invalid group_id' do
      before do
        @response = HTTP.post(
          api_url('/study-sessions'),
          json: valid_params.merge(group_id: 99999)
        )
      end

      it 'returns 404 status code' do
        expect(response.code).to eq(404)
      end

      it 'returns error message' do
        expect(json_response['error']).to include('group not found')
      end
    end
  end

  describe 'GET /study-sessions' do
    before do
      @response = HTTP.get(api_url('/study-sessions'))
    end

    it 'returns 200 status code' do
      expect(response.code).to eq(200)
    end

    it 'returns paginated list' do
      expect(json_response).to include('items', 'pagination')
      expect(json_response['items']).to be_an(Array)
    end

    it 'returns sessions with correct attributes' do
      if json_response['items'].any?
        session = json_response['items'].first
        expect(session).to include(
          'id',
          'group_id',
          'created_at',
          'study_activity_id'
        )
      end
    end
  end

  describe 'GET /study-sessions/:id/words' do
    context 'with valid session ID' do
      before do
        # First create a session
        create_response = HTTP.post(
          api_url('/study-sessions'),
          json: { group_id: 1, study_activity_id: 1 }
        )
        session = JSON.parse(create_response.body)
        @session_id = session['id']
        
        # Then get its words
        @response = HTTP.get(api_url("/study-sessions/#{@session_id}/words"))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated words list' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
      end
    end
  end

  describe 'POST /study-sessions/:id/words/:word_id/review' do
    before do
      # First create a session
      create_response = HTTP.post(
        api_url('/study-sessions'),
        json: { group_id: 1, study_activity_id: 1 }
      )
      session = JSON.parse(create_response.body)
      @session_id = session['id']
    end

    context 'with valid parameters' do
      before do
        @response = HTTP.post(
          api_url("/study-sessions/#{@session_id}/words/1/review"),
          json: { correct: true }
        )
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns success response' do
        expect(json_response).to include(
          'success' => true,
          'word_id' => 1,
          'study_session_id' => @session_id,
          'correct' => true
        )
      end
    end

    context 'with invalid word_id' do
      before do
        @response = HTTP.post(
          api_url("/study-sessions/#{@session_id}/words/999999/review"),
          json: { correct: true }
        )
      end

      it 'returns 404 status code' do
        expect(response.code).to eq(404)
      end

      it 'returns error message' do
        expect(json_response['error']).to include('word not found')
      end
    end
  end
end 