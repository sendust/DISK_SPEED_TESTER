# DISK_SPEED_TESTER

HDD, SSD, NAS·SAN 공유 스토리지의 **쓰기 / 읽기 속도**를 장시간 측정하고, 결과 로그를 그래프로 그려 주는 Python 스크립트 모음입니다.
1GB 파일을 반복해서 쓰고 읽으며 파일마다 속도를 기록하므로, 순간 성능뿐 아니라 **시간 경과·용량 변화에 따른 속도 저하**를 확인할 수 있습니다.

> Code managed by sendust (sendust@sbs.co.kr)

![SAN 읽기 속도 측정 결과](<HDD_speed_read_tester_2023-02-08_[10256].png>)

---

## 구성

| 파일 | 설명 |
|---|---|
| `sendust_hdd_tester.py` | 쓰기 속도 테스트 (최초 버전) — Ctrl+C로 멈출 때까지 계속 기록 |
| `san_write.py` | 쓰기 속도 테스트 — 총 기록 용량 제한(`--size`) 지원 |
| `san_read.py` | 읽기 속도 테스트 — `san_write.py`가 만든 `.bin` 파일을 반복해서 읽음 |
| `log_to_plot.py` | 로그 → 그래프 (X축: 남은 용량) |
| `log_to_plot_by_time.py` | 로그 → 그래프 (X축: 시간, 최저 속도와 발생 시각 표시) |
| `HDD_speed_read_tester_*.log`, `*.png` | 측정 로그와 그래프 예시 |

## 요구 사항

- Python 3
- `matplotlib` (그래프 스크립트용)
  ```bat
  pip install matplotlib
  ```
- Windows 기준으로 작성되었습니다. 로컬 드라이브(`d:\temp`)와 UNC 경로(`\\server\share`) 모두 사용할 수 있습니다.

## 사용 방법

### 1. 쓰기 테스트

```bat
python san_write.py --dest e:\temp --size 100
```

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--dest` | 현재 폴더 | 테스트할 폴더 경로 |
| `--size` | `10` | 총 기록 용량 (GB). 이 용량을 넘으면 테스트 종료 |

- 대상 폴더에 `WriteTestFile_<타임스탬프>.bin` (각 1GB) 파일을 1MB 블록 단위로 계속 만듭니다.
- 화면에는 1MB 블록마다 **순간 속도**가, 파일 하나가 끝날 때마다 **평균 속도와 남은 용량**이 표시됩니다.
- 측정 시간에는 파일 열기·닫기 시간도 포함됩니다.
- `Ctrl+C`로 언제든 중단할 수 있습니다.

`sendust_hdd_tester.py`는 용량 제한 없이 디스크가 찰 때까지 계속 기록하는 초기 버전입니다.

```bat
python sendust_hdd_tester.py e:\temp
python sendust_hdd_tester.py \\server\media
```

### 2. 읽기 테스트

```bat
python san_read.py --dest e:\temp
```

- 대상 폴더의 `*.bin` 파일을 차례로 통째로 읽어 파일마다 읽기 속도를 기록합니다.
- 파일 목록을 반복하며 총 20,000회 읽은 뒤 종료합니다. (`Ctrl+C`로 중단 가능)
- **먼저 `san_write.py`로 테스트 파일을 만들어 두어야 합니다.**
- OS 캐시 영향을 줄이려면 PC 메모리보다 충분히 큰 용량을 써 두는 것이 좋습니다.

### 3. 그래프 그리기

```bat
python log_to_plot_by_time.py "log\HDD_speed_read_tester_2023-02-08_[10256].log"
python log_to_plot.py "log\HDD_speed_write_tester_2023-02-08_[1234].log"
```

로그 파일과 같은 이름의 `.png`를 저장하고 그래프 창을 띄웁니다.

| 스크립트 | X축 | Y축 | 비고 |
|---|---|---|---|
| `log_to_plot_by_time.py` | 시간 | 속도 (MB/s) | 최저 속도와 발생 시각 표시, 한글 경로 제목 지원 |
| `log_to_plot.py` | 남은 용량 (MB) | 속도 (MB/s) | Y축 0~2000 MB/s 고정 |

> `log_to_plot_by_time.py`는 그래프 제목의 한글 표시를 위해 스크립트 폴더의 `font\naverdic.ttf`를 사용합니다. 이 폰트는 저장소에 포함되어 있지 않으므로 직접 넣어 주세요.

## 로그

실행한 폴더의 `log\` 폴더에 프로세스별로 저장됩니다.

| 테스트 | 로그 파일 |
|---|---|
| `san_write.py` | `HDD_speed_write_tester_<날짜>_[pid].log` |
| `san_read.py` | `HDD_speed_read_tester_<날짜>_[pid].log` |
| `sendust_hdd_tester.py` | `HDD_speed_tester_<날짜>_[pid].log` |

```
2023-02-08 10:01:37.721750
Start New Test........
Target folder is Z:\speed
Free size is 62328789.25390625 Mbytes

2023-02-08 14:40:29.613111  Disk read speed: 1170.56 MB/s  free space is 62328400.82 MB
```

## 측정 예시

| 대상 | 기간 | 결과 |
|---|---|---|
| `Z:\speed` (읽기) | 2023-02-08 10:01 ~ 14:40 | 대부분 1,000~1,500 MB/s, 최저 780 MB/s |
| `U:\종편\speed\data` (읽기) | 2023-02-08 08:02 ~ 13:38 | 대부분 약 1,000 MB/s, 최저 292 MB/s |

![종편 스토리지 읽기 속도](<HDD_speed_read_tester_2023-02-08_[12156].png>)

## 주의 사항

- 쓰기 테스트는 대상 폴더에 1GB 파일을 계속 만듭니다. **운영 중인 스토리지에서는 남은 용량을 확인하고 `--size`로 용량을 제한하세요.**
- 테스트가 끝나도 `WriteTestFile_*.bin`, `writetest.txt` 파일은 지워지지 않으므로 직접 삭제해야 합니다.
- 속도 단위 MB/s는 1MB = 1,048,576 bytes 기준이고, `--size`의 GB는 1GB = 1,000,000,000 bytes 기준입니다.
