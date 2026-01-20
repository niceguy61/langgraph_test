"""Configuration management for AWS Lecture Generator"""
import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class OllamaConfig(BaseModel):
    """Ollama LLM configuration"""
    host: str = Field(default_factory=lambda: os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    model: str = Field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "qwen3:8b"))
    embedding_model: str = Field(default="nomic-embed-text")
    temperature: float = 0.7
    num_ctx: int = 8192


class ChromaConfig(BaseModel):
    """ChromaDB configuration"""
    host: str = Field(default_factory=lambda: os.getenv("CHROMA_HOST", "http://localhost:8000"))
    collection_name: str = Field(default_factory=lambda: os.getenv("CHROMA_COLLECTION", "aws_lectures"))


class PathConfig(BaseModel):
    """Path configuration"""
    output_dir: Path = Field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "./output")))
    data_dir: Path = Field(default_factory=lambda: Path(os.getenv("DATA_DIR", "./data/documents")))

    def ensure_dirs(self):
        """Ensure all directories exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)


class CurriculumConfig(BaseModel):
    """Curriculum configuration"""
    total_weeks: int = 4
    days_per_week: int = 5

    # SAA-C03 기준 50+ 서비스를 4주(20일)에 배치
    # Week topics with daily service breakdown
    week_topics: dict = Field(default_factory=lambda: {
        1: {
            "title": "AWS 기초, IAM & 컴퓨팅",
            "description": "AWS 클라우드의 기본 개념, 보안 기초, 핵심 컴퓨팅 서비스",
            "services": ["IAM", "EC2", "VPC", "ELB", "Auto Scaling", "EBS", "AMI", "Security Groups"],
            "days": {
                1: {
                    "title": "AWS 클라우드 개요 & IAM 기초",
                    "services": ["AWS Global Infrastructure", "IAM"],
                    "topics": ["리전/AZ/엣지 로케이션", "IAM 사용자/그룹/역할", "IAM 정책", "MFA", "AWS Organizations"]
                },
                2: {
                    "title": "IAM 심화 & 보안",
                    "services": ["IAM", "AWS Organizations", "AWS Control Tower"],
                    "topics": ["IAM 역할 위임", "STS", "자격 증명 연동", "서비스 연결 역할", "권한 경계", "SCP"]
                },
                3: {
                    "title": "EC2 기초",
                    "services": ["EC2", "AMI", "EBS"],
                    "topics": ["인스턴스 유형", "구매 옵션(온디맨드/예약/스팟/전용)", "AMI", "사용자 데이터", "인스턴스 메타데이터"]
                },
                4: {
                    "title": "EC2 스토리지 & 네트워킹",
                    "services": ["EBS", "EFS", "Instance Store", "Security Groups"],
                    "topics": ["EBS 볼륨 유형(gp3/io2/st1/sc1)", "EBS 스냅샷", "EFS", "Instance Store", "보안 그룹", "ENI"]
                },
                5: {
                    "title": "고가용성 & 확장성",
                    "services": ["ELB", "Auto Scaling", "Launch Templates"],
                    "topics": ["ALB/NLB/GLB/CLB", "대상 그룹", "상태 검사", "Auto Scaling 그룹", "조정 정책", "시작 템플릿"]
                }
            }
        },
        2: {
            "title": "네트워킹 & 스토리지",
            "description": "VPC 네트워킹 심화와 다양한 스토리지 서비스",
            "services": ["VPC", "S3", "Route 53", "CloudFront", "Global Accelerator", "Storage Gateway"],
            "days": {
                1: {
                    "title": "VPC 기초",
                    "services": ["VPC", "Subnet", "Internet Gateway", "NAT Gateway"],
                    "topics": ["VPC CIDR", "퍼블릭/프라이빗 서브넷", "라우팅 테이블", "인터넷 게이트웨이", "NAT 게이트웨이/인스턴스"]
                },
                2: {
                    "title": "VPC 심화",
                    "services": ["VPC Peering", "Transit Gateway", "VPC Endpoints", "PrivateLink"],
                    "topics": ["VPC 피어링", "Transit Gateway", "VPC 엔드포인트(게이트웨이/인터페이스)", "PrivateLink", "VPN", "Direct Connect"]
                },
                3: {
                    "title": "VPC 보안 & 모니터링",
                    "services": ["NACL", "Security Groups", "VPC Flow Logs", "Network Firewall"],
                    "topics": ["NACL vs 보안 그룹", "VPC 흐름 로그", "Network Firewall", "WAF", "Shield", "Firewall Manager"]
                },
                4: {
                    "title": "S3 기초 & 보안",
                    "services": ["S3", "S3 Glacier"],
                    "topics": ["버킷 정책", "ACL", "S3 암호화(SSE-S3/SSE-KMS/SSE-C)", "버전 관리", "MFA Delete", "S3 Object Lock"]
                },
                5: {
                    "title": "S3 심화 & CDN",
                    "services": ["S3", "CloudFront", "Route 53", "Global Accelerator"],
                    "topics": ["S3 스토리지 클래스", "수명주기 정책", "S3 복제(CRR/SRR)", "CloudFront 배포", "Route 53 라우팅 정책", "Global Accelerator"]
                }
            }
        },
        3: {
            "title": "데이터베이스 & 서버리스",
            "description": "관리형 데이터베이스 서비스와 서버리스 아키텍처",
            "services": ["RDS", "Aurora", "DynamoDB", "ElastiCache", "Lambda", "API Gateway", "Step Functions"],
            "days": {
                1: {
                    "title": "RDS & Aurora",
                    "services": ["RDS", "Aurora"],
                    "topics": ["RDS 다중 AZ", "읽기 전용 복제본", "RDS Proxy", "Aurora 클러스터", "Aurora Serverless", "Aurora Global Database"]
                },
                2: {
                    "title": "DynamoDB",
                    "services": ["DynamoDB", "DAX", "DynamoDB Streams"],
                    "topics": ["파티션 키/정렬 키", "GSI/LSI", "용량 모드(프로비저닝/온디맨드)", "DAX", "DynamoDB Streams", "글로벌 테이블", "TTL"]
                },
                3: {
                    "title": "기타 데이터베이스 서비스",
                    "services": ["ElastiCache", "Redshift", "Neptune", "DocumentDB", "Keyspaces", "QLDB", "Timestream"],
                    "topics": ["ElastiCache Redis/Memcached", "Redshift", "Neptune", "DocumentDB", "Amazon Keyspaces", "QLDB", "Timestream"]
                },
                4: {
                    "title": "Lambda & 서버리스",
                    "services": ["Lambda", "API Gateway", "SAM"],
                    "topics": ["Lambda 함수", "실행 역할", "VPC 내 Lambda", "Lambda@Edge", "API Gateway REST/HTTP/WebSocket", "Lambda 계층"]
                },
                5: {
                    "title": "서버리스 심화",
                    "services": ["Step Functions", "EventBridge", "SQS", "SNS", "Kinesis"],
                    "topics": ["Step Functions", "EventBridge", "SQS 표준/FIFO", "SNS", "Kinesis Data Streams/Firehose/Analytics"]
                }
            }
        },
        4: {
            "title": "컨테이너, 보안 & 아키텍처",
            "description": "컨테이너 서비스, 보안 서비스, 모니터링 및 Well-Architected",
            "services": ["ECS", "EKS", "Fargate", "ECR", "KMS", "Secrets Manager", "CloudWatch", "CloudTrail", "Config"],
            "days": {
                1: {
                    "title": "컨테이너 서비스",
                    "services": ["ECS", "EKS", "Fargate", "ECR", "App Runner", "Copilot"],
                    "topics": ["ECS 클러스터/서비스/태스크", "EKS", "Fargate", "ECR", "App Runner", "ECS Anywhere"]
                },
                2: {
                    "title": "보안 서비스",
                    "services": ["KMS", "CloudHSM", "Secrets Manager", "Parameter Store", "ACM", "Macie"],
                    "topics": ["KMS CMK", "봉투 암호화", "CloudHSM", "Secrets Manager 자동 교체", "Parameter Store", "ACM", "Macie"]
                },
                3: {
                    "title": "보안 & 거버넌스",
                    "services": ["GuardDuty", "Inspector", "Security Hub", "Detective", "Config", "CloudTrail"],
                    "topics": ["GuardDuty", "Inspector", "Security Hub", "Detective", "Config Rules", "CloudTrail", "Trusted Advisor"]
                },
                4: {
                    "title": "모니터링 & 로깅",
                    "services": ["CloudWatch", "X-Ray", "CloudTrail", "Athena", "OpenSearch"],
                    "topics": ["CloudWatch 지표/로그/경보/대시보드", "CloudWatch Logs Insights", "X-Ray", "Athena로 로그 분석", "OpenSearch"]
                },
                5: {
                    "title": "IaC & Well-Architected",
                    "services": ["CloudFormation", "CDK", "Systems Manager", "Well-Architected Framework"],
                    "topics": ["CloudFormation 스택/중첩 스택", "CDK", "Systems Manager", "Well-Architected 6대 원칙", "비용 최적화", "DR 전략"]
                }
            }
        }
    })

    # SAA-C03 핵심 서비스 전체 목록 (50+ 서비스)
    saa_services: list = Field(default_factory=lambda: [
        # Compute
        "EC2", "Lambda", "Elastic Beanstalk", "ECS", "EKS", "Fargate", "Batch", "Lightsail", "App Runner",
        # Storage
        "S3", "EBS", "EFS", "FSx", "Storage Gateway", "S3 Glacier", "Snow Family",
        # Database
        "RDS", "Aurora", "DynamoDB", "ElastiCache", "Redshift", "Neptune", "DocumentDB", "Keyspaces", "QLDB", "Timestream",
        # Networking
        "VPC", "Route 53", "CloudFront", "Global Accelerator", "Direct Connect", "VPN", "Transit Gateway", "PrivateLink",
        # Security
        "IAM", "KMS", "Secrets Manager", "ACM", "WAF", "Shield", "GuardDuty", "Inspector", "Macie", "Security Hub", "Detective",
        # Management
        "CloudWatch", "CloudTrail", "Config", "Systems Manager", "Trusted Advisor", "Organizations", "Control Tower",
        # Integration
        "SQS", "SNS", "EventBridge", "Step Functions", "API Gateway", "AppSync", "MQ",
        # Analytics
        "Kinesis", "Athena", "EMR", "Glue", "Lake Formation", "QuickSight", "OpenSearch",
        # Developer Tools
        "CodeCommit", "CodeBuild", "CodeDeploy", "CodePipeline", "Cloud9", "X-Ray",
        # IaC
        "CloudFormation", "CDK", "SAM"
    ])


class GradioConfig(BaseModel):
    """Gradio UI configuration"""
    server_name: str = Field(default_factory=lambda: os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"))
    server_port: int = Field(default_factory=lambda: int(os.getenv("GRADIO_SERVER_PORT", "7860")))
    share: bool = False


class Settings(BaseModel):
    """Main settings class"""
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    chroma: ChromaConfig = Field(default_factory=ChromaConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    curriculum: CurriculumConfig = Field(default_factory=CurriculumConfig)
    gradio: GradioConfig = Field(default_factory=GradioConfig)

    def initialize(self):
        """Initialize settings and ensure directories exist"""
        self.paths.ensure_dirs()
        return self


# Global settings instance
settings = Settings()
