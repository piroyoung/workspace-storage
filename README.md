# workspace-storage

A Python package for Microsoft Fabric workspace and tenant management utilities.

## Features

- **FabricUtil**: A utility class for workspace and tenant management operations
  - Get list of workspaces using semantic-link API (with fallback)
  - Calculate actual total file sizes for workspaces from real data
  - Calculate actual total file sizes for tenants from real data
  - Automatic detection of Microsoft Fabric environment
  - Graceful fallback when not in Fabric environment
  - Support for various authentication methods

## Installation

```bash
pip install workspace-storage
```

For Microsoft Fabric integration (optional):
```bash
pip install workspace-storage[fabric]
```

## Quick Start

```python
from workspace_storage import FabricUtil

# Initialize FabricUtil with workspace and tenant IDs
fabric_util = FabricUtil(
    workspace_id="your-workspace-id",
    tenant_id="your-tenant-id"
)

# Get list of workspaces
workspaces = fabric_util.get_workspaces()
print(f"Found {len(workspaces)} workspaces")

# Get workspace total size
workspace_size = fabric_util.get_workspace_total_size()
print(f"Workspace size: {workspace_size:,} bytes")

# Get tenant total size
tenant_size = fabric_util.get_tenant_total_size()
print(f"Tenant size: {tenant_size:,} bytes")
```

## Documentation

- [FabricUtil API Reference](docs/FabricUtil.md)
- [Examples](examples/fabric_util_example.py)

## License

MIT License - see LICENSE file for details.