# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:27:03 2023

@author: madhu
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import pandas as pd
def get_jobs(keyword, num_jobs, verbose,wait_time,c_path):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    driver_path = Service(executable_path=c_path)
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    #driver = webdriver.Chrome(executable_path="/Users/omersakarya/Documents/GitHub/scraping-glassdoor-selenium/chromedriver", options=options)
    #driver = webdriver.Chrome(executable_path= c_path, options=options)
    
    #driver = webdriver.Chrome(service= driver_path, options=options)
    driver = webdriver.Chrome()
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []
    
    # Create a WebDriverWait object with a timeout value (e.g., 10 seconds)
    wait = WebDriverWait(driver, 10)

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(wait_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            #driver.find_element_by_class_name("selected").click()
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1) 

        try:
            #driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
            #driver.find_element(By.CSS_SELECTOR , '[alt= "Close"]').click()
            # Wait for the close button to be clickable
            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-role-variant="ghost"]')))
            
            # Click the close button
            close_button.click()

            print('clicked the x')

        except NoSuchElementException:
            print('failed to click x')
            pass

        
        #Going through each job in this page
        #job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        #job_buttons = driver.find_element(By.CLASS_NAME,"jl")  #jl for Job Listing. These are the buttons we're going to click.

        # Wait for the job listings to load
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        #print('job:', job_buttons)
        
        # Placeholder for the job ID
        job_id_placeholder = "job-employer-{}"
        
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(5)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    # company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    # location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    # job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    # job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    
                    job_id = job_button.get_attribute("data-id")  # Assuming the job ID is stored in data-id attribute
                 
                    company_name = driver.find_element( "xpath",f'//*[@id="job-employer-{job_id}"]').text
                    location = driver.find_element( "xpath",f'//*[@id="job-location-{job_id}"]').text
                    job_title = driver.find_element( "xpath",f'//*[@id="job-title-{job_id}"]').text
                    #job_description = driver.find_element( "xpath",'//*[@id="job-tile-1008730636845"]').text
                    
                    
                    collected_successfully = True
                    time.sleep(3)
                except Exception as e:
                    print(f'Error occurred: {str(e)}')
                    #print(driver.page_source)
                    time.sleep(5)
                    print('ERRRRR-1')

            try:
                #salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
                salary_estimate = driver.find_element( "xpath",f'//*[@id="job-salary-{job_id}"]').text
            except NoSuchElementException:
                print('ERRRRR-2')
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            # try:
            #     #rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            #     rating = driver.find_element('xpath',f'//*[@id="job-employer-{job_id}"]/div[2]/span[2]').text
            # #except NoSuchElementException:
            # except Exception as e:
            #     print(f'Error occurred: {str(e)}')
            #     rating = -1 #You need to set a "not found value. It's important."
                        
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                # print("Job Description: {}".format(job_description[:500]))
                #print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element('xpath','.//div[@class="tab" and @data-tab-type="overview"]').click()
                print(driver.page_source)
                print('Err-Overview')

                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    headquarters = driver.find_element('xpath','//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[4]/div[1]/div[3]').text
                #except NoSuchElementException:
                except Exception as e:
                    print(f'Error occurred: {str(e)}')
                    print('Err at headqtr')
                    headquarters = -1

            #     try:
            #         size = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         size = -1

            #     try:
            #         founded = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         founded = -1

            #     try:
            #         type_of_ownership = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         type_of_ownership = -1

            #     try:
            #         industry = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         industry = -1

            #     try:
            #         sector = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         sector = -1

            #     try:
            #         revenue = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         revenue = -1

            #     try:
            #         competitors = driver.find_element('xpath','.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         competitors = -1

            except NoSuchElementException: #Rarely, some job postings do not have the "Company" tab.
                print('err')
            
                    
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

                
            # if verbose:
                print("Headquarters: {}".format(headquarters))
            #     print("Size: {}".format(size))
            #     print("Founded: {}".format(founded))
            #     print("Type of Ownership: {}".format(type_of_ownership))
            #     print("Industry: {}".format(industry))
            #     print("Sector: {}".format(sector))
            #     print("Revenue: {}".format(revenue))
            #     print("Competitors: {}".format(competitors))
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({
            "Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            # "Job Description" : job_description,
            #"Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            # "Size" : size,
            # "Founded" : founded,
            # "Type of ownership" : type_of_ownership,
            # "Industry" : industry,
            # "Sector" : sector,
            # "Revenue" : revenue,
            # "Competitors" : competitors
            })
            #add job to jobs
          

        #Clicking on the "next page" button
        try:
            driver.find_element('xpath','//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

