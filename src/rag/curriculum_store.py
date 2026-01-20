"""Curriculum-based ChromaDB Store - 커리큘럼 기반 벡터 스토어"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from src.config import settings


class CurriculumStore:
    """커리큘럼을 ChromaDB에 저장하고 검색하는 클래스"""

    COLLECTION_NAME = "aws_curriculum"

    def __init__(self):
        self._client: Optional[chromadb.HttpClient] = None
        self._collection = None

    def _get_client(self) -> chromadb.HttpClient:
        """ChromaDB 클라이언트 생성"""
        if self._client is None:
            host_url = settings.chroma.host
            if host_url.startswith("http://"):
                host_url = host_url[7:]
            elif host_url.startswith("https://"):
                host_url = host_url[8:]

            if ":" in host_url:
                host, port = host_url.split(":")
                port = int(port)
            else:
                host = host_url
                port = 8000

            self._client = chromadb.HttpClient(
                host=host,
                port=port,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
        return self._client

    def _get_collection(self):
        """컬렉션 가져오기 또는 생성"""
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"description": "AWS SAA-C03 커리큘럼 데이터"}
            )
        return self._collection

    def load_curriculum(self, curriculum_path: Optional[Path] = None) -> Dict[str, Any]:
        """커리큘럼 JSON 파일 로드"""
        if curriculum_path is None:
            curriculum_path = settings.paths.output_dir / "curriculum.json"

        if not curriculum_path.exists():
            raise FileNotFoundError(f"커리큘럼 파일을 찾을 수 없습니다: {curriculum_path}")

        with open(curriculum_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def index_curriculum(self, curriculum: Optional[Dict] = None) -> Dict[str, Any]:
        """커리큘럼을 ChromaDB에 인덱싱"""
        if curriculum is None:
            curriculum = self.load_curriculum()

        collection = self._get_collection()

        # 기존 데이터 삭제 (재인덱싱)
        try:
            existing = collection.get()
            if existing['ids']:
                collection.delete(ids=existing['ids'])
        except Exception:
            pass

        documents = []
        metadatas = []
        ids = []

        # 주차별/일별 데이터 추출
        for week in curriculum.get('weeks', []):
            week_num = week['week']
            week_title = week['title']

            for day in week.get('days', []):
                day_num = day['day']
                day_title = day['title']
                core_services = day.get('core_services', [])
                topics = day.get('topics', [])
                key_concepts = day.get('key_concepts', [])

                # 검색 가능한 문서 생성
                doc_content = f"""
Week {week_num} Day {day_num}: {day_title}
주제: {week_title}

핵심 서비스: {', '.join(core_services)}

다루는 토픽:
{chr(10).join('- ' + t for t in topics)}

핵심 개념:
{chr(10).join('- ' + c for c in key_concepts)}
"""

                doc_id = f"week{week_num}_day{day_num}"

                documents.append(doc_content)
                metadatas.append({
                    'week': week_num,
                    'day': day_num,
                    'week_title': week_title,
                    'day_title': day_title,
                    'core_services': ', '.join(core_services),
                    'topics': ', '.join(topics[:5]),  # 최대 5개
                    'key_concepts': ', '.join(key_concepts[:5])
                })
                ids.append(doc_id)

        # ChromaDB에 저장
        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

        return {
            'status': 'success',
            'indexed_days': len(documents),
            'collection_count': collection.count()
        }

    def get_day_info(self, week: int, day: int) -> Optional[Dict[str, Any]]:
        """특정 일차 정보 조회"""
        collection = self._get_collection()
        doc_id = f"week{week}_day{day}"

        try:
            result = collection.get(ids=[doc_id], include=['documents', 'metadatas'])
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'content': result['documents'][0] if result['documents'] else None,
                    'metadata': result['metadatas'][0] if result['metadatas'] else None
                }
        except Exception as e:
            print(f"조회 오류: {e}")

        return None

    def search_by_service(self, service_name: str, n_results: int = 5) -> List[Dict]:
        """서비스명으로 관련 일차 검색"""
        collection = self._get_collection()

        results = collection.query(
            query_texts=[service_name],
            n_results=n_results,
            include=['documents', 'metadatas']
        )

        matched = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                matched.append({
                    'id': doc_id,
                    'content': results['documents'][0][i] if results['documents'] else None,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else None
                })

        return matched

    def search_by_topic(self, topic: str, n_results: int = 5) -> List[Dict]:
        """토픽으로 관련 일차 검색"""
        return self.search_by_service(topic, n_results)

    def get_week_services(self, week: int) -> List[str]:
        """특정 주차의 모든 서비스 목록 조회"""
        collection = self._get_collection()

        try:
            results = collection.get(
                where={"week": week},
                include=['metadatas']
            )

            services = set()
            for metadata in results.get('metadatas', []):
                if metadata and 'core_services' in metadata:
                    for svc in metadata['core_services'].split(', '):
                        if svc.strip():
                            services.add(svc.strip())

            return list(services)
        except Exception as e:
            print(f"주차 서비스 조회 오류: {e}")
            return []

    def get_day_services(self, week: int, day: int) -> List[str]:
        """특정 일차의 서비스 목록 조회"""
        day_info = self.get_day_info(week, day)
        if day_info and day_info.get('metadata'):
            services_str = day_info['metadata'].get('core_services', '')
            return [s.strip() for s in services_str.split(',') if s.strip()]
        return []

    def validate_content_against_curriculum(
        self,
        week: int,
        day: int,
        content_files: Dict[str, str]
    ) -> Dict[str, Any]:
        """콘텐츠가 커리큘럼과 일치하는지 검증"""
        day_info = self.get_day_info(week, day)

        if not day_info:
            return {
                'status': 'error',
                'message': f'Week {week} Day {day} 커리큘럼 정보를 찾을 수 없습니다',
                'valid': False
            }

        metadata = day_info.get('metadata', {})
        expected_services = set(
            s.strip().upper()
            for s in metadata.get('core_services', '').split(',')
            if s.strip()
        )

        # 콘텐츠에서 서비스 추출
        found_services = set()

        # 파일명에서 서비스 추출
        for filename in content_files.keys():
            if filename not in ['overview', 'concepts', 'console_guide', 'cli_guide',
                               'best_practices', 'practice', 'quiz', 'lecture', 'README']:
                found_services.add(filename.upper())

        # 콘텐츠에서 AWS 서비스 키워드 검색
        aws_services = [
            'EC2', 'EBS', 'S3', 'CloudFront', 'VPC', 'IAM', 'RDS', 'Aurora',
            'DynamoDB', 'Lambda', 'ECS', 'EKS', 'Fargate', 'CloudWatch',
            'Route 53', 'ELB', 'Auto Scaling', 'CloudFormation', 'SNS', 'SQS',
            'API Gateway', 'Step Functions', 'EventBridge', 'Kinesis',
            'ElastiCache', 'Redshift', 'KMS', 'Secrets Manager', 'ACM',
            'GuardDuty', 'Inspector', 'Config', 'CloudTrail', 'X-Ray',
            'NAT Gateway', 'Internet Gateway', 'Transit Gateway', 'VPC Endpoints',
            'Security Groups', 'NACL', 'AMI', 'EFS', 'Glacier'
        ]

        all_content = ' '.join(content_files.values()).upper()
        for svc in aws_services:
            if svc.upper() in all_content:
                found_services.add(svc.upper())

        # 비교
        missing = expected_services - found_services
        extra = found_services - expected_services

        # 상태 판단
        if not missing:
            status = 'COMPLETE'
            message = '모든 핵심 서비스가 포함되어 있습니다.'
        elif len(missing) < len(expected_services) / 2:
            status = 'PARTIAL'
            message = f'일부 서비스 누락: {", ".join(missing)}'
        else:
            status = 'INCOMPLETE'
            message = f'많은 서비스 누락: {", ".join(missing)}'

        return {
            'status': status,
            'valid': status == 'COMPLETE',
            'week': week,
            'day': day,
            'day_title': metadata.get('day_title', ''),
            'expected_services': list(expected_services),
            'found_services': list(found_services),
            'missing_services': list(missing),
            'extra_services': list(extra),
            'message': message
        }

    def get_all_curriculum_info(self) -> List[Dict]:
        """전체 커리큘럼 정보 조회"""
        collection = self._get_collection()

        try:
            results = collection.get(include=['metadatas'])
            return results.get('metadatas', [])
        except Exception as e:
            print(f"전체 조회 오류: {e}")
            return []

    def reset(self) -> bool:
        """컬렉션 리셋"""
        try:
            client = self._get_client()
            client.delete_collection(self.COLLECTION_NAME)
            self._collection = None
            return True
        except Exception as e:
            print(f"리셋 오류: {e}")
            return False
