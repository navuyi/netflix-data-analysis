import os

import matplotlib.pyplot as plt

# import generate
from __config__ import TESTERS_ID
from average_answers_time import average_answers_time
from extract_scenario import extract_scenario
from global_vmaf_distribution import global_vmaf_distribution
from scenarios_usage_stats import scenarios_usage_stats
from global_average_vmaf_to_score import global_average_vmaf_to_score
# from global_average_vmaf_to_score_colored import global_average_vmaf_to_score_colored
from mean_times import mean_time
from scores_distribution_per_user import scores_distribution_per_user
from global_scores_distribution import global_scores_distribution
from sql import sql
from text_colours import colours_ids
from vmaf_plot import vmaf_plot


def main():
    # generate.main()

    global_average_vmaf_to_score(150).savefig(f"./output/functions_mapping/points_plots/average_vmaf_to_score_150s.png")
    global_average_vmaf_to_score(60).savefig(f"./output/functions_mapping/points_plots/average_vmaf_to_score_60s.png")
    global_average_vmaf_to_score(30).savefig(f"./output/functions_mapping/points_plots/average_vmaf_to_score_30s.png")
    # global_average_vmaf_to_score_colored().savefig(f"./output/average_vmaf_to_score_colored.png")
    global_scores_distribution().savefig(f"./output/stats/global_scores_distribution.png")
    scenarios_usage_stats().savefig(f"./output/stats/scenarios_usage_stats.png")
    global_vmaf_distribution().savefig(f"./output/stats/global_vmaf_distribution_from_scenario.png")

    plt.close('all')

    print(f"{colours_ids.OK_GREEN}Global stats processed{colours_ids.END}")

    for TESTER_ID in TESTERS_ID:
        sql_request = f"select video.id, video.video_index from video " \
                      f"inner join experiment " \
                      f"on video.experiment_id = experiment.id " \
                      f"where experiment.tester_id == '{TESTER_ID}'"

        video_ids = sql(sql_request)

        for video_id in video_ids:
            if os.path.isdir(f"./output/{TESTER_ID}_{video_id[0]}"):
                print(f"{colours_ids.WARNING}Tester {TESTER_ID}_{video_id[0]} "
                      f"already processed{colours_ids.END}")
                continue

            os.mkdir(f"./output/{TESTER_ID}_{video_id[0]}")

            print(f"{colours_ids.OK_BLUE}Processing tester {TESTER_ID}_{video_id[0]}{colours_ids.END}")

            with open(f"./output/{TESTER_ID}_{video_id[0]}/{TESTER_ID}_{video_id[0]}_output.txt", "w") as text_file:
                text_file.write(f"ID testera: {TESTER_ID}_{video_id[0]}\n"
                                f"{average_answers_time(video_id[0])[0]}\n"
                                f"{mean_time(video_id[0])[0]}\n"
                                f"{extract_scenario(TESTER_ID, video_id[1])[0]}")

            scores_distribution_per_user(TESTER_ID, video_id[0]).savefig(f"./output/{TESTER_ID}_{video_id[0]}/"
                                                                         f"{TESTER_ID}_{video_id[0]}"
                                                                         f"_scores_distribution.png")
            vmaf_plot(TESTER_ID, video_id[0], video_id[1]).savefig(f"./output/{TESTER_ID}_{video_id[0]}/"
                                                                   f"{TESTER_ID}_{video_id[0]}_vmaf_histograms.png")

            plt.close('all')

            print(f"{colours_ids.OK_GREEN}Processed tester {TESTER_ID}_{video_id[0]}{colours_ids.END}")


if __name__ == "__main__":
    main()
