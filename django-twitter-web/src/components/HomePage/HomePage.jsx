import React, { useState, useEffect } from "react";
import Tweet from "../Tweet";

const HomePage = () => {
  const [tweets, setTweets] = useState([]);

  useEffect(() => {
    const fetchTweets = async () => {
      let response = await fetch("http://localhost:8000/api/tweets");
      let data = await response.json();
      console.log(data);
      setTweets(data);
    };

    fetchTweets();
    // eslint-disable-next-line
  }, []);

  return (
    <div className="container mx-auto px-8 py-4">
      <main className="grid grid-cols-5 gap-4">
        <div className="col-span-3 p-4">
          <form action="/create" method="POST" id="create-tweet-form">
            <div>
              <input type="hidden" value="/" name="next" />
              <textarea
                name="content"
                id="content"
                placeholder="What's happening?"
                className="w-full p-2 border-2 rounded border-pink-500 focus:border-pink-600 outline-none"
              ></textarea>
              <div className="text-xs text-red-600" id="error"></div>
            </div>
            <button
              type="submit"
              className="px-4 py-2 mt-2 bg-pink-600 text-white rounded outline-none"
              id="tweet-btn"
            >
              Tweet
            </button>
          </form>
          <h1 className="text-2xl mt-4">Latest Tweets</h1>
          <div id="tweet-container" className="mt-4">
            {tweets &&
              tweets.map((tweet, index) => <Tweet tweet={tweet} key={index} />)}
          </div>
        </div>
        <div className="col-span-2"></div>
      </main>
    </div>
  );
};

export default HomePage;
