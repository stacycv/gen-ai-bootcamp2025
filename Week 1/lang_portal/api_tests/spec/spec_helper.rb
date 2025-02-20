require 'rspec'
require 'http'
require 'json'
require 'active_support/all'

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
end

# Helper module for API tests
module ApiHelper
  def api_url(path)
    "http://localhost:8080/api#{path}"
  end

  def json_response
    JSON.parse(response.body)
  end

  def response
    @response
  end
end

RSpec.configure do |config|
  config.include ApiHelper
end 