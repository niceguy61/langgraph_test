"""AWS MCP Server for AWS API operations"""
import os
from typing import Any, Dict, List, Optional
import json


class AWSMCPServer:
    """MCP Server for AWS API operations (read-only for safety)"""

    def __init__(self):
        self.region = os.getenv("AWS_REGION", "ap-northeast-2")
        self._boto3_available = self._check_boto3()

    def _check_boto3(self) -> bool:
        """Check if boto3 is available"""
        try:
            import boto3
            return True
        except ImportError:
            return False

    def _get_client(self, service: str):
        """Get boto3 client for a service"""
        if not self._boto3_available:
            return None

        import boto3
        return boto3.client(service, region_name=self.region)

    # MCP Tool: list_ec2_instances
    async def list_ec2_instances(
        self,
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List EC2 instances (read-only)

        Args:
            state: Filter by instance state (running, stopped, etc.)

        Returns:
            List of EC2 instances
        """
        if not self._boto3_available:
            return self._mock_ec2_instances()

        try:
            ec2 = self._get_client('ec2')

            filters = []
            if state:
                filters.append({
                    'Name': 'instance-state-name',
                    'Values': [state]
                })

            response = ec2.describe_instances(Filters=filters) if filters else ec2.describe_instances()

            instances = []
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    instances.append({
                        'instance_id': instance.get('InstanceId'),
                        'instance_type': instance.get('InstanceType'),
                        'state': instance.get('State', {}).get('Name'),
                        'public_ip': instance.get('PublicIpAddress'),
                        'private_ip': instance.get('PrivateIpAddress'),
                        'name': next(
                            (tag['Value'] for tag in instance.get('Tags', [])
                             if tag['Key'] == 'Name'),
                            'N/A'
                        )
                    })

            return {'instances': instances, 'count': len(instances)}

        except Exception as e:
            return {'error': str(e), 'instances': []}

    def _mock_ec2_instances(self) -> Dict[str, Any]:
        """Return mock EC2 instance data for demo purposes"""
        return {
            'instances': [
                {
                    'instance_id': 'i-mock123456',
                    'instance_type': 't3.micro',
                    'state': 'running',
                    'public_ip': '54.123.45.67',
                    'private_ip': '10.0.1.100',
                    'name': 'demo-instance'
                }
            ],
            'count': 1,
            'note': 'Mock data - boto3 not configured'
        }

    # MCP Tool: list_s3_buckets
    async def list_s3_buckets(self) -> Dict[str, Any]:
        """
        List S3 buckets (read-only)

        Returns:
            List of S3 buckets
        """
        if not self._boto3_available:
            return self._mock_s3_buckets()

        try:
            s3 = self._get_client('s3')
            response = s3.list_buckets()

            buckets = [
                {
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate'].isoformat()
                }
                for bucket in response.get('Buckets', [])
            ]

            return {'buckets': buckets, 'count': len(buckets)}

        except Exception as e:
            return {'error': str(e), 'buckets': []}

    def _mock_s3_buckets(self) -> Dict[str, Any]:
        """Return mock S3 bucket data"""
        return {
            'buckets': [
                {'name': 'demo-bucket-123', 'creation_date': '2024-01-15T10:00:00'},
                {'name': 'logs-bucket-456', 'creation_date': '2024-02-20T14:30:00'}
            ],
            'count': 2,
            'note': 'Mock data - boto3 not configured'
        }

    # MCP Tool: list_lambda_functions
    async def list_lambda_functions(self) -> Dict[str, Any]:
        """
        List Lambda functions (read-only)

        Returns:
            List of Lambda functions
        """
        if not self._boto3_available:
            return self._mock_lambda_functions()

        try:
            lambda_client = self._get_client('lambda')
            response = lambda_client.list_functions()

            functions = [
                {
                    'name': func['FunctionName'],
                    'runtime': func.get('Runtime', 'N/A'),
                    'memory': func.get('MemorySize'),
                    'timeout': func.get('Timeout'),
                    'last_modified': func.get('LastModified')
                }
                for func in response.get('Functions', [])
            ]

            return {'functions': functions, 'count': len(functions)}

        except Exception as e:
            return {'error': str(e), 'functions': []}

    def _mock_lambda_functions(self) -> Dict[str, Any]:
        """Return mock Lambda function data"""
        return {
            'functions': [
                {
                    'name': 'demo-function',
                    'runtime': 'python3.11',
                    'memory': 128,
                    'timeout': 30,
                    'last_modified': '2024-03-01T09:00:00'
                }
            ],
            'count': 1,
            'note': 'Mock data - boto3 not configured'
        }

    # MCP Tool: describe_vpc
    async def describe_vpc(self, vpc_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Describe VPC configuration (read-only)

        Args:
            vpc_id: Specific VPC ID (optional)

        Returns:
            VPC information
        """
        if not self._boto3_available:
            return self._mock_vpc()

        try:
            ec2 = self._get_client('ec2')

            if vpc_id:
                response = ec2.describe_vpcs(VpcIds=[vpc_id])
            else:
                response = ec2.describe_vpcs()

            vpcs = [
                {
                    'vpc_id': vpc['VpcId'],
                    'cidr_block': vpc['CidrBlock'],
                    'state': vpc['State'],
                    'is_default': vpc.get('IsDefault', False),
                    'name': next(
                        (tag['Value'] for tag in vpc.get('Tags', [])
                         if tag['Key'] == 'Name'),
                        'N/A'
                    )
                }
                for vpc in response.get('Vpcs', [])
            ]

            return {'vpcs': vpcs, 'count': len(vpcs)}

        except Exception as e:
            return {'error': str(e), 'vpcs': []}

    def _mock_vpc(self) -> Dict[str, Any]:
        """Return mock VPC data"""
        return {
            'vpcs': [
                {
                    'vpc_id': 'vpc-mock123',
                    'cidr_block': '10.0.0.0/16',
                    'state': 'available',
                    'is_default': True,
                    'name': 'default-vpc'
                }
            ],
            'count': 1,
            'note': 'Mock data - boto3 not configured'
        }

    # MCP Tool: get_iam_users
    async def get_iam_users(self) -> Dict[str, Any]:
        """
        List IAM users (read-only)

        Returns:
            List of IAM users
        """
        if not self._boto3_available:
            return self._mock_iam_users()

        try:
            iam = self._get_client('iam')
            response = iam.list_users()

            users = [
                {
                    'user_name': user['UserName'],
                    'user_id': user['UserId'],
                    'created': user['CreateDate'].isoformat(),
                    'arn': user['Arn']
                }
                for user in response.get('Users', [])
            ]

            return {'users': users, 'count': len(users)}

        except Exception as e:
            return {'error': str(e), 'users': []}

    def _mock_iam_users(self) -> Dict[str, Any]:
        """Return mock IAM user data"""
        return {
            'users': [
                {
                    'user_name': 'admin-user',
                    'user_id': 'AIDAMOCK123',
                    'created': '2024-01-01T00:00:00',
                    'arn': 'arn:aws:iam::123456789012:user/admin-user'
                }
            ],
            'count': 1,
            'note': 'Mock data - boto3 not configured'
        }

    # MCP Tool: get_service_info
    async def get_service_info(self, service: str) -> Dict[str, Any]:
        """
        Get information about an AWS service for educational purposes

        Args:
            service: AWS service name

        Returns:
            Service information
        """
        service_info = {
            'EC2': {
                'full_name': 'Elastic Compute Cloud',
                'category': 'Compute',
                'description': '가상 서버를 제공하는 AWS의 핵심 컴퓨팅 서비스',
                'key_features': ['인스턴스 타입', 'AMI', 'EBS', 'Security Groups', 'Elastic IP'],
                'pricing_model': '온디맨드, 예약 인스턴스, 스팟 인스턴스',
                'use_cases': ['웹 서버', '애플리케이션 서버', '개발/테스트 환경']
            },
            'S3': {
                'full_name': 'Simple Storage Service',
                'category': 'Storage',
                'description': '객체 스토리지 서비스',
                'key_features': ['버킷', '객체', '버전관리', '수명주기', '복제'],
                'pricing_model': '스토리지 용량, 요청 수, 데이터 전송',
                'use_cases': ['정적 웹 호스팅', '백업', '데이터 레이크']
            },
            'Lambda': {
                'full_name': 'AWS Lambda',
                'category': 'Compute (Serverless)',
                'description': '서버리스 컴퓨팅 서비스',
                'key_features': ['자동 스케일링', '이벤트 기반', '다양한 런타임'],
                'pricing_model': '호출 수, 실행 시간, 메모리',
                'use_cases': ['API 백엔드', '데이터 처리', '자동화']
            },
            'VPC': {
                'full_name': 'Virtual Private Cloud',
                'category': 'Networking',
                'description': '격리된 가상 네트워크 환경',
                'key_features': ['서브넷', '라우팅 테이블', 'NAT Gateway', 'VPN'],
                'pricing_model': 'NAT Gateway, VPN 연결 시간/데이터',
                'use_cases': ['네트워크 격리', '하이브리드 클라우드']
            },
            'IAM': {
                'full_name': 'Identity and Access Management',
                'category': 'Security',
                'description': 'AWS 리소스 접근 제어 서비스',
                'key_features': ['사용자', '그룹', '역할', '정책', 'MFA'],
                'pricing_model': '무료',
                'use_cases': ['접근 제어', '권한 관리', '보안 감사']
            },
            'RDS': {
                'full_name': 'Relational Database Service',
                'category': 'Database',
                'description': '관리형 관계형 데이터베이스 서비스',
                'key_features': ['자동 백업', '멀티 AZ', '읽기 복제본'],
                'pricing_model': '인스턴스 유형, 스토리지, I/O',
                'use_cases': ['웹 애플리케이션 DB', '엔터프라이즈 DB']
            },
            'DynamoDB': {
                'full_name': 'Amazon DynamoDB',
                'category': 'Database (NoSQL)',
                'description': '완전관리형 NoSQL 데이터베이스',
                'key_features': ['키-값 저장', '자동 스케일링', 'DAX'],
                'pricing_model': '읽기/쓰기 용량 유닛, 스토리지',
                'use_cases': ['실시간 애플리케이션', '게임 백엔드', 'IoT']
            },
            'CloudWatch': {
                'full_name': 'Amazon CloudWatch',
                'category': 'Management & Monitoring',
                'description': 'AWS 리소스 모니터링 서비스',
                'key_features': ['메트릭', '로그', '알람', '대시보드'],
                'pricing_model': '메트릭 수, 로그 저장, 대시보드',
                'use_cases': ['성능 모니터링', '로그 분석', '알림']
            }
        }

        service_upper = service.upper()

        if service_upper in service_info:
            return {
                'service': service_upper,
                'info': service_info[service_upper]
            }

        return {
            'service': service,
            'error': 'Service information not found',
            'available_services': list(service_info.keys())
        }

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get MCP tool definitions for this server"""
        return [
            {
                "name": "list_ec2_instances",
                "description": "List EC2 instances (read-only)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "state": {
                            "type": "string",
                            "enum": ["running", "stopped", "pending", "terminated"],
                            "description": "Filter by instance state"
                        }
                    }
                }
            },
            {
                "name": "list_s3_buckets",
                "description": "List S3 buckets (read-only)",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "list_lambda_functions",
                "description": "List Lambda functions (read-only)",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "describe_vpc",
                "description": "Describe VPC configuration (read-only)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "vpc_id": {"type": "string", "description": "Specific VPC ID"}
                    }
                }
            },
            {
                "name": "get_iam_users",
                "description": "List IAM users (read-only)",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_service_info",
                "description": "Get educational information about an AWS service",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "AWS service name"}
                    },
                    "required": ["service"]
                }
            }
        ]
