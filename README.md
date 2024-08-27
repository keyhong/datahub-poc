## Datahub

> 메타데이터 관리, 데이터 검색 및 데이터 거버넌스를 간소화하도록 설계된 최신 데이터 카탈로그

- [PDF 요약 소개](https://github.com/keyhong/datahub-poc/blob/main/docs-pdf/datahub_introduction_created_by_keyhong.pdf)
- [블로그 사용 후기 포스팅](https://keyhong.github.io/2024/06/27/Datahub/datahub/)

## Infra Docker Compose 

| Platform | Version | Notes |
|----------|---------|-------|
| Airflow  | 2.9.3 | Local 모드. 에어플로우-데이터허브 리니지 테스트 연계용 |
| Postgres | 15 | 기존 데이터허브 메타 DB인 MySQL에서 Postgres로 변경 (MySQL 인프라 종속성 이유) |
| Datahub | head | - |

## Next Trial : `Airflow` - `Datahub` Column Lineage 연계

[Automatic Lineage Extraction Support](https://datahubproject.io/docs/generated/lineage/lineage-feature-guide/#automatic-lineage-extraction-support) 지원이 제한적인 데이터소스가 많음

따라서, Airflow에서 실행하는 Python Task에서 Airflow의 Dag Context를 분석하여 데이터 컬럼 리니지를 만들 수 있는 방법이 필요함

Python SDK에서 [REST Emitter](https://datahubproject.io/docs/metadata-ingestion/as-a-library/#rest-emitter)를 이용하면 모든 데이터소스(ETL 소스, 타겟) 간에 커스텀하게 만들 수 있지 않을까라는 접근.

테스트를 결과, Datahub의 데이터소브 `URN`을 이용하면 자동 리니지 계보 추출이 가능하지 않더라도 수동으로 만들 수 있다. 다만, Airflow와 연계하여 실용적인 계보 추출이 가능하게 하려면 실행하는 Task에 대한 ETL 정보를 분석할 수 있게 해야 함.


** 데이터 컬럼 리니지가 필요한 이유 : CTQ 정의가 가능

### CTQ
---

> 핵심품질항목(CTQ : Critical To Quality)는 6 Sigma에서 유래한 용어로서, 데이터 품질관리 관점에서 데이터의 신뢰도가 고객, 프로세스, 시장 환경 등 `기업 경영에 중요한 영향을 미치는 품질 관리 대상 정보항목`을 의미

#### 데이터 품질 관점

> CTQ를 정의하는 것은 업무 중에 발생하는 `데이터 품질의 여러 가지 문제의 원인을 규명`하고 `품질 개선 활동의 대상과 과제를 식별`하려는 것. 이것은 데이터 품질을 향상시키는 작업의 핵심적인 출발점

#### 데이터 영향도

CTQ를 도출하는 후보 중 데이터 영향도가 있다. 

- `테이블(컬럼) 사용 프로그램 빈도`를 영향도 분석을 통하여 가중치 적용

따라서 **비즈니스에 보다 중요한 지표를 분별**하고, **특정 컬럼의 변화가 시스템 전체에 미치는 영향력을 파악**하기 위해 필요

