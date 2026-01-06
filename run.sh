#!/bin/bash

# Start all docs servers in background
cd datatruck-docs/landing && mkdocs serve -a localhost:8000 &
cd datatruck-docs/devops && mkdocs serve -a localhost:8001 &
cd datatruck-docs/backend && mkdocs serve -a localhost:8002 &
cd datatruck-docs/frontend && mkdocs serve -a localhost:8003 &

echo "Servers running:"
echo "Landing:  http://localhost:8000"
echo "DevOps:   http://localhost:8001"
echo "Backend:  http://localhost:8002"
echo "Frontend: http://localhost:8003"
echo ""
echo "Press Ctrl+C to stop all servers"

wait