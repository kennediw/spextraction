#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 18:42:36 2024

Goal is for each date in the input file,the script will locate 
the corresponding .gz file, extract its contents, run spextraction for those files, 
and save the output spectra.

@author: kennediwhite
"""
# Make sure script is in same directory as spextraction

import os
import subprocess

def run_spextraction(input_file):
    with open(input_file, 'r') as f:
        chunks = []
        chunk = []

        for line in f:
            line = line.strip()

            # Skips commented lines or empty lines
            if not line or line.startswith('#'):
                continue

            # Adds non-empty lines to the current chunk
            if line:
                chunk.append(line)
            
            # If it encounters a line break, this saves the chunk and starts a new one
            if not line and chunk:
                chunks.append(chunk)
                chunk = []

        # Adds the last chunk if any exists
        if chunk:
            chunks.append(chunk)

        # Process each chunk
        for i, chunk in enumerate(chunks):
            # Prepare output directory and file
            output_dir = 'output_spectra'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Create a single output file for the current chunk
            output_file = os.path.join(output_dir, f'chunk_{i+1}_spex')

            # Create a temporary file to store the chunk paths
            temp_file = 'temp_chunk_file.txt'
            with open(temp_file, 'w') as temp_f:
                for gz_file in chunk:
                    temp_f.write(f"{gz_file}\n")

            # Run spextraction.py on the temporary file
            command = ['python', 'spextraction_3.3.py', temp_file, '-o', output_file]

            try:
                # Run the command
                subprocess.run(command, check=True)
                print(f"Successfully processed chunk {i+1} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing chunk {i+1}: {e}")

            # Clean up temporary file
            os.remove(temp_file)

if __name__ == "__main__":
    input_file = '/Users/kennediwhite/lunarenv/workspace/jpl/dates.txt'  # Replace with the path to your input file
    run_spextraction(input_file)


