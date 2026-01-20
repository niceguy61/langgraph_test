"""Tests for agent implementations"""
import pytest
import asyncio
from unittest.mock import MagicMock, patch


class TestCurriculumDesignerAgent:
    """Tests for CurriculumDesignerAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import CurriculumDesignerAgent
        return CurriculumDesignerAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "curriculum_designer"
        assert agent.description is not None

    def test_system_prompt(self, agent):
        """Test system prompt is defined"""
        assert agent.system_prompt is not None
        assert "커리큘럼" in agent.system_prompt or "curriculum" in agent.system_prompt.lower()

    @pytest.mark.asyncio
    async def test_parse_curriculum_json(self, agent):
        """Test JSON parsing from LLM response"""
        valid_response = '''
        Some text before
        {
            "title": "AWS 기초",
            "weeks": []
        }
        Some text after
        '''
        result = agent._parse_curriculum_json(valid_response)
        assert "title" in result
        assert result["title"] == "AWS 기초"

    @pytest.mark.asyncio
    async def test_parse_curriculum_json_invalid(self, agent):
        """Test JSON parsing with invalid input"""
        invalid_response = "This is not JSON at all"
        result = agent._parse_curriculum_json(invalid_response)
        assert "error" in result or "raw_response" in result


class TestContentGeneratorAgent:
    """Tests for ContentGeneratorAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import ContentGeneratorAgent
        return ContentGeneratorAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "content_generator"

    def test_get_week_data(self, agent):
        """Test extracting week data from curriculum"""
        curriculum = {
            "weeks": [
                {"week": 1, "title": "Week 1 Title"},
                {"week": 2, "title": "Week 2 Title"}
            ]
        }
        result = agent._get_week_data(curriculum, 1)
        assert result is not None
        assert result["title"] == "Week 1 Title"

    def test_get_week_data_not_found(self, agent):
        """Test when week is not found"""
        curriculum = {"weeks": []}
        result = agent._get_week_data(curriculum, 99)
        assert result is None


class TestReviewerAgent:
    """Tests for ReviewerAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import ReviewerAgent
        return ReviewerAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "reviewer"

    def test_parse_review_json(self, agent):
        """Test review JSON parsing"""
        valid_response = '''
        {
            "accuracy_score": 85,
            "overall_score": 82,
            "strengths": ["Good content"],
            "improvements": ["Add more examples"]
        }
        '''
        result = agent._parse_review_json(valid_response)
        assert result["accuracy_score"] == 85
        assert "strengths" in result


class TestSupervisorAgent:
    """Tests for SupervisorAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import SupervisorAgent
        return SupervisorAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "supervisor"
        assert len(agent.AGENT_OPTIONS) > 0

    def test_parse_agent_response(self, agent):
        """Test parsing agent routing response"""
        assert agent._parse_agent_response("curriculum_designer") == "curriculum_designer"
        assert agent._parse_agent_response("I think we should use content_generator") == "content_generator"
        assert agent._parse_agent_response("Unknown response") == "FINISH"


class TestWebSearcherAgent:
    """Tests for WebSearcherAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import WebSearcherAgent
        return WebSearcherAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "web_searcher"

    @pytest.mark.asyncio
    async def test_generate_search_queries(self, agent):
        """Test search query generation"""
        curriculum = {
            "weeks": [
                {"week": 1, "services": ["EC2", "S3"]}
            ]
        }
        queries = await agent._generate_search_queries(curriculum, 1, "")
        assert len(queries) > 0


class TestRAGSearcherAgent:
    """Tests for RAGSearcherAgent"""

    @pytest.fixture
    def agent(self):
        from src.agents import RAGSearcherAgent
        return RAGSearcherAgent()

    def test_agent_initialization(self, agent):
        """Test agent is properly initialized"""
        assert agent.name == "rag_searcher"

    def test_generate_queries(self, agent):
        """Test query generation"""
        curriculum = {
            "weeks": [
                {
                    "week": 1,
                    "title": "AWS 기초",
                    "services": ["EC2"],
                    "days": [{"topics": ["인스턴스"]}]
                }
            ]
        }
        queries = agent._generate_queries(curriculum, 1)
        assert len(queries) > 0
        assert "AWS 기초" in queries or "AWS EC2" in queries


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
