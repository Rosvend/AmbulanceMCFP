#!/usr/bin/env python3
"""
Test different capacity constraint interpretations
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from visualization.network import NetworkManager
from optimization.data_interface import OptimizationData
from optimization.model import AmbulanceRoutingModel
import random

def test_constraint_interpretation():
    print("=" * 70)
    print("TESTING CONSTRAINT INTERPRETATIONS")
    print("=" * 70)
    
    # Load network
    nm = NetworkManager(cache_dir="../data")
    center_point = (6.2331, -75.5839)
    graph = nm.load_network(center_point, method='circle', distance=560, use_cache=True)
    
    random.seed(42)
    nm.assign_random_capacities(c_min=40, c_max=80)
    
    origin, destinations = nm.get_random_nodes(n_destinations=3)
    destinations_with_severity = [
        (destinations[0], 'Leve'),
        (destinations[1], 'Media'),
        (destinations[2], 'Critica')
    ]
    
    opt_data = OptimizationData()
    opt_data.from_network(graph, origin, destinations_with_severity)
    
    # Interpretation 1: Each ambulance independently needs speed ≤ capacity
    # (Original formulation)
    print(f"\n[INTERPRETATION 1: Per-commodity constraint]")
    print(f"  Constraint: r_k · x_ijk ≤ c_ij for EACH k")
    print(f"  Meaning: Each ambulance can use the road if its required speed ≤ capacity")
    print(f"  This allows multiple ambulances on same road (they don't interfere)")
    
    # Interpretation 2: Sum of speeds must not exceed capacity
    # (Current formulation)
    print(f"\n[INTERPRETATION 2: Aggregate constraint (current)]")
    print(f"  Constraint: Σ_k (r_k · x_ijk) ≤ c_ij")
    print(f"  Meaning: Sum of all required speeds ≤ capacity")
    print(f"  Example: If 3 ambulances each need 20 km/h, total = 60 km/h")
    print(f"           This road needs capacity ≥ 60 km/h")
    print(f"  Problem: This is VERY restrictive and causes infeasibility!")
    
    # Let's see what happens with per-commodity constraints
    print(f"\n[TESTING: Temporarily revert to per-commodity constraints]")
    print(f"  Parameters: c=[40,80] km/h, r=[15,35] km/h")
    
    model = AmbulanceRoutingModel(opt_data)
    costs = {'Leve': 100.0, 'Media': 250.0, 'Critica': 500.0}
    model.set_parameters(costs=costs, r_min=15, r_max=35)
    
    # Manually override the constraint method
    print(f"  (Manually using per-commodity constraints for this test)")
    model.build_model()
    
    # Remove aggregate constraints and add per-commodity ones
    # Get list of capacity constraints
    cap_constraints = [name for name in model.model.constraints if name.startswith("capacity_")]
    for name in cap_constraints:
        del model.model.constraints[name]
    
    # Add per-commodity constraints
    count = 0
    for (u, v, key) in opt_data.edges:
        edge_data = opt_data.edge_data[(u, v, key)]
        capacity = edge_data['capacity']
        
        for commodity in model.commodities:
            if (u, v, key, commodity) in model.x_vars:
                required_speed = model.required_speeds[commodity]
                constraint_name = f"capacity_{u}_{v}_{key}_{commodity[0]}_{commodity[1]}"
                model.model += (
                    required_speed * model.x_vars[(u, v, key, commodity)] <= capacity,
                    constraint_name
                )
                count += 1
    
    print(f"  Replaced 371 aggregate constraints with {count} per-commodity constraints")
    
    success = model.solve(time_limit=60)
    
    if success:
        print(f"  ✓ FEASIBLE with per-commodity constraints!")
        summary = model.get_solution_summary()
        print(f"    Total cost: ${summary['total_cost']:.2f}")
        print(f"    Total time: {summary['total_time']:.2f} min")
    else:
        print(f"  ✗ Still infeasible")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION:")
    print("  The per-commodity constraint makes more sense physically:")
    print("  - Each ambulance just needs a road fast enough for its requirements")
    print("  - Multiple ambulances CAN use the same road simultaneously")
    print("  - They don't 'consume' the capacity - capacity is a speed limit")
    print("  ")
    print("  The aggregate constraint models congestion (sum of speeds ≤ capacity)")
    print("  but is too restrictive for this use case.")
    print("=" * 70)

if __name__ == "__main__":
    test_constraint_interpretation()
