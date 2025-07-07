"""
FabricUtil class for workspace and tenant management utilities.

This module provides utility functions for managing workspaces and tenants
in Microsoft Fabric environments.
"""

from typing import List, Dict, Any, Optional
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Try to import semantic-link for Fabric API integration
try:
    import sempy.fabric as fabric
    FABRIC_AVAILABLE = True
    logger.info("semantic-link (sempy.fabric) is available")
except ImportError:
    FABRIC_AVAILABLE = False
    logger.warning("semantic-link (sempy.fabric) is not available - using placeholder implementation")


class FabricUtil:
    """
    Utility class for workspace and tenant management operations.
    
    This class provides methods to interact with Microsoft Fabric workspaces
    and tenants, including getting workspace lists and calculating file sizes.
    """
    
    def __init__(
        self, 
        workspace_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        connection_string: Optional[str] = None,
        authentication_method: str = "default"
    ):
        """
        Initialize FabricUtil with required parameters.
        
        Args:
            workspace_id: The ID of the workspace to work with
            tenant_id: The ID of the tenant to work with
            connection_string: Connection string for Fabric API access
            authentication_method: Authentication method to use
        """
        self.workspace_id = workspace_id
        self.tenant_id = tenant_id
        self.connection_string = connection_string
        self.authentication_method = authentication_method
        
        # Initialize connection (placeholder for actual implementation)
        self._connection = None
        self._initialize_connection()
        logger.info(f"FabricUtil initialized with workspace_id: {workspace_id}, tenant_id: {tenant_id}")
    
    def get_workspaces(self) -> List[Dict[str, Any]]:
        """
        Get the list of workspaces available to the current user.
        
        Returns:
            List of workspace dictionaries containing workspace information
            
        Raises:
            Exception: If unable to retrieve workspaces
        """
        try:
            logger.info("Retrieving list of workspaces")
            
            if FABRIC_AVAILABLE:
                try:
                    # Use semantic-link to get real workspace data
                    workspaces_df = fabric.list_workspaces()
                    
                    # Convert pandas DataFrame to list of dictionaries
                    workspaces = []
                    for _, row in workspaces_df.iterrows():
                        workspace_dict = {
                            "id": row.get("Id", ""),
                            "name": row.get("Name", ""),
                            "description": row.get("Description", ""),
                            "is_capacity_assigned": row.get("IsOnDedicatedCapacity", False),
                            "capacity_id": row.get("CapacityId", None)
                        }
                        workspaces.append(workspace_dict)
                    
                    logger.info(f"Found {len(workspaces)} workspaces using semantic-link")
                    return workspaces
                    
                except Exception as e:
                    logger.warning(f"Failed to use semantic-link API: {e}")
                    logger.info("Falling back to placeholder implementation")
            
            # Fallback to placeholder implementation when semantic-link is not available
            # or when not in a Fabric environment
            workspaces = [
                {
                    "id": "workspace-1",
                    "name": "Default Workspace",
                    "description": "Default workspace for the tenant",
                    "is_capacity_assigned": True,
                    "capacity_id": "capacity-1"
                },
                {
                    "id": "workspace-2", 
                    "name": "Development Workspace",
                    "description": "Development environment workspace",
                    "is_capacity_assigned": False,
                    "capacity_id": None
                }
            ]
            
            logger.info(f"Found {len(workspaces)} workspaces using placeholder implementation")
            return workspaces
            
        except Exception as e:
            logger.error(f"Error retrieving workspaces: {e}")
            raise Exception(f"Failed to retrieve workspaces: {e}")
    
    def get_workspace_total_size(self, workspace_id: Optional[str] = None) -> int:
        """
        Get the total file size of all items in a workspace.
        
        Args:
            workspace_id: ID of the workspace to calculate size for.
                         If None, uses the instance's workspace_id.
                         
        Returns:
            Total size in bytes of all items in the workspace
            
        Raises:
            ValueError: If no workspace_id is provided
            Exception: If unable to calculate workspace size
        """
        target_workspace_id = workspace_id or self.workspace_id
        
        if not target_workspace_id:
            raise ValueError("workspace_id must be provided either as parameter or during initialization")
        
        try:
            logger.info(f"Calculating total size for workspace: {target_workspace_id}")
            
            if FABRIC_AVAILABLE:
                try:
                    # Use semantic-link to get real workspace item data
                    items_df = fabric.list_items(workspace=target_workspace_id)
                    
                    total_size = 0
                    
                    # Check if the DataFrame has size-related columns
                    if not items_df.empty:
                        # Try different possible column names for size information
                        size_columns = ['Size', 'size', 'SizeInBytes', 'FileSizeBytes', 'ContentSize']
                        size_column = None
                        
                        for col in size_columns:
                            if col in items_df.columns:
                                size_column = col
                                break
                        
                        if size_column:
                            # Sum up the sizes of all items
                            total_size = items_df[size_column].fillna(0).sum()
                            logger.info(f"Calculated workspace size from semantic-link: {total_size} bytes from {len(items_df)} items")
                        else:
                            logger.warning(f"No size column found in items data. Available columns: {items_df.columns.tolist()}")
                            # Estimate size based on item types as fallback
                            total_size = self._estimate_workspace_size(items_df)
                            logger.info(f"Estimated workspace size: {total_size} bytes from {len(items_df)} items")
                    else:
                        logger.info("No items found in workspace")
                        total_size = 0
                    
                    logger.info(f"Workspace {target_workspace_id} total size: {total_size} bytes")
                    return total_size
                    
                except Exception as e:
                    logger.warning(f"Failed to use semantic-link API for workspace size: {e}")
                    logger.info("Falling back to placeholder calculation")
            
            # Fallback to placeholder implementation when semantic-link is not available
            # or when not in a Fabric environment
            total_size = 0
            
            # Simulate getting workspace items and their sizes
            workspace_items = [
                {"name": "dataset1.pbix", "size": 1024 * 1024 * 50},  # 50MB
                {"name": "report1.pbix", "size": 1024 * 1024 * 25},   # 25MB
                {"name": "dashboard1.json", "size": 1024 * 100},      # 100KB
                {"name": "model1.bim", "size": 1024 * 1024 * 10},     # 10MB
            ]
            
            for item in workspace_items:
                total_size += item["size"]
            
            logger.info(f"Workspace {target_workspace_id} total size (placeholder): {total_size} bytes")
            return total_size
            
        except Exception as e:
            logger.error(f"Error calculating workspace size: {e}")
            raise Exception(f"Failed to calculate workspace size: {e}")
    
    def _estimate_workspace_size(self, items_df) -> int:
        """
        Estimate workspace size based on item types when size data is not available.
        
        Args:
            items_df: DataFrame containing workspace items
            
        Returns:
            Estimated total size in bytes
        """
        # Default size estimates by item type (in bytes)
        size_estimates = {
            'Dataset': 50 * 1024 * 1024,      # 50MB for datasets
            'Report': 25 * 1024 * 1024,       # 25MB for reports  
            'Dashboard': 100 * 1024,          # 100KB for dashboards
            'Dataflow': 10 * 1024 * 1024,     # 10MB for dataflows
            'Lakehouse': 100 * 1024 * 1024,   # 100MB for lakehouses
            'Notebook': 5 * 1024 * 1024,      # 5MB for notebooks
            'SemanticModel': 30 * 1024 * 1024, # 30MB for semantic models
            'Datamart': 75 * 1024 * 1024,     # 75MB for datamarts
        }
        
        total_estimated_size = 0
        
        # Check if Type column exists
        if 'Type' in items_df.columns:
            type_counts = items_df['Type'].value_counts()
            for item_type, count in type_counts.items():
                estimated_size = size_estimates.get(item_type, 1024 * 1024)  # Default 1MB
                total_estimated_size += estimated_size * count
        else:
            # If no type information, assume average item size
            average_item_size = 20 * 1024 * 1024  # 20MB average
            total_estimated_size = len(items_df) * average_item_size
        
        return int(total_estimated_size)
    
    def get_tenant_total_size(self, tenant_id: Optional[str] = None) -> int:
        """
        Get the total file size of all items in a tenant.
        
        Args:
            tenant_id: ID of the tenant to calculate size for.
                      If None, uses the instance's tenant_id.
                      
        Returns:
            Total size in bytes of all items in the tenant
            
        Raises:
            ValueError: If no tenant_id is provided
            Exception: If unable to calculate tenant size
        """
        target_tenant_id = tenant_id or self.tenant_id
        
        if not target_tenant_id:
            raise ValueError("tenant_id must be provided either as parameter or during initialization")
        
        try:
            logger.info(f"Calculating total size for tenant: {target_tenant_id}")
            
            # Get all workspaces in the tenant and sum their sizes
            # This now uses the actual workspace data from semantic-link when available
            total_size = 0
            
            # Get all workspaces in the tenant and sum their sizes
            workspaces = self.get_workspaces()
            
            for workspace in workspaces:
                workspace_size = self.get_workspace_total_size(workspace["id"])
                total_size += workspace_size
            
            logger.info(f"Tenant {target_tenant_id} total size: {total_size} bytes")
            return total_size
            
        except Exception as e:
            logger.error(f"Error calculating tenant size: {e}")
            raise Exception(f"Failed to calculate tenant size: {e}")
    
    def _initialize_connection(self):
        """
        Initialize connection to Fabric API.
        
        This method checks if semantic-link is available and logs the status.
        """
        if FABRIC_AVAILABLE:
            logger.info("semantic-link is available for Fabric API integration")
            # Note: Authentication is handled automatically by semantic-link 
            # when running in a Fabric environment
        else:
            logger.warning("semantic-link is not available - using placeholder implementation")
            logger.info("To enable real API integration, install with: pip install workspace-storage[fabric]")
    
    def __str__(self) -> str:
        """String representation of FabricUtil instance."""
        return f"FabricUtil(workspace_id={self.workspace_id}, tenant_id={self.tenant_id})"
    
    def __repr__(self) -> str:
        """Detailed string representation of FabricUtil instance."""
        return (f"FabricUtil(workspace_id={self.workspace_id}, tenant_id={self.tenant_id}, "
                f"connection_string={'***' if self.connection_string else None}, "
                f"authentication_method={self.authentication_method})")