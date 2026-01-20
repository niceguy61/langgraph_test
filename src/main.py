"""Main entry point for AWS Lecture Generator"""
import asyncio
import argparse
import json
from pathlib import Path

from src.config import settings
from src.ui import launch_app
from src.graph import run_workflow
from src.rag import VectorStoreManager


def init_directories():
    """Initialize required directories"""
    settings.paths.ensure_dirs()
    print(f"Output directory: {settings.paths.output_dir}")
    print(f"Data directory: {settings.paths.data_dir}")


async def generate_lectures(week: int = None, day: int = None):
    """Generate lectures using the workflow"""
    if week:
        request = f"Week {week} AWS 강의자료 생성"
        if day:
            request = f"Week {week} Day {day} AWS 강의자료 생성"
    else:
        request = "4주 전체 AWS 강의자료 생성"

    print(f"\n강의자료 생성 시작: {request}")
    print("-" * 50)

    result = run_workflow(
        request=request,
        target_week=week,
        target_day=day
    )

    print("\n생성 완료!")
    print("-" * 50)

    # Print summary
    if "curriculum" in result:
        print(f"커리큘럼: {json.dumps(result['curriculum'], ensure_ascii=False, indent=2)[:500]}...")

    if "saved_files" in result:
        print(f"\n저장된 파일:")
        for name, path in result["saved_files"].items():
            print(f"  - {name}: {path}")

    if "average_score" in result:
        print(f"\n품질 점수: {result['average_score']:.1f}/100")

    return result


async def index_documents(directory: str = None):
    """Index documents into vector store"""
    vectorstore = VectorStoreManager()

    dir_path = Path(directory) if directory else settings.paths.data_dir

    print(f"문서 인덱싱 시작: {dir_path}")

    result = vectorstore.ingest_documents(dir_path)

    print(f"인덱싱 완료!")
    print(f"  - 로드된 문서: {result.get('documents_loaded', 0)}")
    print(f"  - 생성된 청크: {result.get('chunks_created', 0)}")

    return result


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AWS 학습 강의자료 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # Gradio UI 실행
  python -m src.main

  # 특정 주차 강의자료 생성
  python -m src.main --generate --week 1

  # 전체 강의자료 생성
  python -m src.main --generate

  # 문서 인덱싱
  python -m src.main --index

  # 문서 인덱싱 (특정 디렉토리)
  python -m src.main --index --docs-dir ./my_docs
        """
    )

    parser.add_argument(
        "--ui",
        action="store_true",
        default=True,
        help="Gradio UI 실행 (기본값)"
    )

    parser.add_argument(
        "--generate",
        action="store_true",
        help="강의자료 생성"
    )

    parser.add_argument(
        "--week",
        type=int,
        choices=[1, 2, 3, 4],
        help="생성할 주차 (1-4)"
    )

    parser.add_argument(
        "--day",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="생성할 일차 (1-5)"
    )

    parser.add_argument(
        "--index",
        action="store_true",
        help="문서 인덱싱"
    )

    parser.add_argument(
        "--docs-dir",
        type=str,
        help="인덱싱할 문서 디렉토리"
    )

    parser.add_argument(
        "--host",
        type=str,
        default=settings.gradio.server_name,
        help="서버 호스트"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=settings.gradio.server_port,
        help="서버 포트"
    )

    args = parser.parse_args()

    # Initialize directories
    init_directories()

    # Handle different modes
    if args.index:
        asyncio.run(index_documents(args.docs_dir))

    elif args.generate:
        asyncio.run(generate_lectures(args.week, args.day))

    else:
        # Default: launch UI
        print("\n" + "=" * 50)
        print("AWS 학습 강의자료 생성기")
        print("=" * 50)
        print(f"\nGradio UI 시작: http://{args.host}:{args.port}")
        print("종료하려면 Ctrl+C를 누르세요\n")

        settings.gradio.server_name = args.host
        settings.gradio.server_port = args.port

        launch_app()


if __name__ == "__main__":
    main()
