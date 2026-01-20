"""File Writer Tool for LangChain agents"""
from typing import Type
from pathlib import Path
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import settings


class FileWriteInput(BaseModel):
    """Input schema for file writing"""
    file_path: str = Field(description="Relative path within output directory")
    content: str = Field(description="Content to write to the file")
    create_dirs: bool = Field(default=True, description="Create parent directories if needed")


class FileWriterTool(BaseTool):
    """Tool for writing files to the output directory"""

    name: str = "write_file"
    description: str = "Write content to a file in the output directory. Use this to save generated lecture content."
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, file_path: str, content: str, create_dirs: bool = True) -> str:
        """Write content to file"""
        try:
            base_path = settings.paths.output_dir
            full_path = base_path / file_path

            # Security check
            if not str(full_path.resolve()).startswith(str(base_path.resolve())):
                return f"Error: Path {file_path} is outside allowed directory"

            # Create directories if needed
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            full_path.write_text(content, encoding="utf-8")

            return f"Successfully wrote {len(content)} characters to {file_path}"

        except Exception as e:
            return f"Error writing file: {e}"

    async def _arun(self, file_path: str, content: str, create_dirs: bool = True) -> str:
        """Async version (uses sync implementation)"""
        return self._run(file_path, content, create_dirs)


class FileReadInput(BaseModel):
    """Input schema for file reading"""
    file_path: str = Field(description="Relative path within output directory")


class FileReaderTool(BaseTool):
    """Tool for reading files from the output directory"""

    name: str = "read_file"
    description: str = "Read content from a file in the output directory."
    args_schema: Type[BaseModel] = FileReadInput

    def _run(self, file_path: str) -> str:
        """Read content from file"""
        try:
            base_path = settings.paths.output_dir
            full_path = base_path / file_path

            # Security check
            if not str(full_path.resolve()).startswith(str(base_path.resolve())):
                return f"Error: Path {file_path} is outside allowed directory"

            if not full_path.exists():
                return f"Error: File {file_path} does not exist"

            content = full_path.read_text(encoding="utf-8")
            return content

        except Exception as e:
            return f"Error reading file: {e}"

    async def _arun(self, file_path: str) -> str:
        """Async version (uses sync implementation)"""
        return self._run(file_path)


class ListFilesInput(BaseModel):
    """Input schema for listing files"""
    directory: str = Field(default="", description="Relative directory path")
    pattern: str = Field(default="*", description="Glob pattern for filtering")


class ListFilesTool(BaseTool):
    """Tool for listing files in the output directory"""

    name: str = "list_files"
    description: str = "List files in the output directory."
    args_schema: Type[BaseModel] = ListFilesInput

    def _run(self, directory: str = "", pattern: str = "*") -> str:
        """List files in directory"""
        try:
            base_path = settings.paths.output_dir
            dir_path = base_path / directory

            # Security check
            if not str(dir_path.resolve()).startswith(str(base_path.resolve())):
                return f"Error: Path {directory} is outside allowed directory"

            if not dir_path.exists():
                return f"Directory {directory} does not exist"

            files = list(dir_path.glob(pattern))
            file_list = []

            for f in sorted(files):
                rel_path = f.relative_to(base_path)
                file_type = "DIR" if f.is_dir() else "FILE"
                file_list.append(f"[{file_type}] {rel_path}")

            if file_list:
                return "\n".join(file_list)
            return "No files found"

        except Exception as e:
            return f"Error listing files: {e}"

    async def _arun(self, directory: str = "", pattern: str = "*") -> str:
        """Async version (uses sync implementation)"""
        return self._run(directory, pattern)
