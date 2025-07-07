# FabricUtil

A utility class for Microsoft Fabric workspace and tenant management operations.

## Overview

The `FabricUtil` class provides convenient methods for:
- Getting the list of workspaces
- Calculating total file sizes for workspaces
- Calculating total file sizes for tenants
- Managing workspace and tenant operations

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
    tenant_id="your-tenant-id",
    connection_string="your-connection-string",
    authentication_method="service_principal"
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

## API Reference

### FabricUtil Class

#### Constructor

```python
FabricUtil(
    workspace_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    connection_string: Optional[str] = None,
    authentication_method: str = "default"
)
```

**Parameters:**
- `workspace_id` (optional): The ID of the workspace to work with
- `tenant_id` (optional): The ID of the tenant to work with
- `connection_string` (optional): Connection string for Fabric API access
- `authentication_method` (optional): Authentication method to use (default: "default")

#### Methods

##### get_workspaces()

Get the list of workspaces available to the current user.

```python
workspaces = fabric_util.get_workspaces()
```

**Returns:** List of workspace dictionaries containing:
- `id`: Workspace ID
- `name`: Workspace name
- `description`: Workspace description
- `is_capacity_assigned`: Whether capacity is assigned
- `capacity_id`: Capacity ID (if assigned)

##### get_workspace_total_size(workspace_id=None)

Get the total file size of all items in a workspace.

```python
size = fabric_util.get_workspace_total_size()
# or
size = fabric_util.get_workspace_total_size("specific-workspace-id")
```

**Parameters:**
- `workspace_id` (optional): ID of the workspace to calculate size for. If None, uses the instance's workspace_id.

**Returns:** Total size in bytes of all items in the workspace

##### get_tenant_total_size(tenant_id=None)

Get the total file size of all items in a tenant.

```python
size = fabric_util.get_tenant_total_size()
# or
size = fabric_util.get_tenant_total_size("specific-tenant-id")
```

**Parameters:**
- `tenant_id` (optional): ID of the tenant to calculate size for. If None, uses the instance's tenant_id.

**Returns:** Total size in bytes of all items in the tenant

## Examples

### Basic Usage

```python
from workspace_storage import FabricUtil

# Create FabricUtil instance
fabric_util = FabricUtil(
    workspace_id="my-workspace",
    tenant_id="my-tenant"
)

# Get workspaces
workspaces = fabric_util.get_workspaces()
for workspace in workspaces:
    print(f"Workspace: {workspace['name']} (ID: {workspace['id']})")

# Get sizes
workspace_size = fabric_util.get_workspace_total_size()
tenant_size = fabric_util.get_tenant_total_size()

print(f"Workspace size: {workspace_size / (1024*1024):.2f} MB")
print(f"Tenant size: {tenant_size / (1024*1024):.2f} MB")
```

### Different Authentication Methods

```python
# Service Principal authentication
fabric_util = FabricUtil(
    workspace_id="my-workspace",
    tenant_id="my-tenant",
    authentication_method="service_principal"
)

# Interactive authentication
fabric_util = FabricUtil(
    workspace_id="my-workspace",
    tenant_id="my-tenant",
    authentication_method="interactive"
)
```

### Error Handling

```python
from workspace_storage import FabricUtil

try:
    fabric_util = FabricUtil()  # No workspace_id provided
    size = fabric_util.get_workspace_total_size()
except ValueError as e:
    print(f"Error: {e}")
```

## Implementation Notes

### Current Implementation

The current implementation provides a working framework with placeholder data. It demonstrates:
- Class structure and method signatures
- Error handling patterns
- Logging integration
- Parameter validation

### Future Enhancements

When `semantic-link` is available, the implementation will be enhanced to:
- Connect to actual Microsoft Fabric APIs
- Retrieve real workspace and tenant data
- Process actual file sizes and metadata
- Support various authentication methods

### Dependencies

- **Required**: Python 3.12+
- **Optional**: `semantic-link` (for Microsoft Fabric integration)

## License

MIT License - see LICENSE file for details.