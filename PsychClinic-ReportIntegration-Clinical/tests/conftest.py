import sys
from unittest.mock import MagicMock

# Patch BEFORE any app.Controller.OpenAi is ever imported
mock_openai = MagicMock()
sys.modules['app.Controller.OpenAi'] = MagicMock(OpenAI=mock_openai)