#!/bin/bash

# Add Maestro to PATH
export PATH="$HOME/.maestro/bin:$PATH"
echo "Updated PATH: $PATH"
maestro --version  # Verify Maestro is available

# Function to run a flow and handle failures
run_flow() {
  echo "Running flow: $1"
  flow_name=$(basename "$1" .yaml)
  log_file="./maestro-results/$flow_name.log"
  maestro test "$1" > "$log_file" 2>&1
  if [ $? -ne 0 ]; then
    echo "Flow $1 failed, but continuing with the next flow..."
  fi
}

# List of flows to run
flows=(
  "Klikit_Flows/Login.yaml"
  "Klikit_Flows/homepage.yaml"
  "Klikit_Flows/Add_Order.yaml"
  "Klikit_Flows/StopApp.yaml"
)

# Create a directory for Maestro results
mkdir -p ./maestro-results

# Run each flow sequentially
for flow in "${flows[@]}"; do
  run_flow "$flow"
done

echo "All flows executed."

# Check if Maestro results exist
if [ -d "./maestro-results" ]; then
  echo "Maestro results found."
else
  echo "❌ Maestro results not found!"
  exit 1
fi

# Convert Maestro logs to JUnit XML
echo "Converting Maestro logs to JUnit XML..."
mkdir -p ./allure-results
python3 convert_maestro_to_junit.py ./maestro-results ./allure-results

# Verify JUnit XML files were generated
if [ -d "./allure-results" ]; then
  echo "JUnit XML files generated successfully."
else
  echo "❌ JUnit XML files not found!"
  exit 1
fi