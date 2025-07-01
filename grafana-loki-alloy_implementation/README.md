# Live Log Collection with Grafana Loki and Alloy

This repository provides a setup for collecting and visualizing live logs using Grafana Loki and Grafana Alloy, with a Python application that generates realistic log data in real-time.

![Loki Stack](https://grafana.com/media/docs/loki/getting-started-loki-stack-3.png)

## Overview

This setup includes:
- **Log Generator**: A Python Flask application that generates realistic logs continuously
- **Grafana Alloy**: Collects logs from Docker containers
- **Grafana Loki**: Stores and indexes the logs
- **Grafana**: Visualizes and queries the logs

## Prerequisites
Ensure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Log Collection Stack

1. Navigate to the project directory:
   ```sh
   cd grafana-loki-alloy_implementation
   ```

2. Start all services using Docker Compose:
   ```sh
   docker compose up -d
   ```

3. Verify the components are running:
   - **Log Generator:** [http://localhost:5001](http://localhost:5001)
   - **Grafana:** [http://localhost:3000](http://localhost:3000)
   - **Loki:** [http://localhost:3100/metrics](http://localhost:3100/metrics)
   - **Alloy:** [http://localhost:12345/graph](http://localhost:12345/graph)

## Log Generator Application

The log generator creates realistic log entries including:
- **Info logs**: User actions (login, logout, search, etc.)
- **Warning logs**: Performance warnings
- **Error logs**: Various error scenarios (timeout, permission denied, etc.)

### Manual Log Generation

You can manually generate logs by visiting:
- `http://localhost:5001/generate_log` - Generate a random log
- `http://localhost:5001/generate_log?type=error&message=Custom error message` - Generate specific log

## Querying Logs

You can query your logs using Grafana's **Explore** feature at [http://localhost:3000](http://localhost:3000):

1. Open **Explore**.
2. Select the Loki data source.
3. Use LogQL queries, for example:

   **View all logs:**
   ```logql
   {source="application"}
   ```

   **View error logs:**
   ```logql
   {source="application"} |= "error"
   ```

   **View logs from specific container:**
   ```logql
   {container="grafana-loki-alloy_implementation-log-generator-1"}
   ```

   **View warning logs:**
   ```logql
   {source="application"} |= "warning"
   ```

   **Search for specific users:**
   ```logql
   {source="application"} |= "alice"
   ```

## Log Types Generated

The application generates various types of realistic logs:

### Info Logs
- User actions: login, logout, search, download, upload, delete, create
- Resource operations: document, image, video, audio, database, file

### Warning Logs
- Performance warnings
- Operation timeouts
- Resource usage alerts

### Error Logs
- Timeout errors
- Permission denied errors
- Not found errors
- Server errors
- Network errors

## Stopping the Stack

To stop all services:
```sh
docker compose down
```

## Troubleshooting

If you encounter issues:

1. **Check container status:**
   ```sh
   docker compose ps
   ```

2. **View logs:**
   ```sh
   docker compose logs alloy
   docker compose logs log-generator
   ```

3. **Restart services:**
   ```sh
   docker compose restart
   ```

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch-name`).
3. Commit your changes.
4. Open a pull request.

## Issues

If you encounter any problems, please open an issue in this repository with:
- A clear description of the problem.
- Steps to reproduce the issue.
- Logs or error messages if available.


