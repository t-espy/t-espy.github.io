#!/usr/bin/env python3
"""Playwright check for the agent-coord portfolio card.

Serves this directory and clicks the new home / methodology / Assayer links.
Uses lean-optimizer's Playwright (not a site dependency).

  /home/tespy/lean-optimizer/venv/bin/python e2e_agent_coord_playwright.py
"""
from __future__ import annotations

import http.server
import socket
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "_playwright_shots"


def _serve() -> tuple[threading.Thread, int, http.server.HTTPServer]:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def log_message(self, fmt, *args):  # noqa: ARG002
            return

    httpd = http.server.HTTPServer(("127.0.0.1", port), Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return t, port, httpd


def main() -> int:
    from playwright.sync_api import sync_playwright

    SHOTS.mkdir(exist_ok=True)
    _, port, httpd = _serve()
    base = f"http://127.0.0.1:{port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})

            page.goto(f"{base}/", wait_until="domcontentloaded")
            nav = page.locator(".site-nav a")
            assert nav.count() == 6, nav.count()
            assert page.locator('a[href*="agent-coord.html"]').count() == 0
            assert "github.com/t-espy/agent-coord" not in page.content()
            card = page.locator("#agent-coord")
            card.wait_for()
            assert "Coordination Board for AI Coding Agents" in card.inner_text()
            assert "Private infrastructure; available on request" in card.inner_text()
            assert "not a task runner" in card.inner_text().lower()
            page.screenshot(path=str(SHOTS / "home-card.png"), full_page=True)

            page.locator('#agent-coord a[href="methodology.html#agent-coord-board"]').click()
            page.wait_for_url("**/methodology.html#agent-coord-board")
            board = page.locator("#agent-coord-board")
            board.wait_for()
            assert "fourth place is a coordination board" in board.inner_text()
            page.screenshot(path=str(SHOTS / "methodology-jump.png"), full_page=True)

            page.locator('#agent-coord-board a[href="/#agent-coord"]').click()
            page.wait_for_url("**/#agent-coord")
            page.locator("#agent-coord").wait_for()
            outline = page.evaluate(
                """() => getComputedStyle(document.getElementById('agent-coord')).outlineStyle"""
            )
            assert outline != "none", outline

            page.goto(f"{base}/lean-optimizer.html", wait_until="domcontentloaded")
            page.locator('a[href="/#agent-coord"]').click()
            page.wait_for_url("**/#agent-coord")
            assert page.locator("#agent-coord").is_visible()

            phone = browser.new_page(viewport={"width": 390, "height": 844})
            phone.goto(f"{base}/#agent-coord", wait_until="domcontentloaded")
            phone.locator("#agent-coord").wait_for()
            assert phone.locator(".site-nav a").count() == 6
            phone.screenshot(path=str(SHOTS / "home-card-mobile.png"), full_page=True)
            phone.close()
            browser.close()
    finally:
        httpd.shutdown()
    print("PASS")
    print(f"shots: {SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
