from __future__ import annotations


CLIENT_RUNTIME = r"""
(function () {
    "use strict";

    window.PyLage = window.PyLage || {};
    window.PyLage._propMetaCache = Object.create(null);

    const boundEventTypes = new Set(["click", "input", "change", "submit"]);
    let reconnectDelay = 1000;
    const maxReconnectDelay = 16000;

    function encodeMessagePack(value) {
        const chunks = [];

        function pushByte(value) { chunks.push(value & 255); }
        function pushBytes(bytes) { for (const byte of bytes) chunks.push(byte); }
        function pushU16(value) { pushByte(value >>> 8); pushByte(value); }
        function pushU32(value) { pushByte(value >>> 24); pushByte(value >>> 16); pushByte(value >>> 8); pushByte(value); }
        function pushF64(value) {
            const buffer = new ArrayBuffer(8);
            new DataView(buffer).setFloat64(0, value, false);
            pushBytes(new Uint8Array(buffer));
        }

        const textEncoder = new TextEncoder();

        function encode(value) {
            if (value === null || value === undefined) {
                pushByte(192);
                return;
            }
            if (typeof value === "boolean") {
                pushByte(value ? 195 : 194);
                return;
            }
            if (typeof value === "number") {
                if (Number.isInteger(value) && Number.isSafeInteger(value)) {
                    if (value >= 0 && value <= 127) { pushByte(value); return; }
                    if (value >= -32 && value < 0) { pushByte(256 + value); return; }
                    if (value >= 0 && value <= 255) { pushByte(204); pushByte(value); return; }
                    if (value >= 0 && value <= 65535) { pushByte(205); pushU16(value); return; }
                    if (value >= 0 && value <= 4294967295) { pushByte(206); pushU32(value); return; }
                    if (value >= -128 && value <= 127) { pushByte(208); pushByte(value); return; }
                    if (value >= -32768 && value <= 32767) { pushByte(209); pushU16(value); return; }
                    if (value >= -2147483648 && value <= 2147483647) { pushByte(210); pushU32(value); return; }
                }
                pushByte(203);
                pushF64(value);
                return;
            }
            if (typeof value === "string") {
                const bytes = textEncoder.encode(value);
                const length = bytes.length;
                if (length < 32) { pushByte(160 | length); }
                else if (length <= 255) { pushByte(217); pushByte(length); }
                else if (length <= 65535) { pushByte(218); pushU16(length); }
                else { pushByte(219); pushU32(length); }
                pushBytes(bytes);
                return;
            }
            if (Array.isArray(value)) {
                const length = value.length;
                if (length < 16) { pushByte(144 | length); }
                else if (length <= 65535) { pushByte(220); pushU16(length); }
                else { pushByte(221); pushU32(length); }
                for (const item of value) encode(item);
                return;
            }
            if (typeof value === "object") {
                const keys = Object.keys(value);
                const length = keys.length;
                if (length < 16) { pushByte(128 | length); }
                else if (length <= 65535) { pushByte(222); pushU16(length); }
                else { pushByte(223); pushU32(length); }
                for (const key of keys) { encode(key); encode(value[key]); }
                return;
            }
            throw new TypeError("[PyLage] Unsupported MessagePack value.");
        }

        encode(value);
        return new Uint8Array(chunks).buffer;
    }

    function decodeMessagePack(data) {
        const bytes = data instanceof Uint8Array ? data : new Uint8Array(data);
        const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
        const decoder = new TextDecoder();
        let offset = 0;

        function u8() { return view.getUint8(offset++); }
        function u16() { const v = view.getUint16(offset, false); offset += 2; return v; }
        function u32() { const v = view.getUint32(offset, false); offset += 4; return v; }
        function i8() { return view.getInt8(offset++); }
        function i16() { const v = view.getInt16(offset, false); offset += 2; return v; }
        function i32() { const v = view.getInt32(offset, false); offset += 4; return v; }
        function f32() { const v = view.getFloat32(offset, false); offset += 4; return v; }
        function f64() { const v = view.getFloat64(offset, false); offset += 8; return v; }
        function bytesRead(length) { const v = bytes.subarray(offset, offset + length); offset += length; return v; }
        function text(length) { return decoder.decode(bytesRead(length)); }
        function u64() { return u32() * 4294967296 + u32(); }
        function i64() { return i32() * 4294967296 + u32(); }

        function value() {
            const p = u8();
            if (p <= 127) return p;
            if (p >= 224) return p - 256;
            if (p >= 160 && p <= 191) return text(p & 31);
            if (p >= 144 && p <= 159) {
                const a = [];
                for (let i = 0; i < (p & 15); i++) a.push(value());
                return a;
            }
            if (p >= 128 && p <= 143) {
                const o = {};
                for (let i = 0; i < (p & 15); i++) o[value()] = value();
                return o;
            }
            switch (p) {
                case 192: return null;
                case 194: return false;
                case 195: return true;
                case 202: return f32();
                case 203: return f64();
                case 204: return u8();
                case 205: return u16();
                case 206: return u32();
                case 207: return u64();
                case 208: return i8();
                case 209: return i16();
                case 210: return i32();
                case 211: return i64();
                case 196: return bytesRead(u8());
                case 197: return bytesRead(u16());
                case 198: return bytesRead(u32());
                case 217: return text(u8());
                case 218: return text(u16());
                case 219: return text(u32());
                case 220: { const a=[]; const n=u16(); for(let i=0;i<n;i++) a.push(value()); return a; }
                case 221: { const a=[]; const n=u32(); for(let i=0;i<n;i++) a.push(value()); return a; }
                case 222: { const o={}; const n=u16(); for(let i=0;i<n;i++) o[value()]=value(); return o; }
                case 223: { const o={}; const n=u32(); for(let i=0;i<n;i++) o[value()]=value(); return o; }
                default: throw new Error("[PyLage] Unsupported MessagePack type: " + p);
            }
        }

        return value();
    }

    function ensureEventTypeBound(eventType) {
        if (!eventType || boundEventTypes.has(eventType)) {
            return;
        }
        boundEventTypes.add(eventType);
        document.addEventListener(eventType, handleEvent, true);
    }

    function scanAndBindEvents(rootElement) {
        const root = rootElement || document;
        const elements = root.querySelectorAll ? root.querySelectorAll("[data-pylage-events]") : [];
        for (let i = 0; i < elements.length; i++) {
            const eventsAttr = elements[i].getAttribute("data-pylage-events");
            if (eventsAttr) {
                const parts = eventsAttr.split(",");
                for (let j = 0; j < parts.length; j++) {
                    const trimmed = parts[j].trim();
                    if (trimmed) {
                        ensureEventTypeBound(trimmed);
                    }
                }
            }
        }
    }

    function sessionWebSocketUrl(baseUrl) {
        if (!baseUrl) {
            return baseUrl;
        }

        const token = window.PyLage && window.PyLage.sessionToken;
        if (!token) {
            return baseUrl;
        }

        const separator = baseUrl.indexOf("?") === -1 ? "?" : "&";
        return baseUrl + separator + "session=" + encodeURIComponent(token);
    }

    function redactSessionToken(url) {
        if (!url) {
            return url;
        }
        return url.replace(/([?&]session=)[^&#]*/i, "$1[redacted]");
    }

    function scheduleReconnect(baseUrl) {
        if (!baseUrl) {
            return;
        }
        setTimeout(function () {
            const reconnectUrl = sessionWebSocketUrl(baseUrl);
            console.log("[PyLage] Attempting reconnect to:", redactSessionToken(reconnectUrl));
            connectWebSocket(baseUrl);
            reconnectDelay = Math.min(reconnectDelay * 1.5, maxReconnectDelay);
        }, reconnectDelay);
    }

    function connectWebSocket(baseUrl) {
        if (!baseUrl) {
            return null;
        }

        const url = sessionWebSocketUrl(baseUrl);
        console.log("[PyLage] Connecting:", redactSessionToken(url));

        let socket;

        try {
            socket = new WebSocket(url);
            socket.binaryType = "arraybuffer";
        } catch (error) {
            console.error("[PyLage] WebSocket creation failed", error);
            scheduleReconnect(baseUrl);
            return null;
        }

        socket.addEventListener("open", function () {
            console.log("[PyLage] WebSocket connected");
            reconnectDelay = 1000;
            window.PyLage.socket = socket;
            if (typeof window.PyLage.onConnectionChange === "function") {
                window.PyLage.onConnectionChange(true);
            }
        });

        socket.addEventListener("close", function () {
            console.log("[PyLage] WebSocket disconnected");
            if (typeof window.PyLage.onConnectionChange === "function") {
                window.PyLage.onConnectionChange(false);
            }
            scheduleReconnect(baseUrl);
        });

        socket.addEventListener("error", function (error) {
            console.error("[PyLage] WebSocket error", error);
        });

        socket.addEventListener("message", function (event) {
            try {
                const message = typeof event.data === "string" ? JSON.parse(event.data) : decodeMessagePack(event.data);

                if (
                    message &&
                    message.type === "session" &&
                    message.token &&
                    window.PyLage
                ) {
                    window.PyLage.sessionToken = message.token;
                }

                if (
                    window.PyLage &&
                    typeof window.PyLage.onResponse === "function"
                ) {
                    window.PyLage.onResponse(message);
                }
            } catch (error) {
                console.error("[PyLage] Invalid server message", error);
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

        const socket = window.PyLage.socket;

        if (
            socket &&
            socket.readyState === WebSocket.OPEN
        ) {
            console.log("[PyLage] Sending event:", message);
            socket.send(encodeMessagePack(message));
            return;
        }

        console.warn(
            "[PyLage] WebSocket not ready; event not sent:",
            message
        );

        if (
            window.PyLage &&
            typeof window.PyLage.onEvent === "function"
        ) {
            window.PyLage.onEvent(message);
        }
    }


    function normalizePath(path) {
        if (!path) {
            return "/";
        }
        var normalized = String(path);
        if (normalized.charAt(0) !== "/") {
            normalized = "/" + normalized;
        }
        if (normalized.length > 1 && normalized.charAt(normalized.length - 1) === "/") {
            normalized = normalized.slice(0, -1);
        }
        return normalized;
    }
    function sendNavigate(path) {
        var message = {
            type: "navigate",
            path: normalizePath(path)
        };
        var socket = window.PyLage.socket;
        if (
            socket &&
            socket.readyState === WebSocket.OPEN
        ) {
            console.log("[PyLage] Sending navigate:", message);
            socket.send(encodeMessagePack(message));
            return;
        }
        console.warn(
            "[PyLage] WebSocket not ready; navigate not sent:",
            message
        );
        if (
            window.PyLage &&
            typeof window.PyLage.onEvent === "function"
        ) {
            window.PyLage.onEvent(message);
        }
    }
    function navigate(path, options) {
        var normalized = normalizePath(path);
        var opts = options || {};
        var replace = !!opts.replace;
        if (replace) {
            window.history.replaceState({ pylage: true, path: normalized }, "", normalized);
        } else {
            window.history.pushState({ pylage: true, path: normalized }, "", normalized);
        }
        sendNavigate(normalized);
    }
    window.PyLage.navigate = navigate;
    window.addEventListener("popstate", function (event) {
        var path = (event.state && event.state.path) || window.location.pathname || "/";
        sendNavigate(path);
    });

    function handleEvent(event) {
        let target = event.target;

        while (target && target !== document) {
            if (
                target.getAttribute &&
                target.getAttribute("data-pylage-id")
            ) {
                const eventNames = target.getAttribute(
                    "data-pylage-events"
                );

                if (eventNames) {
                    const supportedEvents = eventNames
                        .split(",")
                        .map(function (name) {
                            return name.trim();
                        });

                    if (
                        supportedEvents.indexOf(event.type) !== -1
                    ) {
                        break;
                    }
                }
            }

            target = target.parentElement;
        }

        if (!target || target === document) {
            return;
        }

        const componentId = target.getAttribute("data-pylage-id");
        const eventNames = target.getAttribute("data-pylage-events");

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

        if (event.type === "submit") {
            event.preventDefault();

            payload = {
                values: Object.fromEntries(
                    new FormData(target).entries()
                )
            };
        } else if (event.type === "input" || event.type === "change") {
            payload = {};

            const payloadTarget = event.target;

            if ("value" in payloadTarget) {
                payload.value = payloadTarget.value;
            }

            if ("checked" in payloadTarget) {
                payload.checked = Boolean(payloadTarget.checked);
            }

            if ("selectedIndex" in payloadTarget) {
                payload.selectedIndex = payloadTarget.selectedIndex;
            }

            if (
                payloadTarget instanceof HTMLSelectElement &&
                payloadTarget.multiple
            ) {
                payload.selectedOptions = Array.from(
                    payloadTarget.selectedOptions
                ).map(function (option) {
                    return {
                        value: option.value,
                        text: option.text
                    };
                });
            }
        }

        sendEvent(componentId, event.type, payload);
    }

    window.PyLage.onEvent = window.PyLage.onEvent || function (message) {
        console.log("[PyLage event]", message);
    };

    window.PyLage.onResponse = window.PyLage.onResponse || function (message) {
        console.log("[PyLage response]", message);

        if (!message) {
            return;
        }

        if (message.type === "response") {
            if (!message.ok) {
                console.error("[PyLage] Server error:", message.error);
                if (typeof window.PyLage.onError === "function") {
                    window.PyLage.onError(message.error);
                }
            }
            return;
        }

        if (message.type === "tree_move") {
            if (
                !message.component_id ||
                !message.old_parent_id ||
                !message.new_parent_id
            ) {
                return;
            }

            const component = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.component_id) +
                '"]'
            );

            const newParent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.new_parent_id) +
                '"]'
            );

            if (!component || !newParent) {
                return;
            }

            newParent.appendChild(component);

            return;
        }

        /*
         * Build DOM from renderer-produced HTML when available.
         *
         * The initial page is rendered by HTMLRenderer on the server.
         * Dynamic tree mutations must use the same renderer contract,
         * otherwise custom components such as Table/DataFrame/Form/Dialog
         * degrade into their raw registry tag.
         *
         * ``item.html`` may contain multiple top-level nodes. DataFrame,
         * for example, emits a <style> node followed by its component root.
         */
        function createRenderedNodes(item) {
            if (
                !item ||
                !item.id ||
                typeof item.html !== "string"
            ) {
                return null;
            }

            const template = document.createElement("template");

            template.innerHTML = item.html.trim();

            const nodes = Array.from(
                template.content.childNodes
            );

            if (!nodes.length) {
                return null;
            }

            let rootElement = null;

            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];

                if (
                    node.nodeType === 1 &&
                    node.getAttribute &&
                    node.getAttribute("data-pylage-id") === item.id
                ) {
                    rootElement = node;
                    break;
                }
            }

            if (!rootElement) {
                return null;
            }

            /*
             * Renderer output must contain the component's real root.
             * Keep all top-level nodes because custom renderers may emit
             * support nodes such as <style> before that root.
             */
            return nodes;
        }

        function createTreeNode(item) {
            if (!item || !item.id) {
                return null;
            }

            /*
             * Preferred path: exact HTMLRenderer output.
             */
            const renderedNodes = createRenderedNodes(item);

            if (renderedNodes) {
                return renderedNodes;
            }

            /*
             * Compatibility path for older payloads that do not contain
             * renderer HTML.
             */
            const element = document.createElement(
                item.tag || "div"
            );

            element.setAttribute(
                "data-pylage-id",
                item.id
            );

            if (item.events) {
                element.setAttribute(
                    "data-pylage-events",
                    item.events
                );
            }

            const props = item.props || {};

            Object.keys(props).forEach(function (name) {
                const value = props[name];

                if (name === "text") {
                    element.textContent =
                        value === null || value === undefined
                            ? ""
                            : String(value);
                    return;
                }

                if (name === "style") {
                    return;
                }

                if (value !== null && value !== undefined) {
                    element.setAttribute(
                        name,
                        String(value)
                    );
                }
            });

            const attrs = item.attrs || {};

            Object.keys(attrs).forEach(function (name) {
                const value = attrs[name];

                if (
                    value === null ||
                    value === undefined
                ) {
                    return;
                }

                if (value === true) {
                    element.setAttribute(
                        name,
                        ""
                    );
                    return;
                }

                element.setAttribute(
                    name,
                    String(value)
                );
            });

            if (item.style) {
                element.setAttribute(
                    "style",
                    String(item.style)
                );
            }

            const children = item.children || [];

            if (Array.isArray(children)) {
                children.forEach(function (child) {
                    const childNodes = createTreeNode(child);

                    if (!childNodes) {
                        return;
                    }

                    /*
                     * A normal fallback component produces one node.
                     * Renderer HTML may produce multiple top-level nodes.
                     */
                    if (Array.isArray(childNodes)) {
                        childNodes.forEach(function (childNode) {
                            element.appendChild(childNode);
                        });
                    } else {
                        element.appendChild(childNodes);
                    }
                });
            }

            return element;
        }

        function insertTreeNodes(parent, item, beforeNode) {
            const nodes = createTreeNode(item);

            if (!nodes) {
                return false;
            }

            if (Array.isArray(nodes)) {
                nodes.forEach(function (node) {
                    if (beforeNode) {
                        parent.insertBefore(
                            node,
                            beforeNode
                        );
                    } else {
                        parent.appendChild(node);
                    }
                });

                return true;
            }

            if (beforeNode) {
                parent.insertBefore(
                    nodes,
                    beforeNode
                );
            } else {
                parent.appendChild(nodes);
            }

            return true;
        }

        if (message.type === "tree_add") {
            const parent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.parent_id) +
                '"]'
            );

            if (
                !parent ||
                !Array.isArray(message.components)
            ) {
                return;
            }

            /*
             * Preserve the protocol's insertion index.
             *
             * The index is evaluated before each insertion, matching the
             * existing behavior where multiple components are inserted
             * in protocol order at the requested position.
             */
            message.components.forEach(function (item) {
                const beforeNode =
                    typeof message.index === "number" &&
                    message.index >= 0 &&
                    message.index < parent.children.length
                        ? parent.children[message.index]
                        : null;

                insertTreeNodes(
                    parent,
                    item,
                    beforeNode
                );
            });

            /*
             * Renderer-produced nodes already carry their event metadata
             * in the rendered HTML. Event handling is delegated from
             * document, so no per-node listener registration is required.
             */
            scanAndBindEvents(parent);

            return;
        }

        if (message.type === "tree_remove") {
            if (!Array.isArray(message.component_ids)) {
                return;
            }

            message.component_ids.forEach(function (componentId) {
                if (!componentId) {
                    return;
                }

                const component = document.querySelector(
                    '[data-pylage-id="' +
                    CSS.escape(componentId) +
                    '"]'
                );

                if (component) {
                    component.remove();
                }
            });

            return;
        }

        if (message.type === "tree_clear") {
            const parent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.parent_id) +
                '"]'
            );

            if (
                !parent ||
                !Array.isArray(message.component_ids)
            ) {
                return;
            }

            const componentIds = new Set(
                message.component_ids
            );

            Array.from(parent.children).forEach(function (child) {
                const componentId = child.getAttribute(
                    "data-pylage-id"
                );

                if (componentIds.has(componentId)) {
                    parent.removeChild(child);
                }
            });

            return;
        }

        if (message.type === "tree_set_children") {
            const parent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.parent_id) +
                '"]'
            );

            if (
                !parent ||
                !Array.isArray(message.children)
            ) {
                return;
            }

            while (parent.firstChild) {
                parent.removeChild(
                    parent.firstChild
                );
            }

            message.children.forEach(function (item) {
                insertTreeNodes(
                    parent,
                    item,
                    null
                );
            });

            scanAndBindEvents(parent);

            return;
        }

        if (message.type === "tree_replace") {
            const oldComponent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.old_component_id) +
                '"]'
            );

            if (
                !oldComponent ||
                !message.new_component
            ) {
                return;
            }

            const item = message.new_component;

            if (!item.id) {
                return;
            }

            const parent = oldComponent.parentNode;

            if (!parent) {
                return;
            }

            const replacementNodes = createTreeNode(item);

            if (!replacementNodes) {
                return;
            }

            if (Array.isArray(replacementNodes)) {
                replacementNodes.forEach(function (node) {
                    parent.insertBefore(
                        node,
                        oldComponent
                    );
                });
            } else {
                parent.insertBefore(
                    replacementNodes,
                    oldComponent
                );
            }

            oldComponent.remove();

            scanAndBindEvents(parent);

            return;
        }

        if (message.type === "theme_update") {
            if (typeof message.css !== "string") {
                return;
            }

            const themeStyle = document.querySelector(
                'style[data-pylage-theme="true"]'
            );

            if (themeStyle === null) {
                return;
            }

            themeStyle.textContent = ':root{' + message.css + '}';
            return;
        }

        if (message.type !== "update") {
            return;
        }

        const component = document.querySelector(
            '[data-pylage-id="' + CSS.escape(message.id) + '"]'
        );

        if (!component) {
            return;
        }

        const incomingPropMeta = message.prop_meta || {};
        const componentPropMeta =
            window.PyLage._propMetaCache[message.id] || Object.create(null);

        Object.keys(incomingPropMeta).forEach(function (propName) {
            componentPropMeta[propName] = incomingPropMeta[propName];
        });

        window.PyLage._propMetaCache[message.id] = componentPropMeta;
        const propMeta = componentPropMeta;

          // Remove props that disappeared from the component snapshot.
          const removeProps = Array.isArray(message.remove_props)
              ? message.remove_props
              : [];

          removeProps.forEach(function (propName) {
              const meta = propMeta[propName] || {};
              const htmlName = meta.html_name || propName;

              component.removeAttribute(htmlName);

              if (htmlName in component) {
                  try {
                      if (meta.kind === "boolean") {
                          component[htmlName] = false;
                      } else if (meta.kind === "text") {
                          component[htmlName] = "";
                      } else {
                          component[htmlName] = null;
                      }
                  } catch (error) {
                      console.warn(
                          "[PyLage] Failed to clear removed DOM property:",
                          htmlName,
                          error
                      );
                  }
              }
          });

          if (!message.props) {
              window.PyLage.onUpdate =
                  window.PyLage.onUpdate || function () {};
              window.PyLage.onUpdate(message);
              return;
          }

          Object.keys(message.props).forEach(function (propName) {
              const value = message.props[propName];
              const meta = propMeta[propName] || {};
              const kind = meta.kind || "attribute";
              const htmlName = meta.html_name || propName;

              if (kind === "text") {
                  component.textContent =
                      value === null || value === undefined
                          ? ""
                          : String(value);
                  return;
              }

              if (kind === "boolean") {
                  const logicalValue = Boolean(value);
                  const booleanValue =
                      meta.boolean_mode === "inverse"
                          ? !logicalValue
                          : logicalValue;

                  if (htmlName in component) {
                      try {
                          component[htmlName] = booleanValue;
                      } catch (error) {
                          console.warn(
                              "[PyLage] Boolean DOM property update failed:",
                              htmlName,
                              error
                          );
                      }
                  }

                  if (booleanValue) {
                      component.setAttribute(htmlName, "");
                  } else {
                      component.removeAttribute(htmlName);
                  }

                  return;
              }

              if (htmlName === 'style') {
                  if (value !== null && value !== undefined) {
                      component.style.cssText = String(value);
                  } else {
                      component.removeAttribute('style');
                  }
                  return;
              }

              if (value === null || value === undefined) {
                  component.removeAttribute(htmlName);

                  if (htmlName in component) {
                      try {
                          component[htmlName] = value;
                      } catch (error) {
                          console.warn(
                              "[PyLage] Failed to clear DOM property:",
                              htmlName,
                              error
                          );
                      }
                  }

                  return;
              }

              if (htmlName in component) {
                  try {
                      component[htmlName] = value;
                      return;
                  } catch (error) {
                      console.warn(
                          "[PyLage] DOM property update failed:",
                          htmlName,
                          error
                      );
                  }
              }

              component.setAttribute(
                  htmlName,
                  String(value)
              );
          });

        window.PyLage.onUpdate = window.PyLage.onUpdate || function () {};
        window.PyLage.onUpdate(message);
    };

    document.addEventListener("click", handleEvent);
    document.addEventListener("input", handleEvent);
    document.addEventListener("change", handleEvent);
    document.addEventListener("submit", handleEvent);

    scanAndBindEvents(document);
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            scanAndBindEvents(document);
        });
    }

    window.PyLage.socket = connectWebSocket(
        window.PyLage.websocketUrl
    );
})();
"""


def get_client_runtime(websocket_url: str | None = None) -> str:
    """Return the embedded PyLage browser runtime."""

    url = websocket_url or ""

    bootstrap = (
        "<script>\n"
        "window.PyLage = window.PyLage || {};\n"
        f"window.PyLage.websocketUrl = {url!r};\n"
        "</script>\n"
    )

    return bootstrap + CLIENT_RUNTIME
