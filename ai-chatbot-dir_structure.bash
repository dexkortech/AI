#!/bin/bash

# Define base project directory
PROJECT_DIR="ai-chatbot"

# Define subdirectories
PHASES=("phase-1-message-classification" "phase-2-summarization" "phase-3-vector-search" "phase-4-logging")

# Create main project directory
mkdir -p $PROJECT_DIR

# Loop through each phase and create directories
for PHASE in "${PHASES[@]}"; do
    mkdir -p $PROJECT_DIR/$PHASE/tests
    mkdir -p $PROJECT_DIR/$PHASE/utils

    # Create main files
    touch $PROJECT_DIR/$PHASE/config.py
    touch $PROJECT_DIR/$PHASE/requirements.txt

    # Create phase-specific files
    case $PHASE in
        "phase-1-message-classification")
            touch $PROJECT_DIR/$PHASE/{main.py,classifier.py}
            touch $PROJECT_DIR/$PHASE/tests/test_classifier.py
            touch $PROJECT_DIR/$PHASE/utils/preprocess.py
            ;;
        "phase-2-summarization")
            touch $PROJECT_DIR/$PHASE/summarizer.py
            touch $PROJECT_DIR/$PHASE/tests/test_summarizer.py
            touch $PROJECT_DIR/$PHASE/utils/text_processing.py
            ;;
        "phase-3-vector-search")
            touch $PROJECT_DIR/$PHASE/vector_store.py
            touch $PROJECT_DIR/$PHASE/tests/test_vector_store.py
            ;;
        "phase-4-logging")
            touch $PROJECT_DIR/$PHASE/logging.py
            touch $PROJECT_DIR/$PHASE/tests/test_logging.py
            ;;
    esac
done

echo "Project structure created successfully!"
