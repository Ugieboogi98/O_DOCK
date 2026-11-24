"""Shared safe diagnostic codes for semantic validation and provider failures."""


class SemanticError(RuntimeError):
    def __init__(self, code, blocked=True):
        self.code, self.blocked = code, blocked
        super().__init__(code)
