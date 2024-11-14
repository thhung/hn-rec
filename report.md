# Report
This report is shortened to save the reader time. More details can be discussed later.

## Summary
The deliverable includes a functional web UI that recommends the top 500 HN articles, ranked in order of relevance to the user. We can import any user's bio to describe their interests. Development time was approximately 3 hours, which meets the project's requirements.

Some missing aspects:
- Benchmarking the quality of recommendations (due to limited time for data collection, but when data is available, we can use MRR as a metric to measure effectiveness, as we want the best matches to appear at the top).
- The initial run is still slow when retrieving all 500 articles; however, it will be faster on subsequent runs thanks to the caching mechanism I implemented.
## Problem Analysis
This project is optimized for rapid development. The goal is to recommend Hacker News stories that best match a given user’s preferences based on their bio. To reduce development time, I’ve simplified the problem significantly, which may affect recommendation performance.

I assume that users may have diverse interests and include all their preferences in their bio. To recommend relevant articles, we need to identify these interests and group them into similar categories. This approach requires some tuning of the algorithm. For simplicity, I chose a basic method: leveraging the tendency of users to group similar interests within the same sentence. This reframes the problem as splitting the bio into sentences and extracting the key interests from each. This can be further simplified by removing stop words within each sentence and using the remaining words as a representation of the user’s interests.

The next step is representing stories. To keep it straightforward, I used the titles of the stories as a representation of each article, hypothesizing that the title reflects the core of the content. Although this is a simplistic approach—given that many Hacker News titles are brief and sometimes obscure—the assumption is sufficient for this project. Note that we could use the entire text from the articles and comments section of HN to model the representation, but this would significantly increase the running time. Therefore, I decided to use only the title. An additional phenomenon we might observe is that the comments section often diverges from the article content due to user interactions.

The final component is measuring the match between user interests and articles. For this, I used a cross-encoder to evaluate the similarity between user preferences and story titles. The quality of this cross-encoder is crucial for delivering good recommendations. Ideally, we would collect a targeted dataset and fine-tune the cross-encoder to better meet our needs.
