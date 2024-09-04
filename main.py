from helpers.selenium_helper import get_driver, validate_links,extract_asu_profile

driver = get_driver()
links = validate_links(driver,'professor_name')
extract_asu_profile(driver,links['asu_profile'])
