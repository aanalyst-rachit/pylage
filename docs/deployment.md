# Production Deployment

Deploy PyLage as a production ASGI application behind a public HTTPS endpoint.

## Architecture

```text
Browser
   |
   | HTTPS
   v
Reverse Proxy / Platform
   |
   | HTTP + WebSocket
   v
PyLage ASGI application
   |
   +-- HTTP
   +-- WebSocket
   +-- /health
```

For production deployments, use the ASGI/Granian runtime rather than the development threaded server.

## Docker

PyLage includes an official `Dockerfile` at the repository root.

The image uses Python 3.12, Granian, the PyLage ASGI runtime, `PYLAGE_APP_FILE` for selecting the application, and `PORT` for the service port.

The default repository container uses `working_demo/app.py` as the smoke/demo application.

To use another application, set `PYLAGE_APP_FILE` to the application path inside the container.

The container listens on port `8000` by default and honors the platform-provided `PORT`.

## Railway

Railway can automatically detect a root `Dockerfile`.

Create a Railway project and connect the PyLage repository. Use the repository root as the service source.

Railway provides the `PORT` environment variable to the service. The PyLage Docker command uses that value automatically and falls back to `8000`.

With the Railway CLI:

```bash
railway link
railway up
```

After deployment, verify `/health` and then open the public HTTPS URL.

PyLage derives the browser WebSocket endpoint from the browser origin, so an HTTPS deployment uses WSS automatically.

## Render

Create a Render Web Service and select Docker as the runtime.

Use the repository root `Dockerfile` as the Dockerfile.

Render runs the Docker image using the Dockerfile command unless a custom command is configured.

Keep the container configured to use the platform-provided `PORT`.

After deployment, verify `/health`, then open the HTTPS service URL and verify browser interaction and WebSocket connectivity.

## Fly.io

From the PyLage repository:

```bash
fly launch --no-deploy
```

Review the generated `fly.toml` before the first deployment.

Deploy with:

```bash
fly deploy
```

Check the deployment with:

```bash
fly status
fly apps open
```

Verify `/health` and confirm browser interaction over HTTPS.

## Generic VPS

Install Python and the PyLage package on the server, or deploy the supplied Docker image.

For a Docker-based VPS deployment:

```bash
docker build -t pylage-app .
docker run --rm -p 8000:8000 -e PORT=8000 pylage-app
```

For a non-container deployment, run the production ASGI application through Granian.

Do not expose the application directly as the public HTTPS endpoint. Put a reverse proxy such as Nginx in front of it.

## Production Command

The intended PyLage production command is:

```bash
pylage run app.py --host 0.0.0.0 --port $PORT
```

The application must listen on the platform-provided port.

For the production ASGI factory, the application file can also be selected with `PYLAGE_APP_FILE`.

## Nginx Reverse Proxy

The production request path should be:

```text
Browser
  |
  | HTTPS / WSS
  v
Nginx
  |
  | HTTP / WebSocket
  v
PyLage
```

Example configuration:

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

The important WebSocket settings are `proxy_http_version 1.1`, `Upgrade`, and `Connection`.

TLS terminates at the reverse proxy. The browser connects using HTTPS/WSS while the proxy forwards traffic to the PyLage endpoint.

## WebSocket Origin Handling

PyLage can derive the browser WebSocket endpoint from the current browser origin.

An HTTP page uses `ws://`, while an HTTPS page uses `wss://`.

This avoids requiring the application to trust arbitrary forwarded host headers merely to construct the browser WebSocket URL.

## Health Check

Every production deployment should expose:

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```

The response is HTTP `200` with `Content-Type: application/json` and `Cache-Control: no-cache`.

Use this endpoint for platform health checks and deployment verification.

## Environment Configuration

Production deployments may provide:

```text
PYLAGE_HOST
PYLAGE_PORT
PYLAGE_ENV
PYLAGE_APP_FILE
PYLAGE_TITLE
PORT
```

Platform-provided `PORT` should be honored for container and platform deployments.

Do not commit secrets into the repository.

## Production Verification

After deployment, verify the complete flow:

1. Open the HTTPS application.
2. Confirm the initial document loads.
3. Confirm the browser establishes a WSS connection.
4. Interact with the application.
5. Reload the browser.
6. Verify reconnection works.
7. Open multiple browser sessions.
8. Verify sessions remain isolated.
9. Request `/health`.
10. Confirm deployment logs contain no startup or WebSocket errors.

## WebSocket Idle Timeout

PyLage sends a WebSocket heartbeat every 20 seconds by default. Each heartbeat waits up to the same heartbeat interval for the peer response. Connections that fail the heartbeat are removed and closed.

When PyLage runs behind a reverse proxy or load balancer, its WebSocket idle timeout must be longer than the PyLage heartbeat interval. Otherwise the proxy can close an otherwise healthy connection before PyLage sends the next heartbeat.

### Recommended production setting

Use an idle timeout of at least 60 seconds for the WebSocket connection. This gives the default 20-second heartbeat enough margin for network and proxy scheduling delays.

If you customize the PyLage heartbeat interval, configure the proxy or load balancer idle timeout to remain comfortably above that interval.

For example:

```text
PyLage heartbeat:       20 seconds
Recommended idle time:  60+ seconds
```

The reverse proxy must also preserve the WebSocket upgrade headers described above. A timeout that is long enough but does not forward the upgrade correctly will still prevent WebSocket connections from working.

## Troubleshooting

### Page loads but WebSocket does not connect

Check that HTTPS is being used, the browser is using WSS, the reverse proxy forwards `Upgrade` and `Connection`, the upstream uses HTTP/1.1, and PyLage is listening on the platform-provided port.

### Health check fails

Check that the service is listening on `0.0.0.0`, the platform `PORT` is being honored, `/health` is reachable, and the application process did not exit during startup.

### Browser works locally but not behind HTTPS

Check the reverse proxy configuration first. PyLage derives the WebSocket protocol from the browser origin, so an HTTPS page should use WSS automatically.

## Deployment Checklist

- [ ] Dockerfile builds successfully.
- [ ] Production ASGI application starts.
- [ ] Application listens on `0.0.0.0`.
- [ ] Platform `PORT` is honored.
- [ ] HTTPS endpoint is reachable.
- [ ] WSS connection succeeds.
- [ ] WebSocket upgrade headers are forwarded.
- [ ] `/health` returns HTTP 200.
- [ ] Browser interaction works.
- [ ] Browser reconnect works.
- [ ] Multiple sessions remain isolated.
- [ ] WebSocket idle timeout is compatible with PyLage heartbeat settings.
