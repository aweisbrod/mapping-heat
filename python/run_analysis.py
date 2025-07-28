#!/usr/bin/env python3
"""
Master script to process heat index data for 2000 vs 2025 comparison
Runs all analysis scripts in sequence
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print(f"✅ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    print("🌡️ Heat Index Analysis Pipeline: 2000 vs 2025 Comparison")
    print("="*70)
    
    # Check if data file exists
    if not os.path.exists("../data/data.grib"):
        print("❌ Error: ../data/data.grib not found!")
        print("Please ensure your GRIB data file is in the data/ folder")
        sys.exit(1)
    
    scripts = [
        ("process_2000_data.py", "Processing 2000 Heat Index Data"),
        ("process_2025_data.py", "Processing 2025 Heat Index Data"),
        ("compare_2000_vs_2025.py", "Creating 2000 vs 2025 Comparison Analysis")
    ]
    
    success_count = 0
    
    for script, description in scripts:
        if run_script(script, description):
            success_count += 1
        else:
            print(f"\n❌ Pipeline failed at {script}")
            break
    
    print(f"\n{'='*70}")
    if success_count == len(scripts):
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("\n📁 Output files created:")
        output_files = [
            "heat_index_2000_avg.nc - 2000 averaged heat index",
            "heat_index_2000_full.nc - 2000 full time series",
            "heat_index_2025_avg.nc - 2025 averaged heat index", 
            "heat_index_2025_full.nc - 2025 full time series",
            "heat_index_difference_2025_2000.nc - Temperature difference map",
            "heat_index_percent_change_2025_2000.nc - Percentage change map",
            "heat_index_comparison_complete.nc - Complete comparison dataset"
        ]
        
        for file_desc in output_files:
            print(f"  ✅ {file_desc}")
            
        print(f"\n🎯 Ready for visualization!")
        print("Use the .nc files in your Svelte mapping application")
        
    else:
        print(f"❌ PIPELINE FAILED - {success_count}/{len(scripts)} scripts completed")
    
    print("="*70)

if __name__ == "__main__":
    main()
