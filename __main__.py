import subprocess
from PIL import Image

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
          f"{extract_scenario()}")

    scores_distribution().savefig(f"./images/_{TESTER_ID}_scores_distribution.png")
    vmaf_plot().savefig(f"./images/{TESTER_ID}_vmaf_histograms.png")

    images = [Image.open(f"./images/_{TESTER_ID}_scores_distribution.png"),
              Image.open(f"./images/{TESTER_ID}_vmaf_histograms.png")]

    images[0].show()
    images[1].show()


if __name__ == "__main__":
    main()
