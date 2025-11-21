# 1. 파이썬 3.11 버전을 기반으로 시작
FROM python:3.11-slim

# 2. 로그가 버퍼링 없이 즉각 찍히도록 설정 (디버깅용)
ENV PYTHONUNBUFFERED=1

# 3. 컨테이너 내 작업 폴더 설정
WORKDIR /app

# 4. PostgreSQL 연동에 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. 라이브러리 목록 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. 나머지 소스 코드 복사
COPY . /app/

# (실행 명령어는 docker-compose.yml에서 정의했으므로 여기선 생략 가능)