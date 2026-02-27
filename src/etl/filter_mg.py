import pandas as pd
import yaml
import os
from pathlib import Path

def load_config():
    with open("configs/config.yaml", "r") as f:
        return yaml.safe_load(f)

def clean_numeric_column(series):
    """Fixes the comma decimal separator (e.g., '34,9' -> 34.9)"""
    return pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')

def process_files(filename_template, output_name, config):
    raw_dir = Path(config['paths']['data_raw_dir'])
    processed_dir = Path(config['paths']['data_processed_dir'])
    
    all_chunks = []
    
    # Loop through years 2017 to 2025
    for year in range(2017, 2026):
        file_path = raw_dir / filename_template.format(year=year)
        
        if not file_path.exists():
            print(f"⚠️ Warning: {file_path.name} not found. Skipping...")
            continue
            
        print(f"🚀 Processing {file_path.name}...")
        
        # Read in chunks to save memory
        chunks = pd.read_csv(
            file_path, 
            sep=config['data_sources']['csv_separator'],
            encoding=config['data_sources']['file_encoding'],
            chunksize=config['etl']['chunksize'],
            low_memory=False
        )
        
        for chunk in chunks:
            # 1. Filter for MG
            mask = chunk[config['filters']['target_state']['state_column']] == config['filters']['target_state']['state_value']
            filtered_chunk = chunk[mask].copy()
            
            if not filtered_chunk.empty:
                # 2. Fix numeric columns (comma to dot)
                for col in config['etl']['numeric_cols_to_fix']:
                    if col in filtered_chunk.columns:
                        filtered_chunk[col] = clean_numeric_column(filtered_chunk[col])
                
                # 3. Add year column for easier analysis later
                filtered_chunk['year_reference'] = year
                all_chunks.append(filtered_chunk)

    if all_chunks:
        print(f"📦 Integrating and saving {output_name}...")
        master_df = pd.concat(all_chunks, ignore_index=True)
        
        # Save as Parquet (Professional format)
        output_path = processed_dir / f"{output_name}.parquet"
        master_df.to_parquet(output_path, index=False)
        print(f"✅ Success! Saved to {output_path}")
    else:
        print(f"❌ No data found for {file_pattern}")


if __name__ == "__main__":
    cfg = load_config()
    # Occurrence dataset
    process_files("datatran{year}.csv", "occ_mg_master", cfg)

    # Person dataset (all causes/types)
    process_files("acidentes{year}_todas_causas_tipos.csv", "pers_mg_master", cfg)