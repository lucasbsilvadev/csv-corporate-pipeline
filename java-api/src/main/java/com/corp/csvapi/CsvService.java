package com.corp.csvapi;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.UUID;

@Service
public class CsvService {
    
    private static final Logger logger = LoggerFactory.getLogger(CsvService.class);

    public String triggerProcessing() {
        String processId = UUID.randomUUID().toString();
        
        logger.info("Starting CSV processing with ID: {}", processId);
        
        try {

            String pythonScriptPath = "../python-worker/worker.py";
            
            ProcessBuilder pb = new ProcessBuilder("python3", pythonScriptPath, processId);
            pb.redirectErrorStream(true);
            
            new Thread(() -> {
                try {
                    Process process = pb.start();
                    
                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(process.getInputStream())
                    );
                    String line;
                    while ((line = reader.readLine()) != null) {
                        logger.info("[Python Worker] {}", line);
                    }
                    
                    int exitCode = process.waitFor();
                    logger.info("Python worker finished with exit code: {}", exitCode);
                    
                } catch (Exception e) {
                    logger.error("Error in Python worker: {}", e.getMessage());
                }
            }).start();
            
        } catch (Exception e) {
            logger.error("Failed to start processing: {}", e.getMessage());
            throw new RuntimeException("Processing failed", e);
        }
        
        return processId;
    }
}