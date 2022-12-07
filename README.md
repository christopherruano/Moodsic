# Moodsic

Moodsic is a web-application dedicated to evaluating a user’s listening habits and returning an analysis of the user’s mood swings over a long, medium, and short term time period. Each time period listed previously presents an aggregation of user listening habits over the course of a set time: short is roughly a month; medium is up to 6 months; long parses over the user’s complete listening history. Mood or happiness versus sadness is measured by the valence of each individual song played by the user’s spotify account, a metric created by spotify themselves that measures the perceived negative emotion of a song. Spotify themselves say valence "describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (happy, cheerful, euphoric), while tracks with low valence sound more negative (sad, depressed, angry)".

Moodsic’s application extends beyond retail-usage. Recent studies suggest a strong correlation between mood and music listening habits, stressing how emotional context can be derived from these individual specific listening habits. Moreover, further studies have explored a compounding effect of sad music on existing depression. As mental health awareness becomes a growing concern for society, Moodsic attempts to democratize self-diagnosis in lieu of further studies that offer more comprehensive conclusions (see articles below).

Users are first introduced to Moodsic via a landing page which introduces users to Moodsic’s functions and prompts the user to login via a Spotify-led authentication process. Note: Moodsic does not store, share, or reveal personal data at any point in time. Moodsic then queries for, operates on, and independently returns segments of digestible data to users on the results page of the application. Session data allows user ‘login’ and ‘session’ data to be stored for future interactivity and local memory. By logging out, users are able to return back to the application homepage and clear session data.

Use of Moodsic is slightly more complex than simple git repository download, navigation, and run command prompts. Local running on the effort of third-party developers requires an account on Spotfiy’s developers platform - Spotipy. Successful login, authentication, and navigation allows for two crucial pieces of information for application configuration: API secret key and client key - a unique sequence of alphanumerics that initializes API requests, data queries, and subsequent analysis. Please visit https://developer.spotify.com to learn more about application functionality, API usage, and documentation.


Music habits and correlation with mental health status: https://www.sciencedaily.com/releases/2015/10/151022094959.htm
The power of sad, angry, and generally negative music to worsen symptoms of mental health: https://journals.sagepub.com/doi/full/10.1177/20592043211057217
Info on valence: https://community.spotify.com/t5/Spotify-for-Developers/Valence-as-a-measure-of-happiness/td-p/4385221

Youtube link:
