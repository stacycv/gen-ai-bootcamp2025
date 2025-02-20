require 'spec_helper'

RSpec.describe 'Dashboard API' do
  describe 'GET /dashboard/quick-stats' do
    before do
      @response = HTTP.get(api_url('/dashboard/quick-stats'))
    end

    it 'returns 200 status code' do
      expect(response.code).to eq(200)
    end

    it 'returns properly structured stats' do
      expect(json_response).to include(
        'total_words_available',
        'total_groups',
        'total_study_sessions',
        'last_study_session_date',
        'overall_accuracy'
      )
    end

    it 'returns numeric values for counts' do
      expect(json_response['total_words_available']).to be_a(Integer)
      expect(json_response['total_groups']).to be_a(Integer)
      expect(json_response['total_study_sessions']).to be_a(Integer)
      expect(json_response['overall_accuracy']).to be_a(Integer)
    end
  end

  describe 'GET /dashboard/study-progress' do
    before do
      @response = HTTP.get(api_url('/dashboard/study-progress'))
    end

    it 'returns 200 status code' do
      expect(response.code).to eq(200)
    end

    it 'returns study progress data' do
      expect(json_response).to include(
        'total_words_studied',
        'total_available_words'
      )
    end
  end

  describe 'GET /dashboard/last-study-session' do
    context 'when study sessions exist' do
      before do
        @response = HTTP.get(api_url('/dashboard/last-study-session'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns last session details' do
        expect(json_response).to include(
          'id',
          'group_id',
          'created_at',
          'study_activity_id',
          'group_name'
        )
      end
    end
  end
end 