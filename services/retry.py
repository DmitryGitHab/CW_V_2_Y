"""Retry с экспоненциальной паузой для нестабильных сетевых вызовов."""

import functools
import logging
import time

logger = logging.getLogger(__name__)


def retry(times: int = 3, base_delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Декоратор: повторяет вызов при исключении из `exceptions`.

    Пауза между попытками растёт экспоненциально: base_delay, base_delay*2,
    base_delay*4, ... Последняя неудачная попытка пробрасывает исключение
    дальше — вызывающий код должен сам решить, что делать при полном отказе.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == times:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        "Попытка %s/%s для %s не удалась (%s), повтор через %.1fs",
                        attempt, times, func.__name__, exc, delay,
                    )
                    time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator
