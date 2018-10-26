from handlers.base import BaseHandler


class APIStatusHandler(BaseHandler):
    """Return server status."""

    async def get(self):
        self.finish({'status': 'ok'})
