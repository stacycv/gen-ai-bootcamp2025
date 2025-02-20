require 'spec_helper'

RSpec.describe 'Reset API' do
  describe 'POST /reset-history' do
    before do
      @response = HTTP.post(api_url('/reset-history'))
    end

    it 'returns 200 status code' do
      expect(response.code).to eq(200)
    end

    it 'returns success message' do
      expect(json_response).to include(
        'success' => true,
        'message' => 'Study history has been reset'
      )
    end

    it 'actually removes study history' do
      stats_response = HTTP.get(api_url('/dashboard/quick-stats'))
      stats = JSON.parse(stats_response.body)
      expect(stats['total_study_sessions']).to eq(0)
    end
  end

  describe 'POST /full-reset' do
    before do
      @response = HTTP.post(api_url('/full-reset'))
    end

    it 'returns 200 status code' do
      expect(response.code).to eq(200)
    end

    it 'returns success message' do
      expect(json_response).to include(
        'success' => true,
        'message' => 'All data has been reset'
      )
    end

    it 'actually removes all data' do
      stats_response = HTTP.get(api_url('/dashboard/quick-stats'))
      stats = JSON.parse(stats_response.body)
      expect(stats['total_words_available']).to eq(0)
      expect(stats['total_groups']).to eq(0)
      expect(stats['total_study_sessions']).to eq(0)
    end
  end
end 