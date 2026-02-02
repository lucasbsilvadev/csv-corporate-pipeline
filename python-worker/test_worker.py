import unittest
import pandas as pd
import os
from worker import CsvProcessor

class TestCsvProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = CsvProcessor("test_id")
        
    def test_csv_validation(self):
        """Testa validação do CSV"""
        self.assertTrue(self.processor.validate_csv())
    
    def test_output_creation(self):
        """Testa se arquivo de saída é criado"""
        if os.path.exists(self.processor.output_path):
            os.remove(self.processor.output_path)
            
        result = self.processor.process()
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(self.processor.output_path))
        
        df = pd.read_csv(self.processor.output_path)
        self.assertIn('total', df.columns)
        self.assertIn('processed_at', df.columns)

if __name__ == '__main__':
    unittest.main()