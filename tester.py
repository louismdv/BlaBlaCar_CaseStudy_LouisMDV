import subprocess


script_path = 'route_tracer.py'

valid1 = """Paris - Bercy seine bus station, 48.83568689, 2.380160747
Lyon - Perrache bus station, 45.749711, 4.826788
done
n
"""
# valid error case
valid2 = """Lille - Europe train station, 50.638638, 3.076491
Lyon - Perrache bus station, 45.749711, 4.826788
Lyon - Perrache bus station, 45.749711, 4.826788
done
n
"""
invalid3 = """NYC - Grand Central Terminal, 40.75348761927637, -73.97677339839454
Lyon - Perrache bus station, 45.749711, 4.826788
done
n
"""
invalid4 = """Ajaccio - Gare Routiere, 41.91920323105271, 8.751207693498317
Lyon - Perrache bus station, 45.749711, 4.826788
done
n
"""
invalid5 = """Santa Cruz de Flores - Gare, 39.47630628991925, -31.036264781203652
Lyon - Perrache bus station, 45.749711, 4.826788
done
n
"""


def run_test(name, input_str):
    print(f"\n\033[1;33m===== Running {name} =====\033[0m\n")
    result = subprocess.run(
        ['python3', script_path],
        input=input_str,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)


run_test("valid1", valid1)
run_test("valid2", valid2)
run_test("invalid3", invalid3)
run_test("invalid4", invalid4)
run_test("invalid5", invalid5)


