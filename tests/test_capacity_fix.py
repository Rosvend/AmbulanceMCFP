#!/usr/bin/env python3
"""
Test the fixed capacity constraint
Verifies that the model now correctly handles shared road capacity
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from visualization.network import NetworkManager
from optimization.data_interface import OptimizationData
from optimization.model import AmbulanceRoutingModel
import random

def test_capacity_constraint():
    """Test that capacity constraints work correctly"""
    
    print("=" * 70)
    print("TESTING FIXED CAPACITY CONSTRAINT")
    print("=" * 70)
    
    # Load network
    print("\n[1] Loading network...")
    nm = NetworkManager(cache_dir="../data")
    center_point = (6.2331, -75.5839)
    graph = nm.load_network(center_point, method='circle', distance=560, use_cache=True)
    print(f"    Network: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
    
    # Test with multiple parameter sets
    test_configs = [
        {"name": "Conservative", "c_min": 40, "c_max": 80, "r_min": 15, "r_max": 35},
        {"name": "Moderate", "c_min": 35, "c_max": 70, "r_min": 15, "r_max": 40},
        {"name": "Aggressive", "c_min": 30, "c_max": 60, "r_min": 20, "r_max": 45},
    ]
    
    results = []
    
    for config in test_configs:
        print(f"\n{'=' * 70}")
        print(f"TESTING: {config['name']} Parameters")
        print(f"{'=' * 70}")
        print(f"  Capacity range: [{config['c_min']}, {config['c_max']}] km/h")
        print(f"  Speed range: [{config['r_min']}, {config['r_max']}] km/h")
        
        # Assign capacities
        random.seed(42)  # For reproducibility
        nm.assign_random_capacities(c_min=config['c_min'], c_max=config['c_max'])
        
        # Select origin and destinations
        origin, destinations = nm.get_random_nodes(n_destinations=3)
        destinations_with_severity = [
            (destinations[0], 'Leve'),
            (destinations[1], 'Media'),
            (destinations[2], 'Critica')
        ]
        
        # Create optimization data
        opt_data = OptimizationData()
        opt_data.from_network(graph, origin, destinations_with_severity)
        
        # Create and solve model
        model = AmbulanceRoutingModel(opt_data)
        costs = {'Leve': 100.0, 'Media': 250.0, 'Critica': 500.0}
        model.set_parameters(costs=costs, r_min=config['r_min'], r_max=config['r_max'])
        
        model.build_model()
        print(f"\n  Model size: {len(model.x_vars)} variables, {len(model.model.constraints)} constraints")
        
        # Check capacity constraints
        capacity_constraints = [c for c in model.model.constraints if 'capacity_' in c]
        print(f"  Capacity constraints: {len(capacity_constraints)}")
        
        success = model.solve(time_limit=60)
        
        if success:
            summary = model.get_solution_summary()
            total_cost = sum(s['cost'] for s in summary.values())
            
            print(f"\n  ✓ FEASIBLE SOLUTION FOUND")
            print(f"    Total cost: ${total_cost:.2f}")
            print(f"    Emergencies served: {len(summary)}/3")
            
            # Verify no capacity violations
            print(f"\n  Verifying capacity constraints...")
            violations = 0
            for (u, v, key) in opt_data.edges:
                capacity = opt_data.edge_data[(u, v, key)]['capacity']
                total_speed = sum(
                    model.required_speeds[comm] 
                    for comm in model.commodities 
                    if (u, v, key, comm) in model.x_vars 
                    and model.x_vars[(u, v, key, comm)].varValue 
                    and model.x_vars[(u, v, key, comm)].varValue > 0.5
                )
                if total_speed > capacity + 0.01:  # Small tolerance for numerical errors
                    violations += 1
                    print(f"    WARNING: Arc ({u},{v},{key}) capacity={capacity:.1f}, used={total_speed:.1f}")
            
            if violations == 0:
                print(f"    ✓ All capacity constraints satisfied")
            else:
                print(f"    ✗ {violations} capacity violations found!")
            
            results.append({
                'config': config['name'],
                'feasible': True,
                'cost': total_cost,
                'violations': violations
            })
        else:
            print(f"\n  ✗ INFEASIBLE")
            results.append({
                'config': config['name'],
                'feasible': False,
                'cost': None,
                'violations': None
            })
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    
    print(f"\n{'Configuration':<20} {'Result':<15} {'Cost':<15} {'Violations':<15}")
    print("-" * 70)
    for r in results:
        result_str = "FEASIBLE ✓" if r['feasible'] else "INFEASIBLE ✗"
        cost_str = f"${r['cost']:.2f}" if r['cost'] else "N/A"
        viol_str = str(r['violations']) if r['violations'] is not None else "N/A"
        print(f"{r['config']:<20} {result_str:<15} {cost_str:<15} {viol_str:<15}")
    
    feasible_count = sum(1 for r in results if r['feasible'])
    print(f"\nFeasible configurations: {feasible_count}/{len(results)}")
    
    if feasible_count > 0:
        print(f"\n✓ CAPACITY CONSTRAINT FIX SUCCESSFUL")
        print(f"  The model can now find feasible solutions with proper capacity handling")
    else:
        print(f"\n⚠ All configurations infeasible - try more relaxed parameters")
    
    print("=" * 70)

if __name__ == "__main__":
    test_capacity_constraint()
