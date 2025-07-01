
import os
import subprocess
import datetime

def run_command(cmd):
    """명령어 실행하고 결과 반환"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def auto_commit():
    """변경사항을 자동으로 commit하고 push"""
    print("🔍 변경사항 확인 중...")
    
    # Git 상태 확인
    success, output, error = run_command("git status --porcelain")
    if not success:
        print(f"❌ Git 상태 확인 실패: {error}")
        return False
    
    if not output.strip():
        print("✅ 변경사항이 없습니다.")
        return True
    
    print(f"📝 변경사항 발견: {len(output.strip().split())} 개의 파일")
    
    # 모든 변경사항 add
    success, _, error = run_command("git add .")
    if not success:
        print(f"❌ Git add 실패: {error}")
        return False
    
    # 현재 시간으로 commit 메시지 생성
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-commit: Replit에서 파일 변경사항 자동 저장 ({timestamp})"
    
    # Commit 실행
    success, _, error = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        print(f"❌ Git commit 실패: {error}")
        return False
    
    print(f"✅ Commit 완료: {commit_msg}")
    
    # Push 실행
    success, _, error = run_command("git push")
    if not success:
        print(f"❌ Git push 실패: {error}")
        print("💡 GitHub 연동을 확인해주세요!")
        return False
    
    print("🚀 GitHub에 push 완료!")
    return True

if __name__ == "__main__":
    print("🎯 Replit 자동 Commit 시작")
    auto_commit()
