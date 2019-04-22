# indonesia-pos-tagger
<p>Building Indonesia POS Tagger by three different methos. There are baseline, statistic, and sequence approach.
The trained dataset used is the corps of POSTag which can be downloaded from http://bahasa.cs.ui.ac.id/postag/corpus. In the construction of training data, the first 1000 sentences are used, and the next 20 sentences are as test sentences.

<b>Baseline</b>
The baseline method is used by tagging the test sentence with frequency
words and tags that appear most often on training data or corpus that have been made. In the baseline model that has been made, the accuracy rate is 97.97297297297297%. In the 20 test sentences tested there were a total of 296 tags, and tags that were correctly predicted were 290 tags.

<b>Statistic</b>
On this issue the POSTagging problem is solved by classification. The algorithm used to perform the classification process is ID3. The accuracy obtained in this model is 92.94117647058823%.

<b>Sequence</b>
In testing using sequence modeling methods, the HMM-Viterbi algorithm is used to predict tags in the test sentence. In this method the accuracy is 86.14864864864865%. In the 20 test sentences that were tried there were a total of 296 tags, and tags that were successfully predicted correctly were 255 tags.
</p>
