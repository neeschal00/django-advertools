#!/bin/bash


# Split requirements.txt into smaller chunks (e.g., 50 packages per batch)
split -l 30 requirements.txt batch_

#activate virtual env
source venv/bin/activate

# Install packages from each batch
for batch in batch_*; do
    pip install -r "$batch"
done

#deactivate venv
deactivate 

#clean up temporary batch files
rm batch_*
