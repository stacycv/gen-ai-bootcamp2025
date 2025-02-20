require 'spec_helper'

RSpec.describe 'Study Activities API' do
  describe 'GET /study-activities/:id' do
    context 'with valid ID' do
      before do
        @response = HTTP.get(api_url('/study-activities/1'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns activity details' do
        expect(json_response).to include(
          'id',
          'name',
          'description',
          'thumbnail_url',
          'launch_url'
        )
      end
    end

    context 'with invalid ID' do
      before do
        @response = HTTP.get(api_url('/study-activities/999999'))
      end

      it 'returns 404 status code' do
        expect(response.code).to eq(404)
      end
    end
  end

  describe 'GET /study-activities/:id/study-sessions' do
    context 'with valid activity ID' do
      before do
        @response = HTTP.get(api_url('/study-activities/1/study-sessions'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated sessions list' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
      end

      it 'returns sessions with correct attributes' do
        if json_response['items'].any?
          session = json_response['items'].first
          expect(session).to include(
            'id',
            'activity_name',
            'activity_description',
            'group_name',
            'start_time',
            'end_time',
            'words_reviewed',
            'success_rate'
          )
        end
      end
    end
  end
end 