import inspect
from functools import wraps

from utils.report_logger import ReportLogger


class attachment_type:
    TEXT = "TEXT"
    PNG = "PNG"


def _safe_format(template, func, args, kwargs):
    try:
        bound = inspect.signature(func).bind_partial(*args, **kwargs)
        bound.apply_defaults()
        return str(template).format(**bound.arguments)
    except Exception:
        return str(template)


class _StepContext:
    def __init__(self, title):
        self.title = str(title)

    def __enter__(self):
        ReportLogger.log_step(f"START: {self.title}")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            ReportLogger.log_step(f"END: {self.title}")
        else:
            ReportLogger.log_step(f"ERROR: {self.title} -> {exc}")
        return False

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            formatted_title = _safe_format(self.title, func, args, kwargs)
            with _StepContext(formatted_title):
                return func(*args, **kwargs)

        return wrapper


def step(title):
    return _StepContext(title)


def attach(body, name=None, attachment_type=attachment_type.TEXT):
    preview = body if isinstance(body, str) else f"<{type(body).__name__}>"
    ReportLogger.log_attachment(name=name or "attachment", attachment_type=attachment_type, preview=preview)
