# Extended Experiments - Music Plagiarism Detection via Bipartite Graph Matching



## Tune piece length $l$

We firstly tune the hyperparameter piece length. We can find that the optimal length is **7** as a short piece cannot well represent the melody while a long piece is not sensitive to plag-degree. A piece length of 7 is about two to three bars in music, which explains why

they are optimal.

| Piece Length | Average Index |  Accuracy  |
| :----------: | :-----------: | :--------: |
|      4       |     4.08      |   0.6253   |
|      5       |     4.15      |   0.6766   |
|      6       |     4.06      |   0.6270   |
|    **7**     |   **3.65**    | **0.7473** |
|      8       |     3.88      |   0.6447   |
|      9       |     4.38      |   0.5248   |
|      10      |     4.60      |   0.5252   |
|      11      |     5.17      |   0.4743   |
|      12      |     5.89      |   0.4743   |



## Tune the overlapping rate $r$

Then we tune the overlapping rate. We find that **0.9** is the best overlap rate for two datasets since it can best detect plagiarism but will high time consumption.

| Overlap Rate | Average Index |  Accuracy  |
| :----------: | :-----------: | :--------: |
|     0.0      |     3.40      |   0.5601   |
|     0.1      |     3.40      |   0.5601   |
|     0.2      |     3.68      |   0.6451   |
|     0.3      |     3.52      |   0.6968   |
|     0.4      |     3.83      |   0.7641   |
|     0.5      |     4.26      |   0.6779   |
|     0.6      |     3.67      |   0.6614   |
|     0.7      |     3.67      |   0.6614   |
|     0.8      |     3.51      |   0.7801   |
|   **0.9**    |   **3.40**    | **0.7801** |



## Tune on duration weight $k_{duration}$

Next, we tune the duration weight $k_{duration}$. We find that 0 is optimal $k_{duration}$, which means considering duration can harm the performance. The reason may be that the relative duration will omit some valuable information of duration.

| $k_{duration}$ | Average Index |  Accuracy  |
| :------------: | :-----------: | :--------: |
|    **0.0**     |   **3.39**    | **0.8145** |
|      0.1       |     3.53      |   0.7288   |
|      0.2       |     3.71      |   0.6602   |
|      0.3       |     3.79      |   0.6430   |
|      0.4       |     3.78      |   0.6430   |
|      0.5       |     4.11      |   0.6430   |
|      0.6       |     4.06      |   0.6430   |
|      0.7       |     4.11      |   0.6598   |
|      0.8       |     4.18      |   0.6598   |



## Tune on downbeat weight $k_{downbeat}$

Finally, we test different weights of downbeats.  We get the optimal downbeat **2** for accuracy, which adds proper importance to the downbeats since it affects the rhythm and emotion of music.

| $k_{downbeat}$ | Average Index | Accuracy |
| :------------: | :-----------: | :------: |
|      1.2       |     3.77      |  0.7284  |
|      1.3       |     3.78      |  0.7111  |
|      1.4       |     3.69      |  0.6728  |
|      1.5       |     3.62      |  0.7284  |
|      1.6       |     3.68      |  0.7115  |
|      1.7       |     3.61      |  0.7115  |
|      1.8       |     3.59      |  0.7115  |
|       2        |     3.57      |  0.7115  |
|      2.5       |     3.62      |  0.7115  |
|       3        |     3.61      |  0.7115  |

