import sys
import os
import pytest
from unittest.mock import MagicMock, patch, ANY

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define a dummy CTk class to allow inheritance without side effects
class DummyCTk:
    def __init__(self, *args, **kwargs):
        pass

    def after(self, ms, func=None, *args):
        pass

    def geometry(self, *args):
        pass

    def wm_state(self, *args):
        pass

    def protocol(self, *args):
        pass

    def configure(self, *args, **kwargs):
        pass

    def title(self, *args):
        pass

    def bind(self, *args):
        pass

    def grid_rowconfigure(self, *args, **kwargs):
        pass

    def grid_columnconfigure(self, *args, **kwargs):
        pass

# Mock customtkinter before importing app
mock_ctk = MagicMock()
mock_ctk.CTk = DummyCTk
sys.modules['customtkinter'] = mock_ctk
sys.modules['tkinter'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Mock submodules in src.ui that might use customtkinter
sys.modules['src.ui.analyzer_tab'] = MagicMock()
sys.modules['src.ui.components'] = MagicMock()
sys.modules['src.ui.utils'] = MagicMock()

from src.ui.app import UnimedPasswordGeneratorApp

def setup_app_mock(mock_init_vars):
    """Helper to set up side effects for _init_vars."""
    def side_effect(self):
        self.vars = {
            "animacao_ativa": MagicMock()
        }
        self.vars["animacao_ativa"].get.return_value = False
    mock_init_vars.side_effect = side_effect

def test_clipboard_clearing_scheduled():
    """Test that clipboard clearing is scheduled after copying."""

    with patch('src.ui.app.pyperclip') as mock_pyperclip:
        # Patch methods called in __init__ to avoid side effects
        # We use autospec=True to ensure arguments match, but here simple patch is enough
        with patch.object(UnimedPasswordGeneratorApp, '_init_vars', autospec=True) as mock_init_vars, \
             patch.object(UnimedPasswordGeneratorApp, 'create_main_widgets'), \
             patch('src.ui.app.SettingsManager'), \
             patch('src.ui.app.PasswordGenerator'):

            # Setup side effect for _init_vars to populate self.vars
            setup_app_mock(mock_init_vars)

            app = UnimedPasswordGeneratorApp()
            app.after = MagicMock() # Mock the after method specifically for verification

            mock_button = MagicMock()
            mock_button.cget.return_value = "Copiar"

            secret_text = "MySecretPass123"

            # Call the method
            app.copy_to_clipboard(secret_text, mock_button)

            # Verify copy was called
            mock_pyperclip.copy.assert_called_with(secret_text)

            # Verify UI feedback (1500ms)
            app.after.assert_any_call(1500, ANY)

            # Verify security clear (60000ms) - This should fail currently
            calls = app.after.call_args_list
            clear_scheduled = False
            for call in calls:
                args, _ = call
                if args and args[0] == 60000:
                    clear_scheduled = True
                    break

            if not clear_scheduled:
                pytest.fail("Security enhancement missing: Clipboard clear not scheduled for 60s")

def test_clear_clipboard_logic():
    """Test the logic that actually clears the clipboard."""

    with patch('src.ui.app.pyperclip') as mock_pyperclip:
        with patch.object(UnimedPasswordGeneratorApp, '_init_vars', autospec=True) as mock_init_vars, \
             patch.object(UnimedPasswordGeneratorApp, 'create_main_widgets'), \
             patch('src.ui.app.SettingsManager'), \
             patch('src.ui.app.PasswordGenerator'):

            setup_app_mock(mock_init_vars)

            app = UnimedPasswordGeneratorApp()

            # Setup mock to return the secret text (simulating it's still there)
            secret_text = "MySecretPass123"
            mock_pyperclip.paste.return_value = secret_text

            # We expect the method to exist
            if not hasattr(app, 'clear_clipboard'):
                pytest.skip("clear_clipboard method not implemented yet")

            app.clear_clipboard(secret_text)

            # It should have cleared it
            mock_pyperclip.copy.assert_called_with("")

    # Test case where clipboard changed
    with patch('src.ui.app.pyperclip') as mock_pyperclip:
        with patch.object(UnimedPasswordGeneratorApp, '_init_vars', autospec=True) as mock_init_vars, \
             patch.object(UnimedPasswordGeneratorApp, 'create_main_widgets'), \
             patch('src.ui.app.SettingsManager'), \
             patch('src.ui.app.PasswordGenerator'):

            setup_app_mock(mock_init_vars)

            app = UnimedPasswordGeneratorApp()

            # Setup mock to return DIFFERENT text
            mock_pyperclip.paste.return_value = "DifferentText"

            if hasattr(app, 'clear_clipboard'):
                app.clear_clipboard("MySecretPass123")

                # It should NOT have cleared it (copy not called with empty string)
                mock_pyperclip.copy.assert_not_called()
