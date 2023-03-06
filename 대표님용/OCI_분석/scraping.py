from selenium import webdriver

# Set up the Chrome driver
driver = webdriver.Chrome('./chromedriver.exe')

# Load the webpage
driver.get('https://finance.naver.com/item/board.naver')

# Find the first post on the page
post = driver.find_element_by_xpath('//table[@class="type2"]//tr[2]')

# Extract the title and author of the post
title = post.find_element_by_css_selector('.title').text
author = post.find_element_by_css_selector('.p11').text

# Print the results
print('Title:', title)
print('Author:', author)

# Close the driver
driver.quit()


https://finance.naver.com/item/board_read.naver?code=010060&nid=241219521&st=&sw=&page=1

https://finance.naver.com/item/board_read.naver?code=010060&nid=241213886&st=&sw=&page=1

https://finance.naver.com/item/board_read.naver?code=010060&nid=241209642&st=&sw=&page=1


https://finance.naver.com/item/board.naver?code=010060&page=2