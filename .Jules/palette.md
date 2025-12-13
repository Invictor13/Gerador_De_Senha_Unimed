## 2024-05-22 - [Async UI Operations in Tkinter]
**Learning:** Tkinter UI updates must happen on the main thread. When using `threading` for background tasks (like network requests), use `widget.after(0, callback)` to schedule UI updates safely back on the main thread.
**Action:** Always wrap UI update callbacks in `self.after(0, ...)` when calling from a background thread.
