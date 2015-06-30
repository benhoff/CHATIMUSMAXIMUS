from selenium import webdriver
from time import sleep
# TODO: dynmaically grab this from the channel using Youtube API
url = 'https://www.youtube.com/watch?v=W2DS6wT6_48'

driver = webdriver.PhantomJS()
driver.set_window_size(1000, 1000)
driver.get(url)
# NOTE: need some time for comments to load
sleep(5)
all_comments = driver.find_element_by_id("all-comments")
comments = all_comments.find_elements_by_tag_name('li')
for comment in comments:
    author = comment.find_element_by_class_name('author').text
    message = comment.find_element_by_class_name('comment-text').text
    print(author, message)
# author
# comment-text
