package com.corp.csvapi;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/csv")
public class CsvController {

    private final CsvService csvService;

    public CsvController(CsvService csvService) {
        this.csvService = csvService;
    }

    @PostMapping("/process")
    public ResponseEntity<ApiResponse> processCsv() {
        String processId = csvService.triggerProcessing();
        return ResponseEntity.ok(
            new ApiResponse("success", "Processing started", processId)
        );
    }

    @GetMapping("/status/{id}")
    public ResponseEntity<ApiResponse> getStatus(@PathVariable String id) {

        return ResponseEntity.ok(
            new ApiResponse("success", "Check logs for details", id)
        );
    }


    public static class ApiResponse {
        private final String status;
        private final String message;
        private final String processId;

        public ApiResponse(String status, String message, String processId) {
            this.status = status;
            this.message = message;
            this.processId = processId;
        }

        public String getStatus() { return status; }
        public String getMessage() { return message; }
        public String getProcessId() { return processId; }
    }
}