class SomeModel:
    def predict(self, message: str) -> float:
        return min(len(message) / 100, 1.0)  # заглушка

    def __str__(self) -> str:
        return "SomeModel()"


def predict_message_mood(
    message: str,
    bad_threshold: float = 0.3,
    good_threshold: float = 0.8,
) -> str:
    model = SomeModel()
    prediction = model.predict(message)

    if prediction < bad_threshold:
        return "неуд"
    if prediction > good_threshold:
        return "отл"
    return "норм"
