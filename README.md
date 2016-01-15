# spectral.ly
welcome to the project page for spectral.ly. spectra.ly is an app that is meant to identify bias in the news media, using tfidf and support vector classification.

## what problem does spectral.ly solve
there are 1million and 1 ways to look at any news-worthy event that happens. and the numerous number of articles and outlets out there all report on that event in a way that is relevant to their audience. often it is difficult to determine what these biases might be without reading the article first.

## what is spectral.ly
spectral.ly collects and analyzes articles related to a user-specified news event, and provides a ranking of all articles on the event based on:
a) how much persuasive language is being used (overall bias)
b) classification as a liberal or conservative view point

while there are numerous other forms of perspective (international vs domestic; mainstream vs non-mainstream; etc.), the ones mentioned above address the two most common forms of  perspective that readers are interested in.

## how does spectral.ly work
for the analysis of persuasive language, word frequencies on wikipedia were compared to common english-language word frequencies (wordcount.org). any word that was much less likely to appear on wikipedia was considered a 'biased' word. 

for the liberal/conservative classification, i trained a support vector classifier on 6 of the most liberal and conservative blogs online. i achieved an 80% accuracy through this classifier compared to others.

(edit: the pickle of the SVC classifier is large, and is not in this github repo. please message me if you want to gain access to it.)

## oooh.. tell me more

### astrosamurai.com my friend..