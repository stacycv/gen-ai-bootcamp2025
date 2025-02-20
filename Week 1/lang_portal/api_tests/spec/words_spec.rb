require 'spec_helper'

RSpec.describe 'Words API' do
  describe 'GET /words' do
    context 'with default pagination' do
      before do
        @response = HTTP.get(api_url('/words'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns properly structured JSON' do
        expect(json_response).to include('items', 'pagination')
        expect(json_response['items']).to be_an(Array)
        expect(json_response['pagination']).to include('current_page', 'total_pages', 'per_page')
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

    context 'with custom pagination' do
      before do
        @response = HTTP.get(api_url('/words?page=1&per_page=2'))
      end

      it 'returns correct number of items' do
        expect(json_response['items'].length).to eq(2)
      end

      it 'returns correct pagination info' do
        expect(json_response['pagination']['per_page']).to eq(2)
        expect(json_response['pagination']['current_page']).to eq(1)
      end
    end
  end

  describe 'GET /words/:id' do
    context 'with valid ID' do
      before do
        @response = HTTP.get(api_url('/words/1'))
      end

      it 'returns 200 status code' do
        expect(response.code).to eq(200)
      end

      it 'returns word details' do
        expect(json_response).to include(
          'id',
          'formal_spanish',
          'informal_spanish',
          'english'
        )
      end
    end

    context 'with invalid ID' do
      before do
        @response = HTTP.get(api_url('/words/999999'))
      end

      it 'returns 404 status code' do
        expect(response.code).to eq(404)
      end

      it 'returns error message' do
        expect(json_response).to include('error')
      end
    end
  end
end 