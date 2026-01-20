"""
커리큘럼 기반 콘텐츠 검증 시스템
ChromaDB + RAG를 사용하여 일별 콘텐츠가 커리큘럼에 맞게 작성되었는지 검증
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

# 설정
OUTPUT_DIR = Path("d:/langgraph/output")
CURRICULUM_PATH = OUTPUT_DIR / "curriculum.json"


def load_curriculum() -> Dict[str, Any]:
    """커리큘럼 JSON 로드"""
    with open(CURRICULUM_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_day_services(curriculum: Dict) -> List[Dict]:
    """커리큘럼에서 일별 서비스 목록 추출"""
    day_services = []

    for week in curriculum['weeks']:
        week_num = week['week']
        week_title = week['title']

        for day in week['days']:
            day_num = day['day']
            day_title = day['title']
            core_services = day['core_services']
            topics = day.get('topics', [])
            key_concepts = day.get('key_concepts', [])

            # 서비스별 문서 생성
            service_doc = {
                'week': week_num,
                'day': day_num,
                'week_title': week_title,
                'day_title': day_title,
                'core_services': core_services,
                'topics': topics,
                'key_concepts': key_concepts,
                'id': f"week{week_num}_day{day_num}",
                'content': f"""
Week {week_num} Day {day_num}: {day_title}
주제: {week_title}

핵심 서비스: {', '.join(core_services)}

다루는 토픽:
{chr(10).join('- ' + t for t in topics)}

핵심 개념:
{chr(10).join('- ' + c for c in key_concepts)}
"""
            }
            day_services.append(service_doc)

    return day_services


def load_actual_content(week: int, day: int) -> Dict[str, str]:
    """실제 작성된 콘텐츠 파일들 로드"""
    content_dir = OUTPUT_DIR / f"week{week}" / f"day{day}"
    content = {}

    if not content_dir.exists():
        return content

    for md_file in content_dir.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content[md_file.stem] = f.read()

    return content


def extract_services_from_content(content: Dict[str, str]) -> List[str]:
    """콘텐츠에서 서비스명 추출"""
    services = set()

    # 파일명에서 서비스 추출
    for filename in content.keys():
        if filename not in ['overview', 'concepts', 'console_guide', 'cli_guide',
                           'best_practices', 'practice', 'quiz', 'lecture']:
            services.add(filename.upper())

    # 콘텐츠에서 서비스명 추출 (제목 기반)
    service_keywords = [
        'EC2', 'EBS', 'S3', 'CloudFront', 'VPC', 'IAM', 'RDS', 'Aurora',
        'DynamoDB', 'Lambda', 'ECS', 'EKS', 'Fargate', 'CloudWatch',
        'Route 53', 'ELB', 'Auto Scaling', 'CloudFormation', 'SNS', 'SQS',
        'API Gateway', 'Step Functions', 'EventBridge', 'Kinesis',
        'ElastiCache', 'Redshift', 'KMS', 'Secrets Manager', 'ACM',
        'GuardDuty', 'Inspector', 'Config', 'CloudTrail', 'X-Ray',
        'NAT Gateway', 'Internet Gateway', 'Transit Gateway', 'VPC Endpoints',
        'Security Groups', 'NACL', 'AMI', 'EFS', 'Glacier'
    ]

    all_content = ' '.join(content.values())
    for keyword in service_keywords:
        if keyword.lower() in all_content.lower():
            services.add(keyword)

    return list(services)


def setup_chromadb(day_services: List[Dict]) -> chromadb.Collection:
    """ChromaDB 설정 및 커리큘럼 데이터 삽입"""
    # 임베딩 함수 (기본 sentence-transformers)
    # sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    #     model_name="all-MiniLM-L6-v2"
    # )

    # 클라이언트 생성
    client = chromadb.Client()

    # 기존 컬렉션 삭제 후 재생성
    try:
        client.delete_collection("curriculum")
    except:
        pass

    collection = client.create_collection(
        name="curriculum",
        metadata={"description": "AWS SAA-C03 커리큘럼 서비스 목록"}
    )

    # 데이터 삽입
    documents = []
    metadatas = []
    ids = []

    for day_service in day_services:
        documents.append(day_service['content'])
        metadatas.append({
            'week': day_service['week'],
            'day': day_service['day'],
            'week_title': day_service['week_title'],
            'day_title': day_service['day_title'],
            'core_services': ', '.join(day_service['core_services'])
        })
        ids.append(day_service['id'])

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return collection


def verify_content(collection: chromadb.Collection, day_services: List[Dict]) -> List[Dict]:
    """각 일별 콘텐츠 검증"""
    results = []

    for day_service in day_services:
        week = day_service['week']
        day = day_service['day']
        expected_services = set(s.upper() for s in day_service['core_services'])

        # 실제 콘텐츠 로드
        actual_content = load_actual_content(week, day)

        if not actual_content:
            results.append({
                'week': week,
                'day': day,
                'day_title': day_service['day_title'],
                'status': 'MISSING',
                'expected_services': list(expected_services),
                'found_services': [],
                'missing_services': list(expected_services),
                'extra_services': [],
                'files': [],
                'message': f"Week{week}/Day{day} 콘텐츠가 존재하지 않습니다."
            })
            continue

        # 콘텐츠에서 서비스 추출
        found_services = set(s.upper() for s in extract_services_from_content(actual_content))

        # 비교
        missing = expected_services - found_services
        extra = found_services - expected_services

        # 상태 판단
        if not missing:
            status = 'COMPLETE'
            message = "모든 핵심 서비스가 포함되어 있습니다."
        elif len(missing) < len(expected_services) / 2:
            status = 'PARTIAL'
            message = f"일부 서비스 누락: {', '.join(missing)}"
        else:
            status = 'INCOMPLETE'
            message = f"많은 서비스 누락: {', '.join(missing)}"

        results.append({
            'week': week,
            'day': day,
            'day_title': day_service['day_title'],
            'status': status,
            'expected_services': list(expected_services),
            'found_services': list(found_services),
            'missing_services': list(missing),
            'extra_services': list(extra),
            'files': list(actual_content.keys()),
            'message': message
        })

    return results


def query_similar_content(collection: chromadb.Collection, query: str, n_results: int = 3):
    """유사한 커리큘럼 내용 검색"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results


def print_verification_report(results: List[Dict]):
    """검증 결과 리포트 출력"""
    print("\n" + "=" * 80)
    print("📊 AWS SAA-C03 커리큘럼 콘텐츠 검증 리포트")
    print("=" * 80)

    # 통계
    total = len(results)
    complete = sum(1 for r in results if r['status'] == 'COMPLETE')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    incomplete = sum(1 for r in results if r['status'] == 'INCOMPLETE')
    missing = sum(1 for r in results if r['status'] == 'MISSING')

    print(f"\n📈 전체 통계:")
    print(f"   총 일수: {total}")
    print(f"   ✅ 완료: {complete}")
    print(f"   ⚠️  부분 완료: {partial}")
    print(f"   ❌ 미완료: {incomplete}")
    print(f"   🚫 누락: {missing}")
    print(f"   완료율: {(complete/total)*100:.1f}%")

    print("\n" + "-" * 80)
    print("📋 상세 결과:")
    print("-" * 80)

    for week_num in range(1, 5):
        week_results = [r for r in results if r['week'] == week_num]
        if week_results:
            print(f"\n🗓️  Week {week_num}")
            for r in week_results:
                status_icon = {
                    'COMPLETE': '✅',
                    'PARTIAL': '⚠️',
                    'INCOMPLETE': '❌',
                    'MISSING': '🚫'
                }.get(r['status'], '❓')

                print(f"\n   {status_icon} Day {r['day']}: {r['day_title']}")
                print(f"      상태: {r['status']}")
                print(f"      예상 서비스: {', '.join(r['expected_services'])}")

                if r['files']:
                    print(f"      작성된 파일: {', '.join(r['files'])}")

                if r['found_services']:
                    print(f"      발견된 서비스: {', '.join(r['found_services'])}")

                if r['missing_services']:
                    print(f"      ⚠️  누락된 서비스: {', '.join(r['missing_services'])}")

                print(f"      메시지: {r['message']}")

    print("\n" + "=" * 80)
    print("검증 완료")
    print("=" * 80)

    return {
        'total': total,
        'complete': complete,
        'partial': partial,
        'incomplete': incomplete,
        'missing': missing,
        'completion_rate': (complete/total)*100
    }


def main():
    """메인 실행"""
    print("🔍 커리큘럼 기반 콘텐츠 검증 시작...\n")

    # 1. 커리큘럼 로드
    print("1️⃣  커리큘럼 로드 중...")
    curriculum = load_curriculum()
    print(f"   ✓ 커리큘럼 로드 완료: {curriculum['title']}")

    # 2. 일별 서비스 추출
    print("\n2️⃣  일별 서비스 목록 추출 중...")
    day_services = extract_day_services(curriculum)
    print(f"   ✓ {len(day_services)}개 일차 서비스 추출 완료")

    # 3. ChromaDB 설정
    print("\n3️⃣  ChromaDB 설정 중...")
    collection = setup_chromadb(day_services)
    print(f"   ✓ ChromaDB 컬렉션 생성 완료 (문서 수: {collection.count()})")

    # 4. 콘텐츠 검증
    print("\n4️⃣  콘텐츠 검증 중...")
    results = verify_content(collection, day_services)

    # 5. 결과 리포트
    stats = print_verification_report(results)

    # 6. 결과 저장
    output_file = OUTPUT_DIR / "verification_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'statistics': stats,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n📁 검증 결과 저장: {output_file}")

    # 7. RAG 테스트 쿼리
    print("\n5️⃣  RAG 테스트 쿼리...")
    test_queries = [
        "EC2 인스턴스와 EBS 볼륨",
        "S3 버킷과 CloudFront CDN",
        "VPC 네트워킹",
        "RDS 데이터베이스"
    ]

    for query in test_queries:
        print(f"\n   쿼리: '{query}'")
        search_results = query_similar_content(collection, query, n_results=2)
        for i, (doc, meta) in enumerate(zip(search_results['documents'][0],
                                            search_results['metadatas'][0])):
            print(f"   → 매칭 {i+1}: Week{meta['week']} Day{meta['day']} - {meta['day_title']}")

    return results


if __name__ == "__main__":
    main()
