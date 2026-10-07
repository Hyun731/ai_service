# 기업 IT 자산 지급 가능 여부 API — 사전 1차시

조회 전용 실습이다. 실제 신청 저장, 지급 확정, 재고 차감, 인증, 데이터베이스는 없다.
장비 1(노트북)은 3대, 장비 2(프로젝터)는 0대가 남아 있다.
신청 수량이 남은 수량 이하이면 지급 가능이어야 한다. 초기 코드에는 경계값 오류가 있다.

## 준비

Python 3.10 이상을 사용한다. 제공 예제는 Python 3.12에서 검증한다.
각자 새 개인 작업 폴더에 압축을 풀고 그 폴더를 연다.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

PowerShell 활성화가 차단되면 정책을 바꾸지 않고 `.\.venv\Scripts\python.exe`를
이 문서의 `python` 대신 사용한다. 설치 명령에도 동일하게 적용한다.

## Git 기준점

ZIP에는 Git 이력이 없다. 새 개인 실습 폴더에서 아래를 한 번 실행한다.
교사가 초기 커밋을 제공한 저장소를 복제한 경우 생략한다.

```bash
git init
git add .gitignore README.md requirements.txt CLAUDE.md app tests checks logs
git commit -m "chore: start lesson 01"
```

이름·이메일 오류는 본인의 정보를 이 저장소 범위에서 설정해 해결한다.
기존 프로젝트 내부에서 실습하지 않는다. 기존 작업을 지우거나 일괄 커밋하지 않는다.

## 실행

```bash
python -m uvicorn app.main:app --reload
```

http://127.0.0.1:8000/docs 에서 `GET /equipment/{equipment_id}/availability`를 연다.
`Try it out` → `equipment_id`와 `quantity` 입력 → `Execute` 순서로 실행한다.
예: ID 1, 수량 3. 서버 터미널은 유지하고 새 터미널에서 검사와 Claude를 실행한다.
새 터미널에서도 같은 폴더로 이동하고 가상환경을 활성화한다.

## 검사

```bash
python -m pytest -q
python -m pytest checks/check_availability_contract.py -q
```

- 기본 테스트: 초기 코드에서 3 passed
- 완료 조건 검사: 초기 코드에서 1 failed, 3 passed
- 별도 검사 파일은 기본 pytest 수집 이름이 아니므로 경로를 명시해야 실행된다.
- 이는 학습 단계 분리용이다. 실제 팀 프로젝트에서는 중요한 회귀 검사를 일반 테스트·CI에 포함한다.

최종 확인:

```bash
python -m pytest tests checks/check_availability_contract.py -q
```

최소 수정 후 제공 검사 기준 7 passed가 되어야 한다. 검사 추가 시 개수는 달라질 수 있다.
테스트는 수정하지 않고 읽고 실행한다. 테스트 설계·TDD 심화는 다음 차시에서 진행한다.
`logs/01.md`에 직접 확인한 증거와 판단을 작성한다.

## 코드 분석 학습 방식

Claude에게 관련 파일과 호출 흐름의 분석 초안을 요청하고, 후속 질문으로 범위를 좁힌다.
학생은 핵심 호출·판단 조건을 직접 확인하고 logs/01.md에 수용·수정·보류 이유를 남긴다.
HTTP·Router·Service·Schema는 이미 학습한 개념으로 전제한다.
