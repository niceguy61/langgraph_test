"""Filesystem MCP Server for managing lecture content files"""
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.config import settings


class FileSystemMCPServer:
    """MCP Server for filesystem operations related to lecture content"""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or settings.paths.output_dir
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _validate_path(self, path: str) -> Path:
        """Validate and resolve path within base directory"""
        resolved = (self.base_path / path).resolve()

        # Security: ensure path is within base directory
        if not str(resolved).startswith(str(self.base_path.resolve())):
            raise ValueError(f"Path {path} is outside allowed directory")

        return resolved

    # MCP Tool: list_files
    async def list_files(self, directory: str = "", pattern: str = "*") -> Dict[str, Any]:
        """
        List files in a directory

        Args:
            directory: Relative path within output directory
            pattern: Glob pattern for filtering (default: *)

        Returns:
            Dictionary with file listing
        """
        try:
            dir_path = self._validate_path(directory)

            if not dir_path.exists():
                return {"error": f"Directory not found: {directory}", "files": []}

            files = []
            for item in dir_path.glob(pattern):
                stat = item.stat()
                files.append({
                    "name": item.name,
                    "path": str(item.relative_to(self.base_path)),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

            return {
                "directory": directory or "/",
                "files": sorted(files, key=lambda x: (x["type"] == "file", x["name"])),
                "count": len(files)
            }

        except Exception as e:
            return {"error": str(e), "files": []}

    # MCP Tool: read_file
    async def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read content of a file

        Args:
            file_path: Relative path to file

        Returns:
            Dictionary with file content
        """
        try:
            path = self._validate_path(file_path)

            if not path.exists():
                return {"error": f"File not found: {file_path}"}

            if not path.is_file():
                return {"error": f"Not a file: {file_path}"}

            content = path.read_text(encoding="utf-8")

            return {
                "path": file_path,
                "content": content,
                "size": len(content),
                "lines": content.count("\n") + 1
            }

        except Exception as e:
            return {"error": str(e)}

    # MCP Tool: write_file
    async def write_file(
        self,
        file_path: str,
        content: str,
        create_dirs: bool = True
    ) -> Dict[str, Any]:
        """
        Write content to a file

        Args:
            file_path: Relative path to file
            content: Content to write
            create_dirs: Create parent directories if needed

        Returns:
            Dictionary with operation result
        """
        try:
            path = self._validate_path(file_path)

            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(content, encoding="utf-8")

            return {
                "path": file_path,
                "status": "success",
                "size": len(content),
                "created": not path.exists()
            }

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    # MCP Tool: create_week_structure
    async def create_week_structure(self, week: int, days: int = 5) -> Dict[str, Any]:
        """
        Create folder structure for a week

        Args:
            week: Week number
            days: Number of days (default: 5)

        Returns:
            Dictionary with created structure
        """
        try:
            week_dir = self._validate_path(f"week{week}")
            created_dirs = []

            # Create week directory
            week_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(week_dir.relative_to(self.base_path)))

            # Create day directories
            for day in range(1, days + 1):
                day_dir = week_dir / f"day{day}"
                day_dir.mkdir(exist_ok=True)
                created_dirs.append(str(day_dir.relative_to(self.base_path)))

            # Create overview.md placeholder
            overview_path = week_dir / "overview.md"
            if not overview_path.exists():
                overview_path.write_text(f"# Week {week} Overview\n\n", encoding="utf-8")

            return {
                "week": week,
                "days": days,
                "created_directories": created_dirs,
                "status": "success"
            }

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    # MCP Tool: save_curriculum
    async def save_curriculum(self, curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save curriculum to JSON file

        Args:
            curriculum: Curriculum dictionary

        Returns:
            Operation result
        """
        try:
            path = self._validate_path("curriculum.json")

            # Add metadata
            curriculum["_metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            }

            path.write_text(
                json.dumps(curriculum, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            return {
                "path": "curriculum.json",
                "status": "success"
            }

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    # MCP Tool: get_curriculum
    async def get_curriculum(self) -> Dict[str, Any]:
        """
        Load curriculum from JSON file

        Returns:
            Curriculum dictionary
        """
        try:
            path = self._validate_path("curriculum.json")

            if not path.exists():
                return {"error": "Curriculum not found", "exists": False}

            content = json.loads(path.read_text(encoding="utf-8"))
            return {"curriculum": content, "exists": True}

        except Exception as e:
            return {"error": str(e)}

    # MCP Tool: delete_file
    async def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file

        Args:
            file_path: Relative path to file

        Returns:
            Operation result
        """
        try:
            path = self._validate_path(file_path)

            if not path.exists():
                return {"error": f"File not found: {file_path}"}

            if path.is_dir():
                import shutil
                shutil.rmtree(path)
            else:
                path.unlink()

            return {"path": file_path, "status": "deleted"}

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    # MCP Tool: get_output_summary
    async def get_output_summary(self) -> Dict[str, Any]:
        """
        Get summary of all generated content

        Returns:
            Summary dictionary
        """
        try:
            summary = {
                "weeks": [],
                "total_files": 0,
                "total_size": 0
            }

            for week_dir in sorted(self.base_path.glob("week*")):
                if week_dir.is_dir():
                    week_info = {
                        "name": week_dir.name,
                        "days": [],
                        "files": []
                    }

                    for item in week_dir.iterdir():
                        if item.is_dir() and item.name.startswith("day"):
                            day_files = list(item.glob("*.md"))
                            week_info["days"].append({
                                "name": item.name,
                                "files": [f.name for f in day_files]
                            })
                            summary["total_files"] += len(day_files)
                        elif item.is_file():
                            week_info["files"].append(item.name)
                            summary["total_files"] += 1
                            summary["total_size"] += item.stat().st_size

                    summary["weeks"].append(week_info)

            # Check for curriculum.json
            curriculum_path = self.base_path / "curriculum.json"
            summary["has_curriculum"] = curriculum_path.exists()

            return summary

        except Exception as e:
            return {"error": str(e)}

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get MCP tool definitions for this server"""
        return [
            {
                "name": "list_files",
                "description": "List files in a directory within the lecture output folder",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "directory": {"type": "string", "description": "Relative path to directory"},
                        "pattern": {"type": "string", "description": "Glob pattern for filtering"}
                    }
                }
            },
            {
                "name": "read_file",
                "description": "Read content of a lecture file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Relative path to file"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a lecture file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Relative path to file"},
                        "content": {"type": "string", "description": "Content to write"},
                        "create_dirs": {"type": "boolean", "description": "Create parent dirs if needed"}
                    },
                    "required": ["file_path", "content"]
                }
            },
            {
                "name": "create_week_structure",
                "description": "Create folder structure for a week of lectures",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "week": {"type": "integer", "description": "Week number"},
                        "days": {"type": "integer", "description": "Number of days"}
                    },
                    "required": ["week"]
                }
            },
            {
                "name": "save_curriculum",
                "description": "Save curriculum to JSON file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "curriculum": {"type": "object", "description": "Curriculum data"}
                    },
                    "required": ["curriculum"]
                }
            },
            {
                "name": "get_output_summary",
                "description": "Get summary of all generated lecture content",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]
