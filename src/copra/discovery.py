from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from cocotb.handle import (
    HierarchyArrayObject,
    HierarchyObject,
    SimHandleBase,
)
from .introspection import extract_full_type_info


@dataclass(slots=True)
class HDLNode:
    path: str
    py_type: str
    width: int | None
    is_scope: bool


class HierarchyDict(Dict[str, Any]):
    """A mutating dictionary that builds hierarchy iteratively during discovery."""
    
    def __init__(self) -> None:
        super().__init__()
        self._nodes: Dict[str, HDLNode] = {}
        self._tree: Dict[str, Any] = {}
    
    def add_node(self, obj: SimHandleBase, path: str) -> None:
        """Add a node to the hierarchy, building the tree structure as we go."""
        width: int | None = None
        if hasattr(obj, '__len__'):
            try:
                width = len(obj)  # type: ignore
            except (TypeError, AttributeError):
                width = None
        
        mro_names = [cls.__name__ for cls in type(obj).__mro__]
        is_scope = ('HierarchyObject' in mro_names or 'HierarchyArrayObject' in mro_names)
        
        node = HDLNode(
            path=path,
            py_type=extract_full_type_info(obj),
            width=width,
            is_scope=is_scope,
        )
        self._nodes[path] = node
        self._build_tree_node(node)
    
    def _build_tree_node(self, node: HDLNode) -> None:
        """Build tree structure for a single node as it's discovered."""
        path_parts = node.path.split(".")
        current = self._tree
        
        for i, part in enumerate(path_parts):
            if part not in current:
                current[part] = {"_node": None, "_children": {}}
            
            if i == len(path_parts) - 1:
                current[part]["_node"] = node
            
            current = current[part]["_children"]
    
    def get_nodes(self) -> list[HDLNode]:
        """Get all nodes as a list."""
        return list(self._nodes.values())
    
    def get_tree(self) -> Dict[str, Any]:
        """Get the built tree structure."""
        return self._tree


async def discover(dut: SimHandleBase) -> HierarchyDict:
    """Discover hierarchy iteratively while building, avoiding explore-then-rebuild pattern."""
    dut._discover_all()  # type: ignore
    hierarchy = HierarchyDict()
    await _discover_iterative(dut, hierarchy, "")
    return hierarchy

async def _discover_iterative(
    obj: SimHandleBase, 
    hierarchy: HierarchyDict, 
    path_prefix: str,
    max_depth: int = 50,
    current_depth: int = 0
) -> None:
    """Iteratively discover hierarchy while building the tree structure."""
    if current_depth > max_depth:
        return
    
    obj_name = getattr(obj, "_name", None)
    if obj_name is None:
        return
    
    full_path = f"{path_prefix}.{obj_name}" if path_prefix else obj_name
    
    hierarchy.add_node(obj, full_path)
    
    if isinstance(obj, HierarchyArrayObject):
        try:
            for idx in obj.range:
                child = obj[idx]
                await _discover_iterative(
                    child, 
                    hierarchy, 
                    full_path, 
                    max_depth, 
                    current_depth + 1
                )
        except RuntimeError:
            pass
    elif isinstance(obj, HierarchyObject):
        for child in obj:
            await _discover_iterative(
                child, 
                hierarchy, 
                full_path, 
                max_depth, 
                current_depth + 1
            )
