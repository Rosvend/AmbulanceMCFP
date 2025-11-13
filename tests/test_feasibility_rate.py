#!/usr/bin/env python3
"""
Test feasibility rate with various parameter combinations
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from visualization.network import NetworkManager
from optimization.data_interface import OptimizationData
from optimization.model import AmbulanceRoutingModel
import random

def test_feasibility_rate():
    print("=" * 70)
    print("FEASIBILITY RATE TESTING")
    print("=" * 70)
    
    # Load network
    nm = NetworkManager(cache_dir="../data")
    center_point = (6.2331, -75.5839)
    graph = nm.load_network(center_point, method='circle', distance=560, use_cache=True)
    
    # Test configurations
    configs = [
        {
            'name': 'Default (App defaults)',
            'c_min': 30, 'c_max': 70,
            'r_min': 20, 'r_max': 50,
            'n_tests': 10
        },
        {
            'name': 'Conservative',
            'c_min': 40, 'c_max': 80,
            'r_min': 15, 'r_max': 35,
            'n_tests': 10
        },
        {
            'name': 'Balanced',
            'c_min': 35, 'c_max': 75,
            'r_min': 18, 'r_max': 40,
            'n_tests': 10
        }
    ]
    
    costs = {'Leve': 100.0, 'Media': 250.0, 'Critica': 500.0}
    
    for config in configs:
        print(f"\n[{config['name']}]")
        print(f"  Parameters: c=[{config['c_min']},{config['c_max']}], r=[{config['r_min']},{config['r_max']}]")
        
        feasible_count = 0
        
        for i in range(config['n_tests']):
            seed = 42 + i
            random.seed(seed)
            nm.assign_random_capacities(c_min=config['c_min'], c_max=config['c_max'])
            
            origin, destinations = nm.get_random_nodes(n_destinations=3)
            destinations_with_severity = [
                (destinations[0], 'Leve'),
                (destinations[1], 'Media'),
                (destinations[2], 'Critica')
            ]
            
            opt_data = OptimizationData()
            opt_data.from_network(graph, origin, destinations_with_severity)
            
            model = AmbulanceRoutingModel(opt_data)
            model.set_parameters(costs=costs, r_min=config['r_min'], r_max=config['r_max'])
            model.build_model()
            
            success = model.solve(time_limit=30)
            if success:
                feasible_count += 1
        
        rate = (feasible_count / config['n_tests']) * 100
        print(f"  Feasibility rate: {feasible_count}/{config['n_tests']} ({rate:.0f}%)")
        
        if rate >= 80:
            print(f"  ✓ Excellent - very reliable")
        elif rate >= 60:
            print(f"  ✓ Good - mostly reliable")
        elif rate >= 40:
            print(f"  ⚠ Fair - some infeasibility expected")
        else:
            print(f"  ✗ Poor - frequent infeasibility")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS:")
    print("  - Use 'Conservative' or 'Balanced' parameters for reliable results")
    print("  - If you get infeasible, just click 'Recalculate' to try again")
    print("  - Some infeasibility is normal in optimization problems")
    print("=" * 70)

if __name__ == "__main__":
    test_feasibility_rate()
