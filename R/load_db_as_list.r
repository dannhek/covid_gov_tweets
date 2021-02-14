load_db_as_list <- function(
  user_file = NA,
  hashtag_file = NA,
  tweet_file = NA,
  url_file = NA,
  as_csv = TRUE
) {
  if (as_csv) {
    if (is.na(user_file)) { user_file <- file.path('.','db','atusers.csv') }
    if (is.na(hashtag_file)) { hashtag_file <- file.path('.','db','hashtags.csv') }  
    if (is.na(tweet_file)) { tweet_file <- file.path('.','db','tweets.csv') }
    if (is.na(url_file)) { url_file <- file.path('.','db','urlrefs.csv') }
    
    ret <- list(
      atusers   = read.csv(user_file),
      hashtags  = read.csv(hashtag_file),
      tweets    = read.csv(tweet_file),
      urlrefs   = read.csv(url_file)
    )
  }
  return(ret)
  
}