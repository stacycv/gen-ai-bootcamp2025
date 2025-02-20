require 'spec_helper'

RSpec.describe 'Groups API' do
  describe 'GET /groups' do
    context 'with default pagination' do
      before do
        @response = HTTP.get(api_url('/groups'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns properly structured JSON' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
        expect(json_response['pagination']).to include('current_page', 'total_pages', 'per_page')
      end

      it 'returns groups with correct attributes' do
        group = json_response['items'].first
        expect(group).to include(
          'id',
          'name',
          'word_count'
        )
      end
    end

    context 'with custom pagination' do
      before do
        @response = HTTP.get(api_url('/groups?page=1&per_page=2'))
      end

      it 'returns correct number of items' do
        expect(json_response['items'].length).to be <= 2
      end
    end
  end

  describe 'GET /groups/:id' do
    context 'with valid ID' do
      before do
        @response = HTTP.get(api_url('/groups/1'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns group details' do
        expect(json_response).to include(
          'id',
          'name',
          'word_count'
        )
      end
    end

    context 'with invalid ID' do
      before do
        @response = HTTP.get(api_url('/groups/999999'))
      end

      it 'returns 404 status code' do
        expect(response.code).to eq(404)
      end
    end
  end

  describe 'GET /groups/:id/words' do
    context 'with valid group ID' do
      before do
        @response = HTTP.get(api_url('/groups/1/words'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated words list' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
      end

      it 'returns words with correct attributes' do
        word = json_response['items'].first
        expect(word).to include(
          'id',
          'formal_spanish',
          'informal_spanish',
          'english'
        )
      end
    end
  end

  describe 'GET /groups/:id/study-sessions' do
    context 'with valid group ID' do
      before do
        @response = HTTP.get(api_url('/groups/1/study-sessions'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated study sessions' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
      end

      it 'returns sessions with correct attributes' do
        if json_response['items'].any?
          session = json_response['items'].first
          expect(session).to include(
            'id',
            'activity_name',
            'start_time',
            'end_time',
            'words_reviewed'
          )
        end
      end
    end
  end
end 