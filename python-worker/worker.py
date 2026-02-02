#!/usr/bin/env python3
"""
CSV Processing Worker - Corporate Pipeline
Processa CSV e calcula totais
"""

import pandas as pd
import sys
import os
import time
import logging
from datetime import datetime

# Setup logging corporativo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(process)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('worker.log')
    ]
)
logger = logging.getLogger(__name__)

class CsvProcessor:
    """Processador corporativo de CSV"""
    
    def __init__(self, process_id=None):
        self.process_id = process_id or f"proc_{int(time.time())}"
        self.input_path = "data/input.csv"
        self.output_path = "data/output.csv"
        
    def validate_csv(self):
        """Valida estrutura do CSV"""
        logger.info(f"[{self.process_id}] Validating CSV structure")
        
        required_columns = ['product', 'price', 'quantity']
        
        try:
            df = pd.read_csv(self.input_path)
            
            # Verifica colunas
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns: {missing_cols}")
                
            # Verifica dados
            if df.empty:
                raise ValueError("CSV file is empty")
                
            logger.info(f"[{self.process_id}] CSV validation passed: {len(df)} rows")
            return True
            
        except Exception as e:
            logger.error(f"[{self.process_id}] CSV validation failed: {e}")
            return False
    
    def process(self):
        """Processa CSV e calcula totais"""
        logger.info(f"[{self.process_id}] Starting CSV processing")
        
        start_time = time.time()
        
        try:
            # Ler CSV
            df = pd.read_csv(self.input_path)
            logger.info(f"[{self.process_id}] Loaded {len(df)} records")
            
            # Transformação corporativa
            df['total'] = df['price'] * df['quantity']
            df['unit'] = 'BRL'
            df['processed_at'] = datetime.now().isoformat()
            
            # Métricas
            total_value = df['total'].sum()
            avg_price = df['price'].mean()
            
            # Salvar resultado
            df.to_csv(self.output_path, index=False)
            
            # Log de métricas
            processing_time = time.time() - start_time
            logger.info(f"[{self.process_id}] Processing completed")
            logger.info(f"[{self.process_id}] Total value: R$ {total_value:,.2f}")
            logger.info(f"[{self.process_id}] Average price: R$ {avg_price:,.2f}")
            logger.info(f"[{self.process_id}] Processing time: {processing_time:.2f}s")
            
            return {
                "status": "success",
                "records_processed": len(df),
                "total_value": float(total_value),
                "processing_time": processing_time,
                "output_file": self.output_path
            }
            
        except Exception as e:
            logger.error(f"[{self.process_id}] Processing failed: {e}")
            return {"status": "error", "message": str(e)}

def main():
    """Função principal"""
    process_id = sys.argv[1] if len(sys.argv) > 1 else "manual_run"
    
    logger.info(f"=== CSV Processing Worker Started ===")
    logger.info(f"Process ID: {process_id}")
    logger.info(f"Python version: {sys.version}")
    
    processor = CsvProcessor(process_id)
    
    # Pipeline corporativo
    if processor.validate_csv():
        result = processor.process()
        logger.info(f"Result: {result}")
    else:
        logger.error("Processing aborted due to validation errors")
    
    logger.info(f"=== CSV Processing Worker Finished ===")

if __name__ == "__main__":
    main()