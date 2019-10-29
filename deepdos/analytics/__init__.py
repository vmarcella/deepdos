from deepdos.db.analytics_tiny_db import TinyAnalytics


class AnalyticsEngine:
    """
        Temporary class for managing the analytics engine. Will
        expand upon in the near future when analytics become a 
        more serious part of the application.
    """

    def __init__(self):
        self.db = TinyAnalytics()
