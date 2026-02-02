package com.corp.csvapi;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/health")
public class HealthController implements HealthIndicator {

    @GetMapping
    public Map<String, Object> health() {
        return Map.of(
            "status", "UP",
            "service", "csv-processing-api",
            "timestamp", LocalDateTime.now().toString(),
            "version", "1.0.0",
            "components", Map.of(
                "java", "21",
                "spring-boot", "3.2.0",
                "python-worker", "ready"
            )
        );
    }

    @Override
    public Health health() {
        return Health.up()
            .withDetail("service", "csv-api")
            .withDetail("timestamp", System.currentTimeMillis())
            .build();
    }
}