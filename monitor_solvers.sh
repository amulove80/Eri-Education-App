#!/bin/bash
# Monitor all running solvers

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         PUZZLE #135 SOLVER - LIVE MONITORING                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

while true; do
    clear
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║         PUZZLE #135 SOLVER - LIVE MONITORING                       ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Count running processes
    RUNNING=$(ps aux | grep "python.*solver" | grep -v grep | wc -l)
    echo "🔄 Running Processes: $RUNNING"
    echo ""
    
    # Show process details
    echo "📊 Active Solvers:"
    echo "----------------------------------------"
    ps aux | grep "python.*solver" | grep -v grep | awk '{print "  PID:", $2, "| CPU:", $3"% | MEM:", $4"% | CMD:", $11, $12}' | head -15
    echo ""
    
    # Check for solution
    if [ -f "/workspace/SOLUTION_*.txt" ]; then
        echo "🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉"
        cat /workspace/SOLUTION_*.txt
        exit 0
    fi
    
    # Show log tails
    echo "📝 Recent Progress:"
    echo "----------------------------------------"
    
    if [ -f "/workspace/fast_solver_1.log" ]; then
        echo "Fast Solver 1:"
        tail -3 /workspace/fast_solver_1.log 2>/dev/null | grep -E "Time:|Rate:|Total:" || echo "  Starting..."
    fi
    
    if [ -f "/workspace/fast_solver_2.log" ]; then
        echo "Fast Solver 2:"
        tail -3 /workspace/fast_solver_2.log 2>/dev/null | grep -E "Time:|Rate:|Total:" || echo "  Starting..."
    fi
    
    if [ -f "/workspace/multi_algo.log" ]; then
        echo "Multi-Algorithm:"
        tail -3 /workspace/multi_algo.log 2>/dev/null | grep -E "GLOBAL|Total|Rate:" || echo "  Starting..."
    fi
    
    echo ""
    echo "Press Ctrl+C to stop monitoring (solvers keep running)"
    
    sleep 10
done
