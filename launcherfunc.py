import os
import math
import subprocess

random_seeds = [42]
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def ils_launcher(
    tsp_base,
    number_of_items_per_city,
    knapsack_type,
    knapsack_size,
    maximum_travel_time,
    repetition
):
    if knapsack_size != "inf":
        knapsack_size = f"{int(knapsack_size):02d}"

    inputfile = (
        "thop-instances/%s-thop/%s_%02d_%s_%s_%02d.thop"
        % (
            tsp_base,
            tsp_base,
            number_of_items_per_city,
            knapsack_type,
            knapsack_size,
            maximum_travel_time
        )
    )

    outputfile = (
        "solutions/%s/%s-thop/%s_%02d_%s_%s_%02d_%02d.thop.sol"
        % (
            "ils",
            tsp_base,
            tsp_base,
            number_of_items_per_city,
            knapsack_type,
            knapsack_size,
            maximum_travel_time,
            repetition + 1
        )
    )

    timelimit = math.ceil(
        (
            int(
                ''.join(
                    filter(lambda x: x.isdigit(), tsp_base)
                )
            ) - 2
        )
        * number_of_items_per_city
        / 10.0
    )

    cmd = [
        "./ilsthop",
        "--inputfile", inputfile,
        "--seed", str(random_seeds[repetition]),
        "--time", str(timelimit),
        "--outputfile", outputfile
    ]

    print(
        "CMD:",
        " ".join(cmd),
        flush=True
    )
    import os

    print("PWD =", os.getcwd())
    print("INPUT =", inputfile)
    print("EXISTS =", os.path.exists(inputfile))
    print("ABS =", os.path.abspath(inputfile))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print("STDERR:", result.stderr)

def brkga_launcher(tsp_base, number_of_items_per_city,
                   knapsack_type, knapsack_size,
                   maximum_travel_time, repetition):

    import os
    import math
    import subprocess

    try:

        # ===== FIX TYPES =====
        number_of_items_per_city = int(number_of_items_per_city)
        maximum_travel_time = int(maximum_travel_time)

        if knapsack_size != "inf":
            knapsack_size = f"{int(knapsack_size):02d}"

        # ===== PATHS =====
        inputfile = (
            f"thop-instances/{tsp_base}-thop/"
            f"{tsp_base}_{number_of_items_per_city:02d}_"
            f"{knapsack_type}_{knapsack_size}_"
            f"{maximum_travel_time:02d}.thop"
        )

        outputfile = (
            f"solutions/brkga/{tsp_base}-thop/"
            f"{tsp_base}_{number_of_items_per_city:02d}_"
            f"{knapsack_type}_{knapsack_size}_"
            f"{maximum_travel_time:02d}_"
            f"{repetition + 1:02d}.thop.sol"
        )

        # ===== RUNTIME =====
        runtime = math.ceil(
            (int(''.join(filter(str.isdigit, tsp_base))) - 2)
            * number_of_items_per_city / 10.0
        )

        # ===== CREATE OUTPUT DIR =====
        os.makedirs(
            os.path.dirname(outputfile),
            exist_ok=True
        )

        # ===== BRKGA PARAMETERS =====
        p = 100
        pe = 0.25
        pm = 0.30
        rhoe = 0.6
        lsfreq = 50
        seed = int(random_seeds[repetition])

        # ===== DEBUG =====
        print("\n===== DEBUG =====")
        print("inputfile :", inputfile)
        print("outputfile:", outputfile)
        print("runtime   :", runtime)
        print("seed      :", seed)
        print("=================\n")

        # ===== COMMAND =====
        cmd = (
            f"./brkgathop "
            f"--inputfile {inputfile} "
            f"--p {p} "
            f"--pe {pe} "
            f"--pm {pm} "
            f"--rhoe {rhoe} "
            f"--lsfreq {lsfreq} "
            f"--seed {seed} "
            f"--time {runtime} "
            f"--outputfile {outputfile}"
        )

        print("\n====================")
        print(cmd)
        print("====================\n")

        # ===== RUN =====
        result = subprocess.run(
            cmd,
            shell=True,
            text=True
        )

        print("\nRETURN CODE:", result.returncode)

    except Exception as e:

        print("\n!!!!!!!! ERROR !!!!!!!!")
        print(type(e))
        print(e)
        print("!!!!!!!!!!!!!!!!!!!!!!!\n")

def aco_launcher(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time, repetition, runtime_factor="1x"):
    if knapsack_size != "inf": 
        knapsack_size = "%02d" % (knapsack_size, )

    inputfile = os.path.join(
        ROOT_DIR,
        "thop-instances",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}.thop"
    )
    outputfile = os.path.join(
        ROOT_DIR,
        "solutions",
        "aco",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}_{repetition + 1:02d}.thop.sol"
    )
    os.makedirs(os.path.dirname(outputfile), exist_ok=True)

    fixed_parameters = "--ants 196 --alpha 1.24 --beta 5.46 --rho 0.51 --ptries 1"
    current_seed = random_seeds[repetition]
    calculated_time = float(runtime_factor.replace('x','')) * math.ceil((int(''.join(filter(lambda x: x.isdigit(), tsp_base))) - 2) * number_of_items_per_city / 10.0)

    executable = os.path.join(ROOT_DIR, "src", "aco", "acothop")
    cmd = [
        executable,
        "--mmas",
        "--tries", "1",
        "--seed", str(current_seed),
        "--time", "%.1f" % calculated_time,
        "--inputfile", inputfile,
        "--outputfile", outputfile,
    ] + fixed_parameters.split() + ["--log"]

    print("CMD:", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print("RETURN CODE:", result.returncode)

def acopp_launcher(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time, repetition, runtime_factor="1x"):
    if knapsack_size != "inf":
        knapsack_size = "%02d" % (knapsack_size, )

    inputfile = os.path.join(
        ROOT_DIR,
        "thop-instances",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}.thop"
    )
    outputfile = os.path.join(
        ROOT_DIR,
        "solutions",
        "aco++",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}_{repetition + 1:02d}.thop.sol"
    )
    os.makedirs(os.path.dirname(outputfile), exist_ok=True)

    fixed_parameters = "--ants 196 --alpha 1.24 --beta 5.46 --rho 0.51 --ptries 1"
    current_seed = random_seeds[repetition]
    calculated_time = float(runtime_factor.replace('x','').replace('t','')) * math.ceil((int(''.join(filter(lambda x: x.isdigit(), tsp_base))) - 2) * number_of_items_per_city / 10.0)

    executable = os.path.join(ROOT_DIR, "src", "aco++", "acothop")
    cmd = [
        executable,
        "--mmas",
        "--tries", "1",
        "--seed", str(current_seed),
        "--time", "%.1f" % calculated_time,
        "--inputfile", inputfile,
        "--outputfile", outputfile,
    ] + fixed_parameters.split() + ["--log"]

    print("CMD:", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print("RETURN CODE:", result.returncode)


def saashc_launcher(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time, repetition, runtime_factor="1x"):
    if knapsack_size != "inf":
        knapsack_size = "%02d" % (knapsack_size, )

    inputfile = os.path.join(
        ROOT_DIR,
        "thop-instances",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}.thop"
    )
    outputfile = os.path.join(
        ROOT_DIR,
        "solutions",
        "saashc",
        f"{tsp_base}-thop",
        f"{tsp_base}_{number_of_items_per_city:02d}_{knapsack_type}_{knapsack_size}_{maximum_travel_time:02d}_{repetition + 1:02d}.thop.sol"
    )
    os.makedirs(os.path.dirname(outputfile), exist_ok=True)

    fixed_parameters = "--ants 196 --alpha 1.24 --beta 5.46 --rho 0.51 --ptries 1"
    current_seed = random_seeds[repetition]
    calculated_time = float(runtime_factor.replace('x','')) * math.ceil((int(''.join(filter(lambda x: x.isdigit(), tsp_base))) - 2) * number_of_items_per_city / 10.0)

    executable = os.path.join(ROOT_DIR, "src", "saashc", "build", "acothop")
    cmd = [
        executable,
        "--mmas",
        "--tries", "1",
        "--seed", str(current_seed),
        "--time", "%.1f" % calculated_time,
        "--inputfile", inputfile,
        "--outputfile", outputfile,
    ] + fixed_parameters.split() + ["--log"]

    print("CMD:", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print("RETURN CODE:", result.returncode)