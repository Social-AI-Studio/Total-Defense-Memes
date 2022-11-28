#!/bin/bash
# for pillar in civil military social psychological digital economics others
# do
#     python remove_corruption.py \
#         --pillar $pillar \
#         --source /mnt/sda/dataset/google_search_results/batch1/postprocessing/grouped/$pillar \
#         --dest /mnt/sda/dataset/google_search_results/batch1/postprocessing/non_corrupted/$pillar
# done

for pillar in civil military social psychological digital economics others
do
    python deduplicate.py \
        --pillar $pillar \
        --source /mnt/sda/dataset/google_search_results/batch1/postprocessing/non_corrupted/$pillar \
        --dest /mnt/sda/dataset/google_search_results/batch1/postprocessing/deduplicated/$pillar 
done