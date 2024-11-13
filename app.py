import streamlit as st

from hnrecommender import recommend_hacker_news

# Streamlit UI
st.title("HNews Recommendation")

# Text input for the user to enter a query
user_bio = st.text_area("Enter the user bio:", height=100)

# Submit button
if st.button("Submit"):
    if user_bio:
        # Show spinner
        with st.spinner("Fetching articles... Please wait."):
            articles = recommend_hacker_news(user_bio, 500)

        # Display the results after processing
        st.success("Here are the articles recommended for you:")
        for story in articles:
            title = story["title"] if "title" in story else "No title article"
            url = story["url"] if "url" in story else "HN article"
            st.write(f"[{title}]({url})")
    else:
        st.error("Please enter an user bio.")
