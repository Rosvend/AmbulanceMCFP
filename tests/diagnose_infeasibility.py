#!/usr/bin/env python3
"""
Diagnose why the model is infeasible
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from visualization.network import NetworkManager
from optimization.data_interface import OptimizationData
from optimization.model import AmbulanceRoutingModel
import networkx as nx
import random

def diagnose_infeasibility():
    print("=" * 70)
    print("DIAGNOSING INFEASIBILITY")
    print("=" * 70)
    
    # Load network
    nm = NetworkManager(cache_dir="../data")
    center_point = (6.2331, -75.5839)
    graph = nm.load_network(center_point, method='circle', distance=560, use_cache=True)
    
    # Very relaxed parameters
    random.seed(42)
    nm.assign_random_capacities(c_min=50, c_max=100)
    
    origin, destinations = nm.get_random_nodes(n_destinations=3)
    
    print(f"\n[Connectivity Check]")
    print(f"  Origin: {origin}")
    
    for i, dest in enumerate(destinations):
        print(f"  Destination {i+1}: {dest}")
        
        # Check if path exists
        try:
            path = nx.shortest_path(graph, origin, dest)
            path_length = nx.shortest_path_length(graph, origin, dest, weight='length')
            print(f"    ✓ Path exists: {len(path)} nodes, {path_length:.1f}m")
            
            # Check capacities along path
            edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
            min_cap = float('inf')
            for u, v in edges_in_path:
                # Get all keys for this edge
                for key in graph[u][v]:
                    cap = graph[u][v][key].get('capacity', 0)
                    min_cap = min(min_cap, cap)
            print(f"    Min capacity along path: {min_cap:.1f} km/h")
            
        except nx.NetworkXNoPath:
            print(f"    ✗ NO PATH EXISTS!")
    
    # Now test with single emergency
    print(f"\n[Testing with SINGLE emergency]")
    destinations_with_severity = [(destinations[0], 'Leve')]
    
    opt_data = OptimizationData()
    opt_data.from_network(graph, origin, destinations_with_severity)
    
    model = AmbulanceRoutingModel(opt_data)
    costs = {'Leve': 100.0, 'Media': 250.0, 'Critica': 500.0}
    model.set_parameters(costs=costs, r_min=15, r_max=25)
    
    print(f"  Required speed for Leve: {model.required_speeds[model.commodities[0]]:.1f} km/h")
    
    model.build_model()
    success = model.solve(time_limit=60)
    
    if success:
        print(f"  ✓ Single emergency: FEASIBLE")
    else:
        print(f"  ✗ Single emergency: INFEASIBLE")
        print(f"     This suggests a fundamental model issue, not capacity conflicts")
    
    # Test with relaxed speed requirements
    print(f"\n[Testing with VERY LOW speed requirements]")
    destinations_with_severity = [
        (destinations[0], 'Leve'),
        (destinations[1], 'Media'),
        (destinations[2], 'Critica')
    ]
    
    opt_data = OptimizationData()
    opt_data.from_network(graph, origin, destinations_with_severity)
    
    model = AmbulanceRoutingModel(opt_data)
    model.set_parameters(costs=costs, r_min=5, r_max=15)
    
    print(f"  Speed requirements:")
    for comm in model.commodities:
        print(f"    {comm[1]}: {model.required_speeds[comm]:.1f} km/h")
    
    model.build_model()
    success = model.solve(time_limit=60)
    
    if success:
        print(f"  ✓ Three emergencies with low speeds: FEASIBLE")
        summary = model.get_solution_summary()
        
        # Check for shared edges
        print(f"\n  Checking for shared road segments...")
        edge_usage = {}
        for comm in model.commodities:
            arcs = model.solution[comm]
            for u, v, key in arcs:
                edge_key = (u, v, key)
                if edge_key not in edge_usage:
                    edge_usage[edge_key] = []
                edge_usage[edge_key].append(comm)
        
        shared_edges = {k: v for k, v in edge_usage.items() if len(v) > 1}
        if shared_edges:
            print(f"    Found {len(shared_edges)} shared road segments")
            for (u, v, key), comms in list(shared_edges.items())[:3]:
                cap = graph[u][v][key]['capacity']
                total_speed = sum(model.required_speeds[c] for c in comms)
                print(f"      Arc ({u},{v},{key}): capacity={cap:.1f}, used by {len(comms)} routes, total_speed={total_speed:.1f}")
        else:
            print(f"    No shared road segments (routes are disjoint)")
    else:
        print(f"  ✗ Three emergencies with low speeds: STILL INFEASIBLE")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    diagnose_infeasibility()
