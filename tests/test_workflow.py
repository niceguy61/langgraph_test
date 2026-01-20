"""Tests for LangGraph workflow"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock


class TestGraphState:
    """Tests for GraphState"""

    def test_create_initial_state(self):
        """Test initial state creation"""
        from src.graph.state import create_initial_state

        state = create_initial_state(
            request="Test request",
            target_week=1,
            target_day=1
        )

        assert state["request"] == "Test request"
        assert state["target_week"] == 1
        assert state["target_day"] == 1
        assert state["current_step"] == "start"
        assert state["completed_tasks"] == []

    def test_create_initial_state_defaults(self):
        """Test initial state with default values"""
        from src.graph.state import create_initial_state

        state = create_initial_state(request="Test")

        assert state["target_week"] is None
        assert state["target_day"] is None
        assert state["max_iterations"] == 10


class TestWorkflowRouting:
    """Tests for workflow routing functions"""

    def test_route_supervisor_curriculum(self):
        """Test routing to curriculum designer"""
        from src.graph.workflow import route_supervisor

        state = {"next_agent": "curriculum_designer", "iteration_count": 0}
        result = route_supervisor(state)
        assert result == "curriculum_designer"

    def test_route_supervisor_content(self):
        """Test routing to content generator"""
        from src.graph.workflow import route_supervisor

        state = {"next_agent": "content_generator", "iteration_count": 0}
        result = route_supervisor(state)
        assert result == "content_generator"

    def test_route_supervisor_finish(self):
        """Test routing to finalize"""
        from src.graph.workflow import route_supervisor

        state = {"next_agent": "FINISH", "iteration_count": 0}
        result = route_supervisor(state)
        assert result == "finalize"

    def test_route_supervisor_max_iterations(self):
        """Test routing when max iterations reached"""
        from src.graph.workflow import route_supervisor

        state = {
            "next_agent": "content_generator",
            "iteration_count": 10,
            "max_iterations": 10
        }
        result = route_supervisor(state)
        assert result == "finalize"

    def test_route_supervisor_error(self):
        """Test routing when error occurred"""
        from src.graph.workflow import route_supervisor

        state = {
            "next_agent": "content_generator",
            "iteration_count": 0,
            "error": "Some error"
        }
        result = route_supervisor(state)
        assert result == "finalize"

    def test_should_continue_after_review(self):
        """Test continuation decision after review"""
        from src.graph.workflow import should_continue

        state = {
            "current_step": "reviewed",
            "completed_tasks": ["review"],
            "needs_revision": False
        }
        result = should_continue(state)
        assert result == "finalize"

    def test_should_continue_needs_revision(self):
        """Test continuation when revision needed"""
        from src.graph.workflow import should_continue

        state = {
            "current_step": "reviewed",
            "completed_tasks": ["review"],
            "needs_revision": True
        }
        result = should_continue(state)
        assert result == "supervisor"


class TestWorkflowCreation:
    """Tests for workflow creation"""

    def test_create_workflow(self):
        """Test workflow graph creation"""
        from src.graph.workflow import create_workflow

        workflow = create_workflow()
        assert workflow is not None

    def test_compile_workflow(self):
        """Test workflow compilation"""
        from src.graph.workflow import compile_workflow

        app = compile_workflow()
        assert app is not None


class TestVectorStore:
    """Tests for VectorStore"""

    def test_vectorstore_manager_init(self):
        """Test VectorStoreManager initialization"""
        from src.rag import VectorStoreManager

        manager = VectorStoreManager()
        assert manager.collection_name is not None

    def test_load_markdown_documents_empty_dir(self, tmp_path):
        """Test loading from empty directory"""
        from src.rag import VectorStoreManager

        manager = VectorStoreManager()
        docs = manager.load_markdown_documents(tmp_path)
        assert docs == []

    def test_load_markdown_documents(self, tmp_path):
        """Test loading markdown documents"""
        from src.rag import VectorStoreManager

        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content\n\nThis is test content.")

        manager = VectorStoreManager()
        docs = manager.load_markdown_documents(tmp_path)

        assert len(docs) == 1
        assert "Test Content" in docs[0].page_content


class TestMCPServers:
    """Tests for MCP servers"""

    @pytest.fixture
    def fs_server(self, tmp_path):
        from src.mcp import FileSystemMCPServer
        return FileSystemMCPServer(base_path=tmp_path)

    @pytest.mark.asyncio
    async def test_list_files_empty(self, fs_server):
        """Test listing files in empty directory"""
        result = await fs_server.list_files()
        assert "files" in result
        assert result["count"] == 0

    @pytest.mark.asyncio
    async def test_write_and_read_file(self, fs_server):
        """Test writing and reading a file"""
        # Write file
        write_result = await fs_server.write_file(
            "test.md",
            "# Test\n\nContent here"
        )
        assert write_result["status"] == "success"

        # Read file
        read_result = await fs_server.read_file("test.md")
        assert "Content here" in read_result["content"]

    @pytest.mark.asyncio
    async def test_create_week_structure(self, fs_server):
        """Test creating week structure"""
        result = await fs_server.create_week_structure(1, 5)
        assert result["status"] == "success"
        assert result["week"] == 1
        assert len(result["created_directories"]) > 0

    @pytest.mark.asyncio
    async def test_path_validation(self, fs_server):
        """Test path validation security"""
        with pytest.raises(ValueError):
            fs_server._validate_path("../outside/path")


class TestAWSMCPServer:
    """Tests for AWS MCP server"""

    @pytest.fixture
    def aws_server(self):
        from src.mcp import AWSMCPServer
        return AWSMCPServer()

    @pytest.mark.asyncio
    async def test_get_service_info(self, aws_server):
        """Test getting service info"""
        result = await aws_server.get_service_info("EC2")
        assert "info" in result
        assert result["info"]["category"] == "Compute"

    @pytest.mark.asyncio
    async def test_get_service_info_unknown(self, aws_server):
        """Test getting info for unknown service"""
        result = await aws_server.get_service_info("UnknownService")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_list_ec2_mock(self, aws_server):
        """Test EC2 listing with mock data"""
        result = await aws_server.list_ec2_instances()
        assert "instances" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
