# dh-indus: 인더스 문자 해독 연구 저장소

인더스 문자 자료를 재현 가능한 방법으로 분석하고, 단계별 성공 기준에 따라 해독을 시도하는 연구 기록이다. 연구 계획과 성공 기준은 [ROADMAP.md](ROADMAP.md), 작업 방법은 [docs/METHOD.md](docs/METHOD.md), 날짜별 진행 기록은 [docs/JOURNAL.md](docs/JOURNAL.md)에 있다.

## 현재 상태

인더스 문자는 해독되지 않았다. 이 저장소의 결과는 [ROADMAP.md](ROADMAP.md) 2절의 단계(L1–L4)에 따라 표시하며, 각 결과가 어느 단계의 기준을 충족했는지를 `docs/JOURNAL.md`에 기록한다.

## 구성

```
ROADMAP.md              연구 단계, 성공 기준
docs/METHOD.md          작업 단위와 순환 절차, 규칙
docs/JOURNAL.md         날짜별 연구 기록
docs/BIBLIOGRAPHY.md    검증된 참고문헌
data/sources.tsv        원자료 목록 (고정 커밋, SHA-256)
scripts/fetch_data.py   원자료 내려받기 및 검증
src/indus/corpus.py     두 코퍼스를 읽는 순서의 줄 단위로 정규화
scripts/phase*_*.py     단계별 분석
results/                분석 결과 (스크립트가 생성)
reports/                단계별 보고서와 검토 보고서
```

## 재현 방법

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
PYTHONPATH=src python scripts/phase2_baseline.py
```

## 자료 출처

원자료는 이 저장소에 포함하지 않는다. `scripts/fetch_data.py`가 `data/sources.tsv`에 적힌 고정 버전을 내려받고 체크섬을 확인한다.

- ICIT 계열 2차 전사본: <https://github.com/horus84/Computational_Linguistics> (커밋 `ac44f08`)
- Koskenniemi & Parpola (1979), *Corpus of Texts in the Indus Script* 기계 판독본: <https://github.com/koskenni/indus> (커밋 `60f6e28`)

두 자료는 서로 다른 기호 번호 체계를 쓴다. 두 자료 모두 원 사진이나 1차 콘코던스를 대신하지 않는다.
