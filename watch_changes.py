
import time
import os
import subprocess
from datetime import datetime

def run_command(cmd):
    """명령어 실행"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_and_commit():
    """변경사항 체크하고 자동 commit"""
    success, output, error = run_command("git status --porcelain")
    
    if not success:
        print(f"❌ Git 상태 확인 실패: {error}")
        return False
    
    if not output.strip():
        return True  # 변경사항 없음
    
    print(f"📝 {datetime.now().strftime('%H:%M:%S')} - 변경사항 발견, 자동 commit 시작...")
    
    # Add all changes
    run_command("git add .")
    
    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-commit: Replit 파일 변경 자동 저장 ({timestamp})"
    
    success, _, error = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        print(f"❌ Commit 실패: {error}")
        return False
    
    # Push to GitHub
    success, _, error = run_command("git push")
    if not success:
        print(f"❌ Push 실패: {error}")
        return False
    
    print(f"✅ {datetime.now().strftime('%H:%M:%S')} - 자동 commit & push 완료!")
    return True

def watch_files():
    """파일 변경사항을 지속적으로 감지"""
    print("👀 Replit 파일 변경 감지 시작 (5초마다 체크)")
    print("💡 중지하려면 Ctrl+C를 누르세요")
    
    try:
        while True:
            check_and_commit()
            time.sleep(5)  # 5초마다 체크
            
    except KeyboardInterrupt:
        print("\n🛑 자동 commit 감지 중지됨")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    watch_files()
