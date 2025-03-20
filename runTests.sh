#!/bin/bash

# Function to run a flow and handle failures
run_flow() {
  echo "Running flow: $1"
  maestro test "$1"
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

# Run each flow sequentially
for flow in "${flows[@]}"; do
  run_flow "$flow"
done

echo "All flows executed."