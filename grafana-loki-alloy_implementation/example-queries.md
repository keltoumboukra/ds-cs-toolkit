# Example LogQL Queries for Live Log Collection

Use these queries in Grafana Explore (http://localhost:3000) to get started with your live log collection.

## Basic Queries

### View all application logs
```logql
{source="application"}
```

### View logs from specific container
```logql
{container="grafana-loki-alloy_implementation-log-generator-1"}
```

### View all logs
```logql
{platform="docker"}
```

## Error and Warning Queries

### Find error messages
```logql
{source="application"} |= "error"
```

### Find warning messages
```logql
{source="application"} |= "warning"
```

### Find failed operations
```logql
{source="application"} |= "failed"
```

## User Activity Queries

### Find user login events
```logql
{source="application"} |= "login"
```

### Find user logout events
```logql
{source="application"} |= "logout"
```

### Find specific user actions
```logql
{source="application"} |= "alice"
```
```logql
{source="application"} |= "bob"
```

## Resource Operation Queries

### Find file operations
```logql
{source="application"} |= "file"
```

### Find database operations
```logql
{source="application"} |= "database"
```

### Find document operations
```logql
{source="application"} |= "document"
```

### Find media operations
```logql
{source="application"} |= "image"
```
```logql
{source="application"} |= "video"
```

## Action-Specific Queries

### Find search operations
```logql
{source="application"} |= "search"
```

### Find download operations
```logql
{source="application"} |= "download"
```

### Find upload operations
```logql
{source="application"} |= "upload"
```

### Find delete operations
```logql
{source="application"} |= "delete"
```

### Find create operations
```logql
{source="application"} |= "create"
```

## Error Type Queries

### Find timeout errors
```logql
{source="application"} |= "timeout"
```

### Find permission errors
```logql
{source="application"} |= "permission denied"
```

### Find server errors
```logql
{source="application"} |= "server error"
```

### Find network errors
```logql
{source="application"} |= "network error"
```

## Advanced Queries

### Combine multiple conditions
```logql
{source="application"} |= "error" |= "timeout"
```

### Exclude certain terms
```logql
{source="application"} != "info" != "debug"
```

### Time-based filtering (last hour)
```logql
{source="application"} |= "error" [1h]
```

### Count log entries by type
```logql
sum by (level) (count_over_time({source="application"}[5m]))
```

### Count errors over time
```logql
sum(count_over_time({source="application"} |= "error" [5m]))
```

## Performance Queries

### Find performance warnings
```logql
{source="application"} |= "took longer than expected"
```

### Find timeout warnings
```logql
{source="application"} |= "timeout"
```

## Tips

1. Use `|=` for case-sensitive text matching
2. Use `=~` for regex matching
3. Use `!=` to exclude terms
4. Add time ranges like `[5m]`, `[1h]`, `[24h]` to limit results
5. Use `count_over_time()` for aggregations
6. Use `sum by (label)` to group results by labels
7. The log generator creates logs every 1-5 seconds, so you should see continuous data
8. You can manually generate logs by visiting `http://localhost:5000/generate_log` 