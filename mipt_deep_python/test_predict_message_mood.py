from unittest.mock import Mock, patch

from predict_message_mood import predict_message_mood


class TestPredictMessageMood:
    def test_excellent_rating(self):
        mock_model = Mock()
        mock_model.predict.return_value = 0.9

        with patch("predict_message_mood.SomeModel", return_value=mock_model):
            result = predict_message_mood("Чапаев и пустота")

        assert result == "отл"
        mock_model.predict.assert_called_once_with("Чапаев и пустота")

    def test_normal_rating(self):
        mock_model = Mock()
        mock_model.predict.return_value = 0.85

        with patch("predict_message_mood.SomeModel", return_value=mock_model):
            result = predict_message_mood("Чапаев и пустота", 0.8, 0.99)

        assert result == "норм"
        mock_model.predict.assert_called_once_with("Чапаев и пустота")

    def test_bad_rating(self):
        mock_model = Mock()
        mock_model.predict.return_value = 0.2

        with patch("predict_message_mood.SomeModel", return_value=mock_model):
            result = predict_message_mood("Вулкан")

        assert result == "неуд"
        mock_model.predict.assert_called_once_with("Вулкан")

    def test_custom_thresholds(self):
        test_cases = [
            (0.1, 0.2, 0.9, "неуд"),
            (0.5, 0.2, 0.9, "норм"),
            (0.95, 0.2, 0.9, "отл"),
            (0.0, 0.1, 0.5, "неуд"),
            (0.3, 0.1, 0.5, "норм"),
            (0.6, 0.1, 0.5, "отл"),
        ]

        for prediction, bad_threshold, good_threshold, expected in test_cases:
            mock_model = Mock()
            mock_model.predict.return_value = prediction

            with patch(
                "predict_message_mood.SomeModel",
                return_value=mock_model,
            ):
                result = predict_message_mood(
                    "test",
                    bad_threshold,
                    good_threshold,
                )

            assert result == expected, (
                f"Failed for prediction={prediction}, \
                    thresholds=({bad_threshold}, {good_threshold})"
            )
            mock_model.predict.assert_called_once_with("test")
