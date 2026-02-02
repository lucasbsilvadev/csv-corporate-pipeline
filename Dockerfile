# build stage
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY java-api/pom.xml .
COPY java-api/src ./src
RUN mvn clean package -DskipTests

# runtime stage
FROM eclipse-temurin:21-jre
WORKDIR /app

# instala Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# copia artefatos Java
COPY --from=builder /app/target/*.jar app.jar

# Copia Python worker
COPY python-worker /app/python-worker

# instala dependências Python
RUN pip3 install -r /app/python-worker/requirements.txt

# health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1

# expose port
EXPOSE 8080

# entrypoint
ENTRYPOINT ["java", "-jar", "/app.jar"]