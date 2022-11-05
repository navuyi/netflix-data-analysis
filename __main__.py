import os

import generate
from __config__ import TESTER_ID
from avenge_answers_time import avenge_answers_time
from extract_scenario import extract_scenario
from global_avenge_vmaf_to_score import global_avenge_vmaf_to_score
# from global_avenge_vmaf_to_score_colored import global_avenge_vmaf_to_score_colored
from mean_times import mean_time
from scores_distribution_per_user import scores_distribution_per_user
from global_scores_distribution import global_scores_distribution
from text_colours import colours_ids
from vmaf_plot import vmaf_plot


def main():
    generate.main()

    print(f"{colours_ids.UNDERLINE}ID testera:{colours_ids.END} {TESTER_ID}\n"
          f"{avenge_answers_time()[1]}\n"
          f"{mean_time()[1]}\n"
          f"{extract_scenario()[1]}")

    if not os.path.isdir(f"./output/{TESTER_ID}"):
        os.mkdir(f"./output/{TESTER_ID}")

    with open(f"./output/{TESTER_ID}/{TESTER_ID}_output.txt", "w") as text_file:
        text_file.write(f"ID testera: {TESTER_ID}\n"
                        f"{avenge_answers_time()[0]}\n"
                        f"{mean_time()[0]}\n"
                        f"{extract_scenario()[0]}")

    scores_distribution_per_user().savefig(f"./output/{TESTER_ID}/{TESTER_ID}_scores_distribution.png")
    vmaf_plot().savefig(f"./output/{TESTER_ID}/{TESTER_ID}_vmaf_histograms.png")
    global_avenge_vmaf_to_score(150).savefig(f"./output/avenge_vmaf_to_score_150s.png")
    global_avenge_vmaf_to_score(60).savefig(f"./output/avenge_vmaf_to_score_60s.png")
    global_avenge_vmaf_to_score(30).savefig(f"./output/avenge_vmaf_to_score_30s.png")
    # global_avenge_vmaf_to_score_colored().savefig(f"./output/avenge_vmaf_to_score_colored.png")
    global_scores_distribution().savefig(f"./output/global_scores_distribution.png")


if __name__ == "__main__":
    main()
