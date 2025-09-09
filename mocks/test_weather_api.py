from weather_api import get_weather


def test_get_weather(mocker):
    # Mock requests.get to avoid real API calls
    mock_get = mocker.patch("weather_api.requests.get")

    # Set return values for mock
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temp": 20, "condition": "Sunny"}

    # Call function
    result = get_weather("Valby")

    # Assert
    assert result == {"temp": 20, "condition": "Sunny"}
    mock_get.assert_called_once_with("http://api.weather.com/v1/Valby")