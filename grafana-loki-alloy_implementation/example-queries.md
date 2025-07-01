# Example LogQL Queries for Mac Logs

Use these queries in Grafana Explore (http://localhost:3000) to get started with your Mac logs.

## Basic Queries

### View all logs by source
```logql
{source="system"}
```
```logql
{source="application"}
```
```logql
{source="user"}
```

### View all Mac logs
```logql
{platform="macos"}
```

## Error and Warning Queries

### Find error messages
```logql
{platform="macos"} |= "error"
```

### Find warning messages
```logql
{platform="macos"} |= "warning"
```

### Find failed operations
```logql
{platform="macos"} |= "failed"
```

## System-Specific Queries

### Kernel messages
```logql
{source="system"} |= "kernel"
```

### Security events
```logql
{source="system"} |= "security"
```

### Authentication events
```logql
{source="system"} |= "auth"
```

## Application-Specific Queries

### Installation logs
```logql
{source="application"} |= "install"
```

### Filesystem operations
```logql
{source="application"} |= "fsck"
```

### App Store activity
```logql
{source="application"} |= "commerce"
```

## User-Specific Queries

### User application crashes
```logql
{source="user"} |= "crash"
```

### User application hangs
```logql
{source="user"} |= "hang"
```

## Advanced Queries

### Combine multiple sources
```logql
{source=~"system|application"} |= "error"
```

### Time-based filtering (last hour)
```logql
{platform="macos"} |= "error" [1h]
```

### Exclude certain terms
```logql
{platform="macos"} != "debug" != "info"
```

### Count log entries by source
```logql
sum by (source) (count_over_time({platform="macos"}[5m]))
```

## Useful Patterns

### Find specific applications
```logql
{platform="macos"} |= "Safari"
```
```logql
{platform="macos"} |= "Chrome"
```

### Find system startup/shutdown
```logql
{source="system"} |= "shutdown"
```
```logql
{source="system"} |= "startup"
```

### Find network-related issues
```logql
{platform="macos"} |= "network"
```
```logql
{platform="macos"} |= "wifi"
```

## Tips

1. Use `|=` for case-sensitive text matching
2. Use `=~` for regex matching
3. Use `!=` to exclude terms
4. Add time ranges like `[5m]`, `[1h]`, `[24h]` to limit results
5. Use `count_over_time()` for aggregations
6. Use `sum by (label)` to group results by labels 