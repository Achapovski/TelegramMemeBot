import logging


class DebugInfoLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname.upper() in ("DEBUG", "INFO")


class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname.upper() == 'ERROR'


class WarningLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname.upper() == 'WARNING'


class CriticalLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname.upper() == 'CRITICAL'
