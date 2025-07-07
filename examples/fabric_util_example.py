"""
Example usage of the FabricUtil class.

This script demonstrates how to use the FabricUtil class for workspace
and tenant management operations.
"""

import sys
import os
import logging

# Add the src directory to the path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from workspace_storage import FabricUtil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    """Main example function demonstrating FabricUtil usage."""
    print("FabricUtil Example Usage")
    print("========================\n")
    
    # Example 1: Initialize FabricUtil with workspace and tenant IDs
    print("1. Creating FabricUtil instance...")
    fabric_util = FabricUtil(
        workspace_id="my-workspace-id",
        tenant_id="my-tenant-id",
        connection_string="DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey",
        authentication_method="service_principal"
    )
    print(f"   Created: {fabric_util}")
    
    # Example 2: Get list of workspaces
    print("\n2. Getting list of workspaces...")
    try:
        workspaces = fabric_util.get_workspaces()
        print(f"   Found {len(workspaces)} workspaces:")
        for workspace in workspaces:
            print(f"     • {workspace['name']} (ID: {workspace['id']})")
            print(f"       Description: {workspace['description']}")
            print(f"       Capacity assigned: {workspace['is_capacity_assigned']}")
            if workspace['capacity_id']:
                print(f"       Capacity ID: {workspace['capacity_id']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Get workspace total size
    print("\n3. Getting workspace total size...")
    try:
        workspace_size = fabric_util.get_workspace_total_size()
        print(f"   Workspace size: {workspace_size:,} bytes")
        print(f"   That's {workspace_size / (1024*1024):.2f} MB")
        print(f"   Or {workspace_size / (1024*1024*1024):.2f} GB")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 4: Get size of a specific workspace
    print("\n4. Getting size of a specific workspace...")
    try:
        specific_workspace_size = fabric_util.get_workspace_total_size("workspace-1")
        print(f"   Workspace 'workspace-1' size: {specific_workspace_size:,} bytes")
        print(f"   That's {specific_workspace_size / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 5: Get tenant total size
    print("\n5. Getting tenant total size...")
    try:
        tenant_size = fabric_util.get_tenant_total_size()
        print(f"   Tenant size: {tenant_size:,} bytes")
        print(f"   That's {tenant_size / (1024*1024):.2f} MB")
        print(f"   Or {tenant_size / (1024*1024*1024):.2f} GB")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 6: Error handling demonstration
    print("\n6. Demonstrating error handling...")
    try:
        # Create FabricUtil without workspace_id
        util_no_workspace = FabricUtil(tenant_id="my-tenant-id")
        # This should raise a ValueError
        util_no_workspace.get_workspace_total_size()
    except ValueError as e:
        print(f"   Correctly caught error: {e}")
    except Exception as e:
        print(f"   Unexpected error: {e}")
    
    # Example 7: Using with different authentication methods
    print("\n7. Different authentication methods...")
    auth_methods = ["default", "service_principal", "interactive", "device_code"]
    
    for method in auth_methods:
        print(f"   • {method} authentication:")
        try:
            util = FabricUtil(
                workspace_id="demo-workspace",
                tenant_id="demo-tenant",
                authentication_method=method
            )
            print(f"     Created FabricUtil with {method} auth")
        except Exception as e:
            print(f"     Error with {method} auth: {e}")
    
    print("\n" + "="*50)
    print("Example completed successfully!")
    print("\nNote: This example uses placeholder data.")
    print("In a real implementation, you would:")
    print("- Connect to actual Microsoft Fabric APIs")
    print("- Use real workspace and tenant IDs")
    print("- Handle authentication properly")
    print("- Process real file sizes and metadata")


if __name__ == "__main__":
    main()