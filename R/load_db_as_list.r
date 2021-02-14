load_db_as_list <- function(
  user_file = NA,
  hashtag_file = NA,
  tweet_file = NA,
  url_file = NA
) {
  if (is.na(user_file)) { user_file <- file.path('.','db','user_file.csv')  
  if (is.na(hashtag_file)) { hashtag_file <- file.path('.','db','hashtag_file.csv')  
  if (is.na(tweet_file)) { tweet_file <- file.path('.','db','tweet_file.csv')  
  if (is.na(url_file)) { url_file <- file.path('.','db','url_file.csv') 
  
  
  
}