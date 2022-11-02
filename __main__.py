import subprocess

from __config__ import TESTER_ID
from avenge_answers_time import avenge_answers_time
from extract_scenario import extract_scenario
from mean_times import mean_time
from scores_distribution import scores_distribution
from text_colours import colours_ids
from vmaf_plot import vmaf_plot
import generate


def main():
    generate.main()
    subprocess.call(["/usr/bin/Rscript", "./R-scripts/data_analysis.R"])

    print(f"{colours_ids.UNDERLINE}ID testera:{colours_ids.END} {TESTER_ID}\n"
          f"{avenge_answers_time()}\n"
          f"{mean_time()}\n"
          f"{scores_distribution()}\n"
          f"{extract_scenario()}")

    vmaf_plot()


if __name__ == "__main__":
    main()
