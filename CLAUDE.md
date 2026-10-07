# 사전 1차시 개인 실습

FastAPI 기반 IT 자산 지급 가능 여부 조회 API다. 실제 지급나 재고 차감은 하지 않는다.
학생이 요청한 단계만 진행하고, 조사 요청에서는 구현 파일을 수정하지 않는다.
설명에 실제 확인한 파일·함수 근거를 제시하고 추측과 관찰 결과를 구분한다.
관련 없는 리팩터링, 의존성 변경, 데이터 변경, 테스트 삭제·약화는 하지 않는다.
커밋은 학생이 직접 수행한다. 실행하지 않은 검증은 미실행으로 보고한다.

- 기본 테스트: python -m pytest -q
- 완료 조건 검사: python -m pytest checks/check_availability_contract.py -q
- 두 검사 모두: python -m pytest tests checks/check_availability_contract.py -q
- 서버: python -m uvicorn app.main:app --reload

기본 테스트는 모든 요구사항을 포함하지 않는다. checks 검사는 별도 명시 실행한다.
이 파일은 작업 지침이며 기술적인 권한 차단 장치가 아니다.
