from selenium import webdriver;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import unittest;


chrome_options = Options();
prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_experimental_option("detach", True);

browser = webdriver.Chrome(options=chrome_options);
browser.implicitly_wait(5);

class Testing(unittest.TestCase):
    # def setUp(self):
    #     return
    # def tearDown(self):
    #     self.browser.quit();
    @unittest.skip("skipping")
    def test_google_title(self):
        # browser = self.browser
        browser.get('http://google.com');
        try:
            self.assertTrue('Google', browser.title);
            self.assertNotEqual('Goog', browser.title);
            # print("Google title test is Present.");
        
        except AssertionError as e:
            print(f"!!!Google title test failed. {e}");
            raise
    
    @unittest.skip("skip")
    def test_login_practice(self):
        # browser = self.browser
        browser.get("https://proleed.academy/exercises/selenium/selenium-element-id-locators-practice-form.php");

        email = browser.find_element(By.ID,'email');
        email.clear();
        email.send_keys("email@gmail.com");

        password = browser.find_element(By.ID,'password');
        password.clear();
        password.send_keys("password123");

        login_button = browser.find_element(By.ID,'login')
        login_button.submit()
        self.assertEqual("https://proleed.academy/thanks.php", browser.current_url)
        # browser.refresh();
        nextup = browser.find_element(By.LINK_TEXT,"Back to Home Page")
        # print(nextup.get_attribute('class'))
        # self.assertTrue(nextup.is_displayed())
        nextup.click()

    @unittest.skip("skip")
    def test_name_locator(self):
        # browser = self.browser
        browser.get("https://proleed.academy/exercises/selenium/selenium-element-name-locators-practice-form.php");

        name = browser.find_element(By.NAME,'name');
        name.clear();
        name.send_keys("John Doe")

        mobileNum = browser.find_element(By.NAME,'mobile');
        mobileNum.clear();
        mobileNum.send_keys("111-222-3333");

        email = browser.find_element(By.NAME,'email')
        email.clear();
        email.send_keys("email@gmail.com");

        password = browser.find_element(By.NAME,'password')
        password.clear();
        password.send_keys("password123");

        submit = browser.find_element(By.NAME,'submit')
        submit.submit()

        self.assertEqual("https://proleed.academy/thanks.php", browser.current_url)
    
    @unittest.skip("skip")
    def test_form(self):

        browser.get("https://proleed.academy/exercises/selenium/automate-the-signup-form-using-selenium-webdriver.php")

        # First Name and Last Name
        firstname = browser.find_element(By.NAME,'firstname');
        firstname.clear();
        firstname.send_keys("John");

        lastname = browser.find_element(By.NAME,'lastname');
        lastname.clear();
        lastname.send_keys("Doe");

        # Gender Radio Button
        male = browser.find_element(By.ID,'male');
        female = browser.find_element(By.ID, "female")
        self.assertTrue(male.is_selected());
        # print(female.get_attribute('tagName'));
        parent = female.find_element(By.XPATH,'..');
        # print(parent.get_attribute('tagName'));
        # female.click(); doesn't work
        # parent.click(); doesn't work
        # ActionChains(browser).move_to_element(female).click().perform(); works
        ActionChains(browser).move_to_element(parent).click().perform();
        self.assertFalse(male.is_selected());
        self.assertTrue(female.is_selected());
        
        # Select Experience Dropdown
        experience = Select(browser.find_element(By.NAME,'experience'));
        # print(experience.first_selected_option.text);
        experience.select_by_visible_text('3');
        experience.select_by_visible_text('6');
        experience.select_by_visible_text('1');
        experience.select_by_visible_text('2');
        self.assertEqual('2', experience.first_selected_option.text);
        experience.select_by_index(0);
        self.assertEqual("Select",experience.first_selected_option.text);

        # DATE PICKER
        date = browser.find_element(By.ID,'date');
        date.clear();
        date.send_keys("11223333");

        # PROFESSION CHECK
        manual = browser.find_element(By.ID,'manual');
        automation = browser.find_element(By.ID,'automation');
        self.assertFalse(manual.is_selected())
        manual.click()
        self.assertTrue(manual.is_selected())
        automation.click()
        self.assertFalse(manual.is_selected())
        self.assertTrue(automation.is_selected())

        # Skills Checkboxs
        skills = [];
        ms_word = browser.find_element(By.ID,'msword');
        ms_excel = browser.find_element(By.ID,'msexcel');
        jira = browser.find_element(By.ID,'jira');
        selenium = browser.find_element(By.ID,'selenium');
        java = browser.find_element(By.ID,'java');
        softwaretesting = browser.find_element(By.ID,'software_testing');
        postman = browser.find_element(By.ID,'postman');
        skills.extend([ms_word, ms_excel, jira, selenium, java, softwaretesting, postman]);
        for skill in skills:
            self.assertFalse(skill.is_selected());
            skill.click();
            self.assertTrue(skill.is_selected());
        self.assertTrue(all(skill.is_selected() for skill in skills));

        # Country Dropdown
        country = Select(browser.find_element(By.NAME,'country'));
        self.assertEqual("", country.first_selected_option.get_attribute('value'));
        country.select_by_value('Canada');
        country.select_by_value('India');
        country.select_by_value('United States');
        self.assertEqual('United States', country.first_selected_option.get_attribute('value'));

        photo = browser.find_element(By.ID,'photo');
        photo.send_keys(r'C:\Users\Legen\OneDrive\Pictures\hulkxmario1.png');

        submit = browser.find_element(By.ID,'add');
        submit.submit();

        alert = Alert(browser);
        self.assertEqual("Form submitted", alert.text);
        alert.accept();

    @unittest.skip("skip")
    def test_calculations(self):
        browser.get('https://proleed.academy/exercises/selenium/emi-calculator-for-home-loan.php');

        amount = 100000
        interest = 2
        term = 12

        loanamount = browser.find_element(By.ID,'loanamount');
        loanamount.clear();
        loanamount.send_keys(amount);

        interestamount = browser.find_element(By.ID,'loaninterest');
        interestamount.clear();
        interestamount.send_keys(interest);
        
        tenure = browser.find_element(By.ID,'loanterm');
        tenure.clear();
        tenure.send_keys(term);

        calculate = browser.find_element(By.ID,'calculator');
        ActionChains(browser).move_to_element(calculate).click().perform();


        result = amount * (interest/12/100) * (1 + (interest/12/100)) ** (term) / ((1 + (interest/12/100)) ** (term) - 1);\
        print("Calculated EMI:", result);
        print(f"Expected EMI: {round(result)}");
        emi = browser.find_element(By.ID,'emi');
        print("Displayed EMI:", emi.get_attribute('value'));
        try :
            self.assertEqual(str(round(result)), emi.get_attribute('value'))
            print("EMI calculation test passed.");
        except AssertionError as e:
            print(f"EMI calculation test failed. {e}");
            raise

    @unittest.skip("demonstrating skipping")
    def test_skip(self):
        pass










# browser.get('http://google.com');
# browser.implicitly_wait(5);
# element = browser.find_element(By.CLASS_NAME,'gLFyf');
# element.clear();
# element.send_keys('Selenium');
# element.send_keys(Keys.ENTER);
# element = browser.find_element(By.NAME,'Wikipedia');
# assert 'Wikipedia' in browser.
if __name__ == '__main__':
    unittest.main();