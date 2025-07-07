"""
Simple test script to validate FabricUtil functionality.

This script tests the basic functionality of the FabricUtil class
without requiring external dependencies.
"""

import sys
import os
import logging

# Add the src directory to the path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from workspace_storage import FabricUtil

# Configure logging to see debug information
logging.basicConfig(level=logging.INFO)


def test_fabric_util():
    """Test basic FabricUtil functionality."""
    print("Testing FabricUtil class...")
    
    # Test 1: Basic initialization
    print("\n1. Testing basic initialization...")
    util = FabricUtil(
        workspace_id="test-workspace-1",
        tenant_id="test-tenant-1",
        connection_string="test-connection",
        authentication_method="test-auth"
    )
    print(f"   Created FabricUtil: {util}")
    print(f"   Representation: {repr(util)}")
    
    # Test 2: Get workspaces
    print("\n2. Testing get_workspaces()...")
    workspaces = util.get_workspaces()
    print(f"   Found {len(workspaces)} workspaces:")
    for workspace in workspaces:
        print(f"     - {workspace['name']} (ID: {workspace['id']})")
    
    # Test 3: Get workspace total size
    print("\n3. Testing get_workspace_total_size()...")
    workspace_size = util.get_workspace_total_size()
    print(f"   Workspace size: {workspace_size:,} bytes ({workspace_size / (1024*1024):.2f} MB)")
    
    # Test 4: Get workspace total size with different workspace ID
    print("\n4. Testing get_workspace_total_size() with specific workspace ID...")
    workspace_size_2 = util.get_workspace_total_size("workspace-2")
    print(f"   Workspace-2 size: {workspace_size_2:,} bytes ({workspace_size_2 / (1024*1024):.2f} MB)")
    
    # Test 5: Get tenant total size
    print("\n5. Testing get_tenant_total_size()...")
    tenant_size = util.get_tenant_total_size()
    print(f"   Tenant size: {tenant_size:,} bytes ({tenant_size / (1024*1024):.2f} MB)")
    
    # Test 6: Error handling - no workspace ID
    print("\n6. Testing error handling...")
    try:
        util_no_ids = FabricUtil()
        util_no_ids.get_workspace_total_size()
        print("   ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"   Correctly raised ValueError: {e}")
    
    # Test 7: Error handling - no tenant ID
    try:
        util_no_ids = FabricUtil()
        util_no_ids.get_tenant_total_size()
        print("   ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"   Correctly raised ValueError: {e}")
    
    print("\nAll tests completed successfully!")
    return True


if __name__ == "__main__":
    try:
        test_fabric_util()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)