# Mac Log Collection with Grafana Loki and Alloy

This repository provides a setup for collecting and visualizing real logs from your Mac laptop using Grafana Loki and Grafana Alloy.

![Loki Stack](https://grafana.com/media/docs/loki/getting-started-loki-stack-3.png)

## Overview

This setup collects logs from:
- **System logs**: `/var/log/system.log`, `/var/log/secure.log`, diagnostic reports
- **Application logs**: Installation logs, filesystem logs, commerce logs
- **User logs**: User-specific logs from `~/Library/Logs/`

## Prerequisites
Ensure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Mac Log Collection Stack

1. Navigate to the project directory:
   ```sh
   cd grafana-loki-alloy_implementation
   ```

2. Start Loki, Grafana, and Alloy using Docker Compose:
   ```sh
   docker compose up -d
   ```

3. Verify the components are running:
   - **Grafana:** [http://localhost:3000](http://localhost:3000)
   - **Loki:** [http://localhost:3100/metrics](http://localhost:3100/metrics)
   - **Alloy:** [http://localhost:12345/graph](http://localhost:12345/graph)

## Querying Mac Logs

You can query your Mac logs using Grafana's **Explore** feature at [http://localhost:3000](http://localhost:3000):

1. Open **Explore**.
2. Select the Loki data source.
3. Use LogQL queries, for example:

   **View all system logs:**
   ```logql
   {source="system"}
   ```

   **View error logs:**
   ```logql
   {source="system"} |= "error"
   ```

   **View user-specific logs:**
   ```logql
   {source="user"}
   ```

   **View application logs:**
   ```logql
   {source="application"}
   ```

   **Search for specific terms:**
   ```logql
   {platform="macos"} |= "kernel"
   ```

## Log Sources

The setup collects logs from these Mac-specific locations:

### System Logs (`source="system"`)
- `/var/log/system.log` - General system messages
- `/var/log/secure.log` - Security-related messages
- `/var/log/asl/*.asl` - Apple System Log files
- `/var/log/DiagnosticReports/*.crash` - Application crash reports
- `/var/log/DiagnosticReports/*.spin` - Application hang reports
- `/var/log/DiagnosticReports/*.hang` - System hang reports

### Application Logs (`source="application"`)
- `/var/log/install.log` - Installation logs
- `/var/log/commerce.log` - App Store and commerce logs
- `/var/log/fsck_hfs.log` - HFS filesystem check logs
- `/var/log/fsck_apfs.log` - APFS filesystem check logs

### User Logs (`source="user"`)
- `/Users/*/Library/Logs/*.log` - User application logs
- `/Users/*/Library/Logs/DiagnosticReports/*.crash` - User app crashes
- `/Users/*/Library/Logs/DiagnosticReports/*.spin` - User app hangs

## Stopping the Stack

To stop all services:
```sh
docker compose down
```

## Troubleshooting

If you encounter permission issues accessing log files, you may need to grant Docker access to the log directories. The setup uses read-only mounts for security.

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


