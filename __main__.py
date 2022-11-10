import os

import matplotlib.pyplot as plt

import generate
from __config__ import TESTERS_ID
from avenge_answers_time import avenge_answers_time
from extract_scenario import extract_scenario
from global_stats.global_vmaf_distribution import global_vmaf_distribution
from global_stats.scenarios_usage_stats import scenarios_usage_stats
from global_stats.global_avenge_vmaf_to_score import global_avenge_vmaf_to_score
# from global_avenge_vmaf_to_score_colored import global_avenge_vmaf_to_score_colored
from mean_times import mean_time
from global_stats.scores_distribution_per_user import scores_distribution_per_user
from global_stats.global_scores_distribution import global_scores_distribution
from text_colours import colours_ids
from vmaf_plot import vmaf_plot


def main():
    generate.main()

    global_avenge_vmaf_to_score(150).savefig(f"./output/avenge_vmaf_to_score_150s.png")
    global_avenge_vmaf_to_score(60).savefig(f"./output/avenge_vmaf_to_score_60s.png")
    global_avenge_vmaf_to_score(30).savefig(f"./output/avenge_vmaf_to_score_30s.png")
    # global_avenge_vmaf_to_score_colored().savefig(f"./output/avenge_vmaf_to_score_colored.png")
    global_scores_distribution().savefig(f"./output/global_scores_distribution.png")
    scenarios_usage_stats().savefig(f"./output/scenarios_usage_stats.png")
    global_vmaf_distribution().savefig(f"./output/global_vmaf_distribution_from_scenario.png")

    plt.close('all')

    print(f"{colours_ids.OK_GREEN}Global stats processed{colours_ids.END}")

    for TESTER_ID in TESTERS_ID:
        if not os.path.isdir(f"./output/{TESTER_ID}"):
            os.mkdir(f"./output/{TESTER_ID}")
        else:
            print(f"{colours_ids.WARNING}Tester {TESTER_ID} "
                  f"already processed{colours_ids.END}")
            continue

        print(f"{colours_ids.OK_BLUE}Processing tester {TESTER_ID}{colours_ids.END}")

        with open(f"./output/{TESTER_ID}/{TESTER_ID}_output.txt", "w") as text_file:
            text_file.write(f"ID testera: {TESTER_ID}\n"
                            f"{avenge_answers_time(TESTER_ID)[0]}\n"
                            f"{mean_time(TESTER_ID)[0]}\n"
                            f"{extract_scenario(TESTER_ID)[0]}")

        scores_distribution_per_user(TESTER_ID).savefig(f"./output/{TESTER_ID}/{TESTER_ID}_scores_distribution.png")
        vmaf_plot(TESTER_ID).savefig(f"./output/{TESTER_ID}/{TESTER_ID}_vmaf_histograms.png")

        plt.close('all')

        print(f"{colours_ids.OK_GREEN}Processed tester {TESTER_ID}{colours_ids.END}")


if __name__ == "__main__":
    main()
