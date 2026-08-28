from __future__ import annotations


CLIENT_RUNTIME = r"""
(function () {
    "use strict";

    window.PySkin = window.PySkin || {};

    function connectWebSocket(url) {
        if (!url) {
            return null;
        }

        console.log("[PySkin] Connecting:", url);

        let socket;

        try {
            socket = new WebSocket(url);
        } catch (error) {
            console.error("[PySkin] WebSocket creation failed", error);
            return null;
        }

        socket.addEventListener("open", function () {
            console.log("[PySkin] WebSocket connected");
            window.PySkin.socket = socket;
        });

        socket.addEventListener("close", function () {
            console.log("[PySkin] WebSocket disconnected");
        });

        socket.addEventListener("error", function (error) {
            console.error("[PySkin] WebSocket error", error);
        });

        socket.addEventListener("message", function (event) {
            try {
                const message = JSON.parse(event.data);

                if (
                    window.PySkin &&
                    typeof window.PySkin.onResponse === "function"
                ) {
                    window.PySkin.onResponse(message);
                }
            } catch (error) {
                console.error("[PySkin] Invalid server message", error);
            }
        });

        return socket;
    }

    function sendEvent(componentId, eventName, payload) {
        const message = {
            type: "event",
            id: componentId,
            event: eventName
        };

        if (payload !== undefined) {
            message.payload = payload;
        }

        const socket = window.PySkin.socket;

        if (
            socket &&
            socket.readyState === WebSocket.OPEN
        ) {
            console.log("[PySkin] Sending event:", message);
            socket.send(JSON.stringify(message));
            return;
        }

        console.warn(
            "[PySkin] WebSocket not ready; event not sent:",
            message
        );

        if (
            window.PySkin &&
            typeof window.PySkin.onEvent === "function"
        ) {
            window.PySkin.onEvent(message);
        }
    }

    function handleEvent(event) {
        const target = event.target.closest("[data-pyskin-id]");

        if (!target) {
            return;
        }

        const componentId = target.getAttribute("data-pyskin-id");
        const eventNames = target.getAttribute("data-pyskin-events");

        if (!componentId || !eventNames) {
            return;
        }

        const supportedEvents = eventNames
            .split(",")
            .map(function (name) {
                return name.trim();
            });

        if (supportedEvents.indexOf(event.type) === -1) {
            return;
        }

        let payload;

        if (event.type === "input" || event.type === "change") {
            if ("value" in target) {
                payload = {
                    value: target.value
                };
            }
        }

        sendEvent(componentId, event.type, payload);
    }

    window.PySkin.onEvent = window.PySkin.onEvent || function (message) {
        console.log("[PySkin event]", message);
    };

    window.PySkin.onResponse = window.PySkin.onResponse || function (message) {
        console.log("[PySkin response]", message);

        if (!message || message.type !== "update") {
            return;
        }

        const component = document.querySelector(
            '[data-pyskin-id="' + CSS.escape(message.id) + '"]'
        );

        if (!component || !message.props) {
            return;
        }

        Object.keys(message.props).forEach(function (propName) {
            const value = message.props[propName];

            if (propName === "text") {
                component.textContent = String(value);
                return;
            }

            if (propName === "value") {
                component.value = value;
                return;
            }

            if (propName === "disabled") {
                component.disabled = Boolean(value);
                return;
            }

            if (propName === "class") {
                component.className = String(value);
                return;
            }

            if (propName === "title") {
                component.title = String(value);
                return;
            }

            console.warn(
                "[PySkin] Unsupported reactive prop:",
                propName
            );
        });

        window.PySkin.onUpdate = window.PySkin.onUpdate || function () {};
        window.PySkin.onUpdate(message);
    };

    document.addEventListener("click", handleEvent);
    document.addEventListener("change", handleEvent);

    window.PySkin.socket = connectWebSocket(
        window.PySkin.websocketUrl
    );
})();
"""


def get_client_runtime(websocket_url: str | None = None) -> str:
    """Return the embedded PySkin browser runtime."""

    url = websocket_url or ""

    bootstrap = (
        "<script>\n"
        "window.PySkin = window.PySkin || {};\n"
        f"window.PySkin.websocketUrl = {url!r};\n"
        "</script>\n"
    )

    return bootstrap + CLIENT_RUNTIME
