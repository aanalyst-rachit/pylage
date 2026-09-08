from __future__ import annotations

import asyncio
import threading
from typing import Any, Optional

try:
    from websockets.asyncio.server import Server, ServerConnection, serve
except ImportError:
    Server = Any  # type: ignore[misc,assignment]
    ServerConnection = Any  # type: ignore[misc,assignment]
    serve = None  # type: ignore[assignment]

from pylage.ENGINE.core.binding import StateBinding
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.ENGINE.core.events import EventDispatcher
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.scheduler import Scheduler
from pylage.ENGINE.core.state import State
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.global_theme import subscribe_global_theme
from pylage.ENGINE.core.protocol import (
    EventMessage,
    EventMessageResponse,
    UpdateMessage,
    ThemeUpdateMessage,
    TreeAddMessage,
    TreeRemoveMessage,
    TreeMoveMessage,
    TreeReplaceMessage,
    TreeClearMessage,
    TreeSetChildrenMessage,
)


class WebSocketServer:
    """WebSocket transport for PyLage events and state updates."""

    def __init__(
        self,
        root: Component,
        *,
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "WebSocketServer expects a Component root."
            )

        self.root = root
        self.host = host
        self.port = port

        # Dynamic tree mutations must use the same renderer contract
        # as the initial static HTML render.  Keep one renderer instance
        # on the server so registered/custom renderers are reused.
        self._renderer = HTMLRenderer()

        self._dispatcher = EventDispatcher(root)

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._server: Optional[Server] = None
        self._thread: Optional[threading.Thread] = None

        self._connections: set[ServerConnection] = set()
        self._connections_lock = threading.Lock()

        self._theme_unsubscribe = None

        self._ready = threading.Event()
        self._startup_error: Optional[BaseException] = None

        self._graph = DependencyGraph()
        self._dirty = DirtyNodes()
        self._scheduler = Scheduler(
            self._dirty,
            self._scheduled_update,
            schedule_flush=self._schedule_scheduler_flush,
        )

        self._binding = StateBinding(
            root,
            self._on_state_change,
            graph=self._graph,
            dirty=self._dirty,
            scheduler=self._scheduler,
        )

        from pylage.ENGINE.core.tree import TreeMutationObserver

        self._tree_observer = TreeMutationObserver(
            root,
            self._on_tree_mutation,
        )

    @property
    def running(self) -> bool:
        return self._server is not None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("WebSocket server is not running.")

        # Wildcard bind addresses are valid for the server listener but are
        # not valid browser connection targets. Use loopback for local
        # browser clients while keeping the server bound to the wildcard.
        host = self.host
        if host == "0.0.0.0":
            host = "127.0.0.1"
        elif host == "::":
            host = "[::1]"

        return f"ws://{host}:{self.port}/"

    def _schedule_scheduler_flush(self) -> None:
        """Schedule one coalesced scheduler flush on the WebSocket loop."""

        if self._loop is None:
            return

        self._loop.call_soon_threadsafe(
            lambda: self._loop.call_later(
                0.001,
                self._scheduler.flush,
            )
        )

    def _json_safe(self, value: Any) -> Any:
        """Convert PyLage runtime values into JSON-safe values."""

        if isinstance(value, State):
            return self._json_safe(value.value)

        if isinstance(value, Style):
            return {
                "color": self._json_safe(value.color),
                "background": self._json_safe(value.background),
                "background_color": self._json_safe(value.background_color),
                "font_size": self._json_safe(value.font_size),
                "font_weight": self._json_safe(value.font_weight),
                "font_family": self._json_safe(value.font_family),
                "line_height": self._json_safe(value.line_height),
                "text_align": self._json_safe(value.text_align),
                "margin": self._json_safe(value.margin),
                "margin_top": self._json_safe(value.margin_top),
                "margin_right": self._json_safe(value.margin_right),
                "margin_bottom": self._json_safe(value.margin_bottom),
                "margin_left": self._json_safe(value.margin_left),
                "padding": self._json_safe(value.padding),
                "padding_top": self._json_safe(value.padding_top),
                "padding_right": self._json_safe(value.padding_right),
                "padding_bottom": self._json_safe(value.padding_bottom),
                "padding_left": self._json_safe(value.padding_left),
                "width": self._json_safe(value.width),
                "min_width": self._json_safe(value.min_width),
                "max_width": self._json_safe(value.max_width),
                "height": self._json_safe(value.height),
                "min_height": self._json_safe(value.min_height),
                "max_height": self._json_safe(value.max_height),
                "display": self._json_safe(value.display),
                "position": self._json_safe(value.position),
                "top": self._json_safe(value.top),
                "right": self._json_safe(value.right),
                "bottom": self._json_safe(value.bottom),
                "left": self._json_safe(value.left),
                "flex_direction": self._json_safe(value.flex_direction),
                "flex_wrap": self._json_safe(value.flex_wrap),
                "justify_content": self._json_safe(value.justify_content),
                "align_items": self._json_safe(value.align_items),
                "align_content": self._json_safe(value.align_content),
                "flex": self._json_safe(value.flex),
                "flex_grow": self._json_safe(value.flex_grow),
                "flex_shrink": self._json_safe(value.flex_shrink),
                "flex_basis": self._json_safe(value.flex_basis),
                "gap": self._json_safe(value.gap),
                "row_gap": self._json_safe(value.row_gap),
                "column_gap": self._json_safe(value.column_gap),
                "grid_template_columns": self._json_safe(value.grid_template_columns),
                "grid_template_rows": self._json_safe(value.grid_template_rows),
                "grid_column": self._json_safe(value.grid_column),
                "grid_row": self._json_safe(value.grid_row),
                "border": self._json_safe(value.border),
                "border_width": self._json_safe(value.border_width),
                "border_style": self._json_safe(value.border_style),
                "border_color": self._json_safe(value.border_color),
                "border_radius": self._json_safe(value.border_radius),
                "box_shadow": self._json_safe(value.box_shadow),
                "opacity": self._json_safe(value.opacity),
                "overflow": self._json_safe(value.overflow),
                "box_sizing": self._json_safe(value.box_sizing),
                "cursor": self._json_safe(value.cursor),
                "z_index": self._json_safe(value.z_index),
                "transform": self._json_safe(value.transform),
                "transition": self._json_safe(value.transition),
                "text_transform": self._json_safe(value.text_transform),
                "text_decoration": self._json_safe(value.text_decoration),
                "letter_spacing": self._json_safe(value.letter_spacing),
                "white_space": self._json_safe(value.white_space),
                "outline": self._json_safe(value.outline),
                "visibility": self._json_safe(value.visibility),
                "pointer_events": self._json_safe(value.pointer_events),
                "border_top": self._json_safe(value.border_top),
                "border_right": self._json_safe(value.border_right),
                "border_bottom": self._json_safe(value.border_bottom),
                "border_left": self._json_safe(value.border_left),
                "custom": self._json_safe(value.custom),
            }

        if isinstance(value, ResponsiveStyle):
            return {
                "base": self._json_safe(value.base),
                "sm": self._json_safe(value.sm),
                "md": self._json_safe(value.md),
                "lg": self._json_safe(value.lg),
                "xl": self._json_safe(value.xl),
            }

        if isinstance(value, dict):
            return {
                str(key): self._json_safe(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [self._json_safe(item) for item in value]

        if isinstance(value, (str, int, float, bool)) or value is None:
            return value

        return str(value)

    def _scheduled_update(
        self,
        component: Component,
        changed_props: set[str] | None = None,
    ) -> None:
        """Flush a dirty component using only its changed props."""

        props: dict[str, Any] = {}

        if changed_props is None:
            changed_props = self._dirty.changed_props(component)

        if changed_props is None:
            prop_items = component.props.items()
        else:
            prop_items = (
                (prop_name, component.props[prop_name])
                for prop_name in changed_props
                if prop_name in component.props
            )

        for prop_name, value in prop_items:
            if prop_name == "style":
                style_value = value

                if isinstance(style_value, State):
                    style_value = style_value.value

                if isinstance(style_value, Style):
                    props[prop_name] = style_value.to_css()
                    continue

            props[prop_name] = self._json_safe(value)

        self._on_state_change(component, props)

    def _on_state_change(
        self,
        component: Component,
        props: dict[str, Any],
    ) -> None:
        """Called whenever a bound State changes."""

        definition = self._get_component_definition(component)

        prop_meta = {}
        remove_props = []

        if definition is not None and definition.props:
            for prop_name in list(props):
                prop_definition = definition.props.get(prop_name)
                if prop_definition is None:
                    continue

                meta = {
                    "kind": prop_definition.kind,
                    "html_name": prop_definition.html_name,
                }

                if prop_definition.boolean_mode != "normal":
                    meta["boolean_mode"] = prop_definition.boolean_mode

                prop_meta[prop_name] = meta


        message = UpdateMessage(
            component_id=component.id,
            props=props,
            remove_props=remove_props,
            prop_meta=prop_meta,
        )

        if self._loop is None or self._server is None:
            return

        asyncio.run_coroutine_threadsafe(
            self._broadcast(message.to_json()),
            self._loop,
        )

    def _on_tree_mutation(
        self,
        event: dict[str, Any],
    ) -> None:
        mutation_type = event.get("type")

        if mutation_type == "move":
            component = event.get("component")
            old_parent = event.get("old_parent")
            new_parent = event.get("new_parent")

            if not isinstance(component, Component):
                return

            if not isinstance(old_parent, Component):
                return

            if not isinstance(new_parent, Component):
                return

            message = TreeMoveMessage(
                component_id=component.id,
                old_parent_id=old_parent.id,
                new_parent_id=new_parent.id,
            )

            raw_message = message.to_json()

            if self._loop is None:
                return

            asyncio.run_coroutine_threadsafe(
                self._broadcast(raw_message),
                self._loop,
            )

            return

        if mutation_type == "replace":
            parent = event.get("parent")
            old_child = event.get("old_child")
            new_child = event.get("new_child")
            index = event.get("index")

            if not isinstance(parent, Component):
                return

            if not isinstance(old_child, Component):
                return

            if not isinstance(new_child, Component):
                return

            if not isinstance(index, int):
                return

            self._dispatcher.deindex(old_child)
            self._binding.unbind(old_child)
            self._dispatcher.index(new_child)
            self._binding.bind(new_child)

            component = self._serialize_component_tree(new_child)

            message = TreeReplaceMessage(
                parent_id=parent.id,
                old_component_id=old_child.id,
                new_component=component,
                index=index,
            )

            if self._loop is None:
                return

            asyncio.run_coroutine_threadsafe(
                self._broadcast(message.to_json()),
                self._loop,
            )

            return

        if mutation_type == "set_children":
            parent = event.get("parent")
            children = event.get("children", [])

            if not isinstance(parent, Component):
                return

            for child in children:
                if isinstance(child, Component):
                    self._dispatcher.index(child)
                    self._binding.bind(child)

            serialized_children = [
                self._serialize_component_tree(child)
                for child in children
                if isinstance(child, Component)
            ]

            message = TreeSetChildrenMessage(
                parent_id=parent.id,
                children=serialized_children,
            )

            if self._loop is None:
                return

            asyncio.run_coroutine_threadsafe(
                self._broadcast(message.to_json()),
                self._loop,
            )

            return

        if mutation_type == "clear":
            parent = event.get("parent")
            children = event.get("children", [])

            if not isinstance(parent, Component):
                return

            for child in children:
                if isinstance(child, Component):
                    self._dispatcher.deindex(child)
                    self._binding.unbind(child)

            component_ids = [
                child.id
                for child in children
                if isinstance(child, Component)
            ]

            message = TreeClearMessage(
                parent_id=parent.id,
                component_ids=component_ids,
            )

            if self._loop is None:
                return

            asyncio.run_coroutine_threadsafe(
                self._broadcast(message.to_json()),
                self._loop,
            )

            return

        if mutation_type == "remove":
            parent = event.get("parent")
            children = event.get("children", [])

            if not isinstance(parent, Component):
                return

            for child in children:
                if isinstance(child, Component):
                    self._dispatcher.deindex(child)
                    self._binding.unbind(child)

            component_ids = [
                child.id
                for child in children
                if isinstance(child, Component)
            ]

            if not component_ids:
                return

            message = TreeRemoveMessage(
                parent_id=parent.id,
                component_ids=component_ids,
            )

            raw_message = message.to_json()

            if self._loop is None:
                return

            asyncio.run_coroutine_threadsafe(
                self._broadcast(raw_message),
                self._loop,
            )
            return

        if mutation_type != "add":
            return

        parent = event.get("parent")
        children = event.get("children", [])

        if not isinstance(parent, Component):
            return

        components = []

        for child in children:
            if not isinstance(child, Component):
                continue

            self._dispatcher.index(child)
            self._binding.bind(child)

            components.append(self._serialize_component_tree(child))

        if not components:
            return

        message = TreeAddMessage(
            parent_id=parent.id,
            components=components,
            index=event.get("index"),
        )

        raw_message = message.to_json()

        if self._loop is None:
            return

        asyncio.run_coroutine_threadsafe(
            self._broadcast(raw_message),
            self._loop,
        )

    def _serialize_component_tree(self, component: Component) -> dict[str, Any]:
        """Serialize a component for browser-side dynamic tree insertion.

        The initial HTML renderer applies registry HTML-name mappings and
        renderer default styles. Dynamic tree mutations must carry the same
        browser-facing metadata so that a component inserted with
        ``set_children``/``add``/``replace`` renders equivalently.
        """
        definition = self._get_component_definition(component)

        attrs: dict[str, Any] = {}

        if definition is not None and definition.props:
            for prop_name, prop_definition in definition.props.items():
                if prop_name not in component.props:
                    continue

                value = component.props.get(prop_name)

                if isinstance(value, State):
                    value = value.value

                if value is None:
                    continue

                html_name = prop_definition.html_name or prop_name

                if prop_definition.kind == "boolean":
                    if bool(value):
                        attrs[html_name] = True
                    continue

                if prop_definition.kind == "attribute":
                    attrs[html_name] = self._json_safe(value)

        # ``class_name`` is a normal registry attribute in PyLage. The
        # renderer maps it to HTML ``class``; preserve that mapping even
        # when a component definition predates explicit prop metadata.
        if "class_name" in component.props:
            class_name = component.props.get("class_name")
            if isinstance(class_name, State):
                class_name = class_name.value
            if class_name is not None:
                attrs["class"] = self._json_safe(class_name)

        style = component.props.get("style")

        if isinstance(style, State):
            style = style.value

        default_style = self._dynamic_default_style(component)

        if default_style is not None:
            if style is None:
                style = default_style
            elif isinstance(style, Style):
                style = default_style.merge(style)

        style_css = None

        if isinstance(style, Style):
            style_css = style.to_css() or None

        # ``html`` is the authoritative DOM representation for
        # dynamically inserted components.  It is produced by the same
        # HTMLRenderer used by the initial page render, so custom
        # renderers such as Table/DataFrame/Form/Dialog are preserved.
        rendered_html = self._renderer._render_component(component)

        return {
            "id": component.id,
            "type": component.type,
            "tag": (
                definition.tag
                if definition is not None
                else "div"
            ),
            "events": ",".join(component.events.keys()),
            "html": rendered_html,
            "props": {
                k: self._json_safe(v)
                for k, v in component.props.items()
            },
            "attrs": attrs,
            "style": style_css,
            "children": [
                self._serialize_component_tree(child)
                for child in component.children
                if isinstance(child, Component)
            ],
        }

    def _dynamic_default_style(self, component: Component) -> Style | None:
        """Return renderer defaults required by dynamic DOM insertion.

        These are the defaults currently applied by HTMLRenderer for the
        built-in layout/card components. Keeping them here makes the dynamic
        tree protocol match the existing renderer without changing the
        component tree or the public component API.
        """
        if component.type == "Column":
            return Style(
                display="flex",
                flex_direction="column",
            )

        if component.type == "Row":
            return Style(
                display="flex",
                flex_direction="row",
            )

        if component.type == "Card":
            return Style(
                display="block",
                width="100%",
                box_sizing="border-box",
            )

        return None

    def flush(self) -> None:
        """Explicit batching boundary for scheduled state updates."""
        self._scheduler.flush()

    def _get_component_definition(self, component: Component):
        """Resolve registry metadata for a component."""
        from pylage.ENGINE.core.registry import registry

        return registry.get(component.type)

    def _subscribe_theme(self) -> None:
        if self._theme_unsubscribe is not None:
            return

        self._theme_unsubscribe = subscribe_global_theme(
            self._on_theme_change
        )

    def _unsubscribe_theme(self) -> None:
        if self._theme_unsubscribe is None:
            return

        self._theme_unsubscribe()
        self._theme_unsubscribe = None

    def _on_theme_change(self, old_theme: Any, new_theme: Any) -> None:
        if new_theme is None:
            return

        css = new_theme.to_css()
        message = ThemeUpdateMessage(css=css)

        if self._loop is None or self._server is None:
            return

        asyncio.run_coroutine_threadsafe(
            self._broadcast(message.to_json()),
            self._loop,
        )

    async def _broadcast(self, raw_message: str) -> None:
        """Send a state update to every connected browser."""

        with self._connections_lock:
            connections = tuple(self._connections)

        if not connections:
            return

        results = await asyncio.gather(
            *(connection.send(raw_message) for connection in connections),
            return_exceptions=True,
        )

        dead = {
            connection
            for connection, result in zip(connections, results)
            if isinstance(result, Exception)
        }

        if dead:
            with self._connections_lock:
                self._connections.difference_update(dead)

    async def _handle(self, connection: ServerConnection) -> None:
        with self._connections_lock:
            self._connections.add(connection)

        try:
            async for raw_message in connection:
                try:
                    message = EventMessage.from_json(raw_message)

                    result = self._dispatcher.dispatch(
                        message.component_id,
                        message.event,
                        message.payload,
                    )

                    await connection.send(
                        EventMessageResponse.success(result).to_json()
                    )

                except Exception as exc:
                    await connection.send(
                        EventMessageResponse.failure(str(exc)).to_json()
                    )
        finally:
            with self._connections_lock:
                self._connections.discard(connection)

    async def _serve(self) -> None:
        try:
            self._server = await serve(
                self._handle,
                self.host,
                self.port,
            )

            socket = next(iter(self._server.sockets))
            self.port = socket.getsockname()[1]

        except BaseException as exc:
            self._startup_error = exc

        finally:
            self._ready.set()

        if self._server is None:
            return

        await self._server.wait_closed()

    def _thread_main(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._serve())
        finally:
            self._loop.close()
            self._loop = None

    def start(self) -> str:
        if serve is None:
            raise ImportError(
                "websockets is required for WebSocketServer. "
                "Install it with: pip install websockets"
            )

        if self._thread is not None:
            raise RuntimeError(
                "WebSocket server is already running."
            )

        self._startup_error = None
        self._ready.clear()
        self._subscribe_theme()

        self._thread = threading.Thread(
            target=self._thread_main,
            daemon=True,
        )

        self._thread.start()
        self._ready.wait()

        if self._startup_error is not None:
            error = self._startup_error
            self._unsubscribe_theme()
            self._thread = None
            raise RuntimeError(
                "Failed to start WebSocket server."
            ) from error

        return self.url

    def stop(self) -> None:
        if self._thread is None:
            return

        self._binding.stop()
        self._unsubscribe_theme()

        if self._loop is not None and self._server is not None:
            self._loop.call_soon_threadsafe(
                self._server.close
            )

        self._thread.join(timeout=2.0)

        self._server = None
        self._thread = None
        self._loop = None

        with self._connections_lock:
            self._connections.clear()
